from dataclasses import asdict
import polars as pl
import duckdb

from db_data_generator.order.factories import (
    ALL_STOCK,
    CustomerFactory,
    generate_dataframe,
)


df = generate_dataframe(20000, CustomerFactory)

stock_df = pl.DataFrame([asdict(stock) for stock in ALL_STOCK])
stock_df.write_csv("data/stock.csv")

df.select(
    "customer_id",
    "name",
    "date_of_birth",
).write_csv("data/customer.csv")

address_df = (
    df.select("customer_id", "addresses").explode("addresses").unnest("addresses")
)
address_df.write_csv("data/customer_address.csv")

order_df = df.select("customer_id", "orders").explode("orders").unnest("orders")

order_df.select(
    "order_id",
    "customer_id",
    pl.col("address").alias("address_id"),
).write_csv("data/order_record.csv")

order_status_df = order_df.select(
    "order_id", "order_status_id", "order_status", "status_date"
).explode("order_status", "status_date", "order_status_id")

order_status_df.write_csv("data/order_status.csv")

order_line_item_df = (
    order_df.select("order_lines")
    .explode("order_lines")
    .unnest("order_lines")
    .unnest("stock")
    .with_columns(
        price=(pl.col("quantity_ordered") * pl.col("price_per_item")).cast(
            pl.Decimal(scale=2)
        )
    )
    .drop("name", "quantity", "price_per_item")
)
order_line_item_df.write_csv("data/order_line_item.csv")

with duckdb.connect("data/orders.ddb") as conn:
    for table_type in [
        "stock",
        "customer",
        "customer_address",
        "order_record",
        "order_line_item",
        "order_status",
    ]:
        conn.execute(f"DROP TABLE IF EXISTS {table_type};")
        conn.read_csv(f"data/{table_type}.csv").create(table_type)
