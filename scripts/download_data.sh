#!/usr/bin/env bash
set -euo pipefail

DATA_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)/data"
mkdir -p "${DATA_DIR}"

BASE_URL="https://data.insideairbnb.com/canada/bc/vancouver/2026-06-15"

echo "Downloading Inside Airbnb Vancouver (15 June 2026) snapshot to ${DATA_DIR}..."

curl -fsSL "${BASE_URL}/data/listings.csv.gz" -o "${DATA_DIR}/listings.csv.gz"
curl -fsSL "${BASE_URL}/data/calendar.csv.gz" -o "${DATA_DIR}/calendar.csv.gz"
curl -fsSL "${BASE_URL}/data/reviews.csv.gz" -o "${DATA_DIR}/reviews.csv.gz"
curl -fsSL "${BASE_URL}/visualisations/neighbourhoods.geojson" -o "${DATA_DIR}/neighbourhoods.geojson"
curl -fsSL "${BASE_URL}/visualisations/neighbourhoods.csv" -o "${DATA_DIR}/neighbourhoods.csv"

echo "Download completed successfully."
ls -lh "${DATA_DIR}"
