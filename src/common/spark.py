"""Factory for the SparkSession shared by every job of the project."""

import os

import pyspark
from pyspark.sql import SparkSession

# The connector version must match the installed Spark version (Scala 2.12).
KAFKA_PACKAGE = f"org.apache.spark:spark-sql-kafka-0-10_2.12:{pyspark.__version__}"


def get_spark(app_name: str, with_kafka: bool = False) -> SparkSession:
    """Return a SparkSession configured for this project.

    Args:
        app_name: Name shown in the Spark UI.
        with_kafka: Load the Kafka connector (needed for streaming jobs only).
    """
    builder = (
        SparkSession.builder.appName(app_name)
        .master(os.environ.get("SPARK_MASTER", "local[*]"))
        .config("spark.driver.memory", os.environ.get("SPARK_DRIVER_MEMORY", "4g"))
        .config(
            "spark.sql.shuffle.partitions",
            os.environ.get("SPARK_SHUFFLE_PARTITIONS", "16"),
        )
        .config("spark.sql.session.timeZone", "UTC")
    )
    if with_kafka:
        builder = builder.config("spark.jars.packages", KAFKA_PACKAGE)

    spark = builder.getOrCreate()
    spark.sparkContext.setLogLevel(os.environ.get("SPARK_LOG_LEVEL", "WARN"))
    return spark
