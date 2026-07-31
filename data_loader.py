"""Downloading, cleaning and feature engineering for NYC taxi trip data."""

import os
import urllib.request

import numpy as np
import pandas as pd

DATA_URL = "https://d37ci6vzurychx.cloudfront.net/trip-data/yellow_tripdata_2024-01.parquet"
TARGET_COLUMNS = [
    "trip_distance",
    "fare_amount",
    "tip_amount",
    "tolls_amount",
    "passenger_count",
    "payment_type",
    "tpep_pickup_datetime",
    "tpep_dropoff_datetime",
    "PULocationID",
    "DOLocationID",
]

MAX_DISTANCE_MILES = 100.0
MAX_DURATION_MINUTES = 720.0
MAX_FARE = 1000.0
MAX_SPEED_MPH = 90.0


def download_data(url=DATA_URL, dest="data/yellow_tripdata_2024-01.parquet", retries=3):
    """Download the dataset if it does not exist locally. Returns the file path."""
    if os.path.exists(dest) and os.path.getsize(dest) > 0:
        return dest
    os.makedirs(os.path.dirname(dest) or ".", exist_ok=True)
    last_error = None
    for attempt in range(1, retries + 1):
        try:
            print(f"Downloading {url} (attempt {attempt}/{retries})...")
            urllib.request.urlretrieve(url, dest)
            if os.path.getsize(dest) == 0:
                raise IOError("Downloaded file is empty")
            return dest
        except Exception as exc:  # noqa: BLE001 - surface any network issue
            last_error = exc
            if attempt < retries:
                print(f"  attempt failed ({exc}); retrying...")
    raise ConnectionError(f"Failed to download {url} after {retries} attempts: {last_error}")


def _compute_features(df):
    """Add derived columns: trip duration, pickup hour, and average speed (mph)."""
    out = df.copy()
    out["trip_duration_min"] = (
        pd.to_datetime(out["tpep_dropoff_datetime"]) - pd.to_datetime(out["tpep_pickup_datetime"])
    ).dt.total_seconds() / 60.0
    out["pickup_hour"] = pd.to_datetime(out["tpep_pickup_datetime"]).dt.hour
    out["avg_speed_mph"] = out["trip_distance"] / (out["trip_duration_min"] / 60.0)
    return out


def _filter_outliers(df):
    """Remove implausible records (negative fares, absurd distances, bad timestamps)."""
    mask = (
        (df["trip_distance"] > 0)
        & (df["trip_distance"] <= MAX_DISTANCE_MILES)
        & (df["trip_duration_min"] >= 1.0)
        & (df["trip_duration_min"] <= MAX_DURATION_MINUTES)
        & (df["fare_amount"] > 0)
        & (df["fare_amount"] <= MAX_FARE)
        & (df["tip_amount"] >= 0)
        & (df["passenger_count"].between(1, 6))
        & (df["avg_speed_mph"] > 0)
        & (df["avg_speed_mph"] <= MAX_SPEED_MPH)
    )
    return df.loc[mask]


def load_and_clean(path="data/yellow_tripdata_2024-01.parquet", max_samples=100_000, random_state=42):
    """Load the parquet file, clean it and return a tidy, cluster-ready DataFrame.

    Rows that cannot be parsed are dropped. A random sample is returned so that
    clustering stays fast on laptops, while remaining representative.
    """
    if not os.path.exists(path):
        raise FileNotFoundError(f"Data file not found: {path}")
    try:
        df = pd.read_parquet(path)
    except Exception as exc:  # noqa: BLE001
        raise ValueError(f"Could not read parquet file {path}: {exc}") from exc

    missing = [c for c in TARGET_COLUMNS if c not in df.columns]
    if missing:
        raise ValueError(f"File is missing required columns: {missing}")

    df = df[TARGET_COLUMNS]
    df = _compute_features(df)

    numeric_cols = [c for c in df.columns if c != "tpep_pickup_datetime" and c != "tpep_dropoff_datetime"]
    df[numeric_cols] = df[numeric_cols].apply(pd.to_numeric, errors="coerce")
    df = df.dropna(subset=["trip_duration_min"])

    cleaned = _filter_outliers(df)
    if len(cleaned) == 0:
        raise ValueError("Cleaning removed every row; check the raw data")

    if max_samples and len(cleaned) > max_samples:
        cleaned = cleaned.sample(n=max_samples, random_state=random_state)

    return cleaned.reset_index(drop=True)


def prepare_features(df, feature_cols):
    """Return a standardised NumPy matrix of the chosen numeric features."""
    matrix = df[feature_cols].to_numpy(dtype=float)
    if np.isnan(matrix).any():
        raise ValueError("Feature matrix contains NaN; clean the data first")
    means = matrix.mean(axis=0)
    stds = matrix.std(axis=0)
    stds[stds == 0] = 1.0
    return (matrix - means) / stds
