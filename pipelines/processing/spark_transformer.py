# Step 1: PySpark Delta Lake Pipeline (pipelines/processing/spark_transformer.py)
# This script reads raw match JSON payloads from data/raw/, cleans schema irregularities,
# calculates rolling team form metrics, and writes the structured data to Delta Lake 
# (data/delta/matches).

import logging
from pyspark.sql import SparkSession
from pyspark.sql.functions import col, when
from config.settings import RAW_DATA_DIR, DELTA_DATA_DIR

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")


def get_spark_session() -> SparkSession:
    """Initialize PySpark session with Delta Lake support."""
    return (
        SparkSession.builder
        .appName("SportsLakehouseTransformer")
        .config("spark.jars.packages", "io.delta:delta-spark_2.12:3.0.0")
        .config("spark.sql.extensions", "io.delta.sql.DeltaSparkSessionExtension")
        .config("spark.sql.catalog.spark_catalog", "org.apache.spark.sql.delta.catalog.DeltaCatalog")
        .getOrCreate()
    )

def process_raw_matches_to_delta() -> None:
    """Combine all saved competition match payloads and write them to Delta Lake."""
    spark = get_spark_session()
    raw_json_paths = sorted(RAW_DATA_DIR.glob("raw_*_matches.json"))

    if not raw_json_paths:
        logging.warning("No raw competition matches found in %s. Run ingestion first.", RAW_DATA_DIR)
        return

    logging.info("Loading match data from %s files", len(raw_json_paths))
    df = spark.read.option("multiline", "true").json([str(path) for path in raw_json_paths])

    if "matches" in df.columns:
        matches_df = df.selectExpr("explode(matches) as match").select("match.*")
    else:
        matches_df = df

    transformed_df = matches_df.select(
        col("id").alias("match_id"),
        col("utcDate").alias("match_date"),
        col("competition.code").alias("competition_code"),
        col("competition.name").alias("competition_name"),
        col("homeTeam.name").alias("home_team"),
        col("awayTeam.name").alias("away_team"),
        col("score.fullTime.home").alias("home_goals"),
        col("score.fullTime.away").alias("away_goals"),
        col("status").alias("match_status")
    ).withColumn(
        "winner",
        when(col("home_goals").isNull() | col("away_goals").isNull(), None)
        .when(col("home_goals") > col("away_goals"), "HOME_TEAM")
        .when(col("away_goals") > col("home_goals"), "AWAY_TEAM")
        .otherwise("DRAW")
    )

    delta_output_path = DELTA_DATA_DIR / "matches"

    logging.info(f"Writing transformed data to Delta Lake at {delta_output_path}")
    (
        transformed_df.write
        .format("delta")
        .mode("overwrite")
        .save(str(delta_output_path))
    )

    logging.info("Successfully updated Delta Lake matches table.")


if __name__ == "__main__":
    process_raw_matches_to_delta()