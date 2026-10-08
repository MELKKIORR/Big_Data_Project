"""Check that Spark, the IMDb files and Kafka are all reachable.

Usage (inside the spark container):
    python scripts/check_env.py
"""

import socket

from src.common.config import KAFKA_BOOTSTRAP_SERVERS, RAW_DIR
from src.common.spark import get_spark


def check_spark() -> None:
    spark = get_spark("check-env")
    count = spark.range(1_000_000).count()
    print(f"[ok]   Spark {spark.version} is running ({count:,} test rows)")

    ratings = RAW_DIR / "title.ratings.tsv.gz"
    if ratings.exists():
        df = spark.read.csv(str(ratings), sep="\t", header=True)
        print(f"[ok]   title.ratings readable ({df.count():,} rows)")
    else:
        print("[warn] IMDb files missing: run scripts/download_imdb.py")
    spark.stop()


def check_kafka() -> None:
    host, port = KAFKA_BOOTSTRAP_SERVERS.split(",")[0].split(":")
    try:
        with socket.create_connection((host, int(port)), timeout=5):
            print(f"[ok]   Kafka reachable at {host}:{port}")
    except OSError as error:
        print(f"[fail] Kafka not reachable at {host}:{port} ({error})")


if __name__ == "__main__":
    check_spark()
    check_kafka()
