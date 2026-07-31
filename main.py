"""NYC Taxi Trip Clustering — K-Means application.

Clusters yellow-taxi trips from the AWS Registry of Open Data using a
from-scratch K-Means implementation, then reports cluster profiles and
writes plots and results to disk.

Usage:
    python main.py                      # full pipeline on default settings
    python main.py --k 4 --sample 50000 # tune the number of clusters / sample size
"""

import argparse
import os
import sys

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
import numpy as np  # noqa: E402
import pandas as pd  # noqa: E402

import data_loader  # noqa: E402
from kmeans import KMeans, elbow_wcss  # noqa: E402

FEATURE_COLS = [
    "trip_distance",
    "trip_duration_min",
    "avg_speed_mph",
    "fare_amount",
    "tip_amount",
    "passenger_count",
    "pickup_hour",
]


def run_pipeline(args):
    os.makedirs(args.output_dir, exist_ok=True)

    print("Step 1/5: Downloading data if needed...")
    data_path = data_loader.download_data(dest=args.data)

    print("Step 2/5: Loading and cleaning data...")
    df = data_loader.load_and_clean(path=data_path, max_samples=args.sample, random_state=args.seed)
    print(f"  {len(df):,} trips ready for clustering")
    df.to_csv(os.path.join(args.output_dir, "cleaned_sample.csv"), index=False)

    print("Step 3/5: Selecting k with the elbow method...")
    X = data_loader.prepare_features(df, FEATURE_COLS)
    k_choices = list(range(2, args.max_k + 1))
    wcss = elbow_wcss(X, k_choices, random_state=args.seed)
    _plot_elbow(k_choices, list(wcss.values()), os.path.join(args.output_dir, "elbow_plot.png"))
    k = args.k if args.k else _pick_elbow(k_choices, list(wcss.values()))
    print(f"  chosen k = {k}")

    print("Step 4/5: Clustering with K-Means...")
    model = KMeans(n_clusters=k, random_state=args.seed).fit(X)
    df["cluster"] = model.labels_
    df.to_csv(os.path.join(args.output_dir, "clustered_trips.csv"), index=False)
    print(f"  converged in {model.n_iter_} iterations, inertia = {model.inertia_:,.0f}")

    print("Step 5/5: Writing reports and plots...")
    profile = _cluster_profile(df)
    profile.to_csv(os.path.join(args.output_dir, "cluster_profiles.csv"))
    print(profile.to_string())
    _plot_scatter(df, model, os.path.join(args.output_dir, "cluster_scatter.png"))
    _plot_speed(df, os.path.join(args.output_dir, "cluster_speed.png"))
    _plot_pca(X, model, os.path.join(args.output_dir, "pca_view.png"))

    summary = {
        "dataset": "NYC TLC yellow taxi trip records, January 2024",
        "source": data_loader.DATA_URL,
        "rows_after_cleaning": len(df),
        "features": FEATURE_COLS,
        "n_clusters": k,
        "inertia": model.inertia_,
        "iterations": model.n_iter_,
    }
    pd.Series(summary).to_csv(os.path.join(args.output_dir, "run_summary.csv"))
    print(f"\nDone. Results saved to {args.output_dir}/")


def _pick_elbow(k_choices, wcss_values):
    """Pick k at the elbow: the point of maximum perpendicular distance from the line."""
    x = np.asarray(k_choices, dtype=float)
    y = np.asarray(wcss_values, dtype=float)
    x_n = (x - x.min()) / (x.max() - x.min())
    y_n = (y - y.min()) / (y.max() - y.min())
    vx, vy = x_n[-1] - x_n[0], y_n[-1] - y_n[0]
    dx, dy = x_n[-1] - x_n, y_n[-1] - y_n
    dists = np.abs(vx * dy - vy * dx) / np.hypot(vx, vy)
    return int(x[int(np.argmax(dists))])


def _cluster_profile(df):
    """Summarise each cluster with interpretable medians and counts."""
    rows = []
    for cluster_id in sorted(df["cluster"].unique()):
        sub = df[df["cluster"] == cluster_id]
        rows.append(
            {
                "cluster": cluster_id,
                "trips": len(sub),
                "share_pct": round(100 * len(sub) / len(df), 1),
                "median_distance_mi": round(sub["trip_distance"].median(), 2),
                "median_duration_min": round(sub["trip_duration_min"].median(), 1),
                "median_fare_usd": round(sub["fare_amount"].median(), 2),
                "median_tip_usd": round(sub["tip_amount"].median(), 2),
                "median_passengers": round(sub["passenger_count"].median(), 1),
                "median_pickup_hour": round(sub["pickup_hour"].median(), 1),
                "median_speed_mph": round(sub["avg_speed_mph"].median(), 1),
            }
        )
    return pd.DataFrame(rows)


def _plot_elbow(k_choices, wcss_values, out_path):
    fig, ax = plt.subplots(figsize=(7, 5))
    ax.plot(k_choices, wcss_values, marker="o")
    ax.set_xlabel("Number of clusters (k)")
    ax.set_ylabel("Within-cluster sum of squares")
    ax.set_title("Elbow method for choosing k")
    ax.grid(True, alpha=0.3)
    fig.tight_layout()
    fig.savefig(out_path, dpi=150)
    plt.close(fig)


def _plot_scatter(df, model, out_path):
    fig, axes = plt.subplots(1, 2, figsize=(13, 5))
    cluster_ids = sorted(df["cluster"].unique())
    for cid in cluster_ids:
        sub = df[df["cluster"] == cid]
        label = f"Cluster {cid}"
        axes[0].scatter(sub["trip_distance"], sub["fare_amount"], s=4, alpha=0.35, label=label)
        axes[1].scatter(sub["trip_distance"], sub["tip_amount"], s=4, alpha=0.35, label=label)
    axes[0].set_xlabel("Trip distance (miles)")
    axes[0].set_ylabel("Fare amount (USD)")
    axes[0].set_title("Distance vs Fare")
    axes[1].set_xlabel("Trip distance (miles)")
    axes[1].set_ylabel("Tip amount (USD)")
    axes[1].set_title("Distance vs Tip")
    for ax in axes:
        ax.grid(True, alpha=0.3)
        ax.legend(markerscale=4)
    fig.suptitle("NYC taxi trip clusters")
    fig.tight_layout()
    fig.savefig(out_path, dpi=150)
    plt.close(fig)


def _plot_speed(df, out_path):
    """Bar chart of median trip speed per cluster — helps interpret each group."""
    medians = (
        df.groupby("cluster")["avg_speed_mph"].median().sort_values(ascending=False)
    )
    fig, ax = plt.subplots(figsize=(8, 5))
    ax.bar([f"Cluster {c}" for c in medians.index], medians.values, color="#4C72B0")
    ax.set_xlabel("Cluster")
    ax.set_ylabel("Median trip speed (mph)")
    ax.set_title("Median trip speed by cluster")
    ax.grid(True, axis="y", alpha=0.3)
    fig.tight_layout()
    fig.savefig(out_path, dpi=150)
    plt.close(fig)


def _plot_pca(X, model, out_path):
    """Project the 6-dimensional features onto 2 principal components for a 2-D view."""
    mean = X.mean(axis=0)
    centered = X - mean
    _, _, vt = np.linalg.svd(centered, full_matrices=False)
    proj = centered @ vt[:2].T
    fig, ax = plt.subplots(figsize=(7, 6))
    for cid in np.unique(model.labels_):
        mask = model.labels_ == cid
        ax.scatter(proj[mask, 0], proj[mask, 1], s=4, alpha=0.4, label=f"Cluster {cid}")
    ax.set_xlabel("Principal component 1")
    ax.set_ylabel("Principal component 2")
    ax.set_title("Cluster view (2-D PCA projection)")
    ax.grid(True, alpha=0.3)
    ax.legend(markerscale=4)
    fig.tight_layout()
    fig.savefig(out_path, dpi=150)
    plt.close(fig)


def main():
    parser = argparse.ArgumentParser(description="Cluster NYC taxi trips with K-Means")
    parser.add_argument("--data", default="data/yellow_tripdata_2024-01.parquet")
    parser.add_argument("--sample", type=int, default=100_000, help="max trips to cluster")
    parser.add_argument("--k", type=int, default=0, help="fixed k (0 = choose via elbow)")
    parser.add_argument("--max-k", type=int, default=10)
    parser.add_argument("--seed", type=int, default=42)
    parser.add_argument("--output-dir", default="results")
    args = parser.parse_args()

    try:
        run_pipeline(args)
    except (ValueError, FileNotFoundError, ConnectionError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
