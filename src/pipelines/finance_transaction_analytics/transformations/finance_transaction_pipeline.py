from pyspark import pipelines as dp
from pyspark.sql import functions as F

catalog = spark.conf.get("finance.catalog")
schema = spark.conf.get("finance.schema")
landing_table = f"{catalog}.{schema}.landing_transactions"


@dp.table(name="bronze_card_transactions")
def bronze_card_transactions():
    return spark.readStream.table(landing_table)


@dp.table(name="silver_card_transactions")
@dp.expect_or_drop("valid_transaction_id", "transaction_id IS NOT NULL")
@dp.expect_or_drop("valid_customer_id", "customer_id IS NOT NULL")
@dp.expect_or_drop("positive_amount", "amount > 0")
@dp.expect_or_drop("valid_currency", "currency = 'INR'")
def silver_card_transactions():
    source = spark.readStream.table(
        f"{catalog}.{schema}.bronze_card_transactions"
    )
    return (
        source
        .withColumn("transaction_type", F.upper(F.trim("transaction_type")))
        .withColumn("channel", F.upper(F.trim("channel")))
        .withColumn("merchant_category", F.upper(F.trim("merchant_category")))
        .withColumn("amount", F.col("amount").cast("decimal(18,2)"))
        .withColumn(
            "spend_category",
            F.when(F.col("merchant_category").isin("GROCERY", "SUPERMARKET"), "ESSENTIALS")
             .when(F.col("merchant_category").isin("FUEL", "TRANSPORT"), "TRANSPORT")
             .when(F.col("merchant_category").isin("DINING", "RESTAURANT"), "DINING")
             .when(F.col("merchant_category").isin("SHOPPING", "E_COMMERCE"), "SHOPPING")
             .when(F.col("merchant_category").isin("UTILITIES", "BILLS"), "BILLS")
             .otherwise("OTHER")
        )
        .withColumn("transaction_date", F.to_date("transaction_timestamp"))
        .withColumn("ingested_at", F.current_timestamp())
    )


@dp.materialized_view(name="gold_customer_monthly_spend")
def gold_customer_monthly_spend():
    silver = spark.read.table(
        f"{catalog}.{schema}.silver_card_transactions"
    )
    return (
        silver.filter(F.col("transaction_type") == "DEBIT")
        .groupBy(
            "customer_id",
            F.date_format("transaction_date", "yyyy-MM").alias("spend_month"),
            "spend_category",
        )
        .agg(
            F.countDistinct("transaction_id").alias("transaction_count"),
            F.sum("amount").alias("total_spend_inr"),
            F.avg("amount").alias("average_transaction_inr"),
        )
    )
