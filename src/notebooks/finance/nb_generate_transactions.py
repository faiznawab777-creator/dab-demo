# Databricks notebook source
# MAGIC %run ../utils/nb_transaction_helpers

# COMMAND ----------
dbutils.widgets.text("catalog", "finance_dev")
dbutils.widgets.text("schema", "retail_banking")
dbutils.widgets.text("batch_size", "100")
dbutils.widgets.text("batch_label", "poc_batch")

catalog = dbutils.widgets.get("catalog")
schema = dbutils.widgets.get("schema")
batch_size = int(dbutils.widgets.get("batch_size"))
batch_label = dbutils.widgets.get("batch_label")
target_table = f"{catalog}.{schema}.landing_transactions"

# The catalog and schema must exist before the first job run.
spark.sql(f"""
CREATE TABLE IF NOT EXISTS {target_table} (
  transaction_id STRING,
  customer_id STRING,
  account_id STRING,
  transaction_timestamp TIMESTAMP,
  transaction_type STRING,
  channel STRING,
  merchant_name STRING,
  merchant_category STRING,
  amount DECIMAL(18,2),
  currency STRING,
  city STRING,
  batch_label STRING
) USING DELTA
""")

rows = generate_transaction_rows(batch_size=batch_size, batch_label=batch_label)
spark.createDataFrame(rows).write.format("delta").mode("append").saveAsTable(target_table)
print(f"Appended {len(rows)} records to {target_table}")
display(spark.table(target_table).orderBy("transaction_timestamp", ascending=False).limit(10))
