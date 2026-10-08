"""Project-wide paths and settings, overridable with environment variables."""

import os
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]
DATA_DIR = Path(os.environ.get("DATA_DIR", PROJECT_ROOT / "data"))

RAW_DIR = DATA_DIR / "raw"  # original .tsv.gz files from IMDb
PARQUET_DIR = DATA_DIR / "parquet"  # raw tables converted to Parquet
CLEAN_DIR = DATA_DIR / "clean"  # cleaned tables used by every analysis

KAFKA_BOOTSTRAP_SERVERS = os.environ.get("KAFKA_BOOTSTRAP_SERVERS", "localhost:29092")
