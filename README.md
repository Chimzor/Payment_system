# NYC Taxi Trip Clustering with K-Means

A Python application that clusters New York City yellow-taxi trip records
(January 2024) from the [AWS Registry of Open Data](https://registry.opendata.aws/nyc-tlc-trip-records-pds/)
using a K-Means algorithm implemented from scratch with NumPy.

## Dataset

- **Name:** NYC Taxi and Limousine Commission (TLC) Trip Record Data
- **Provider:** City of New York, published on AWS (`s3://nyc-tlc`, us-east-1)
- **License:** NYC TLC terms of use (free, public)
- **File:** `yellow_tripdata_2024-01.parquet` (~2.96M trips, ~48 MB)
- **Direct download:** `https://d37ci6vzurychx.cloudfront.net/trip-data/yellow_tripdata_2024-01.parquet`

## Features used for clustering

| Feature | Description |
|---|---|
| `trip_distance` | Trip distance in miles |
| `trip_duration_min` | Drop-off minus pick-up time, in minutes (engineered) |
| `avg_speed_mph` | Average trip speed in mph (engineered: distance / duration) |
| `fare_amount` | Fare in USD |
| `tip_amount` | Tip in USD |
| `passenger_count` | Number of passengers |
| `pickup_hour` | Hour of day the trip started (engineered) |

Cleaning: drops records with negative/zero fares, distances over 100 mi,
durations outside 1-720 min, speeds over 90 mph, more than 6 passengers, and
unparseable dates.
All features are standardised (zero mean, unit variance) before clustering.

## How to run

**Quickest way (one command):**

```bash
./run.sh        # macOS / Linux (first run sets everything up automatically)
```

```bat
run.bat         # Windows
```

**Manually:**

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python main.py                       # full pipeline, k chosen via elbow method
python main.py --k 4 --sample 50000  # fixed k / smaller sample
```

The ~48MB dataset is downloaded automatically on first run; you don't need to ship it.

Outputs (in `results/`):
- `elbow_plot.png` — within-cluster sum of squares vs k
- `cluster_scatter.png` — distance vs fare/tip, coloured by cluster
- `pca_view.png` — 2-D PCA projection of the clusters
- `cluster_profiles.csv` — median profile per cluster
- `clustered_trips.csv` — cleaned sample with cluster labels
- `run_summary.csv` — parameters and fit statistics

## Tests

```bash
pytest tests/ -v
```

The suite covers cluster correctness on synthetic data, input validation,
reproducibility, outlier filtering, feature engineering, and helper logic.
