#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
from sqlalchemy import create_engine
from dotenv import load_dotenv
load_dotenv()
import os
from tqdm.auto import tqdm
import click


db_host = os.environ["DB_HOST"]
db_port = os.environ["DB_PORT"]
db_name = os.environ["DB_NAME"]
db_pw = os.environ["DB_PASSWORD"]
db_us = os.environ["DB_USERNAME"]

data_path = os.environ["URL"]

@click.command()
@click.option('--pg-user', default=db_us, help='PostgreSQL user')
@click.option('--pg-pass', default=db_pw, help='PostgreSQL password')
@click.option('--pg-host', default=db_host, help='PostgreSQL host')
@click.option('--pg-port', default=db_port, type=int, help='PostgreSQL port')
@click.option('--pg-db', default=db_name, help='PostgreSQL database name')
@click.option('--target-table', default=os.environ["DATA"], help='Target table name')
@click.option('--year', default=2021, type=int, help='Year of the data')
@click.option('--month', default=1, type=int, help='Month of the data')
@click.option('--chunksize', default=100000, type=int, help='Chunk size for reading CSV')

def run(pg_user, pg_pass, pg_host, pg_port, pg_db, year, month, target_table, chunksize):
    """Ingest NYC taxi data into PostgreSQL database."""

    url = f'{data_path}yellow_tripdata_{year}-{month:02d}.csv.gz'
    engine = create_engine(f'postgresql+psycopg://{pg_user}:{pg_pass}@{pg_host}:{pg_port}/{pg_db}')
    # Read a sample of the data
    dtype = {
        "VendorID": "Int64",
        "passenger_count": "Int64",
        "trip_distance": "float64",
        "RatecodeID": "Int64",
        "store_and_fwd_flag": "string",
        "PULocationID": "Int64",
        "DOLocationID": "Int64",
        "payment_type": "Int64",
        "fare_amount": "float64",
        "extra": "float64",
        "mta_tax": "float64",
        "tip_amount": "float64",
        "tolls_amount": "float64",
        "improvement_surcharge": "float64",
        "total_amount": "float64",
        "congestion_surcharge": "float64"
    }

    parse_dates = [
        "tpep_pickup_datetime",
        "tpep_dropoff_datetime"
    ]

    df_iter = pd.read_csv(
        url,
        dtype=dtype,
        parse_dates=parse_dates,
        iterator=True,
        chunksize=chunksize,
    )
    total_rows = 0
    for i, df_chunk in enumerate(tqdm(df_iter, desc="Ingestion progression")):

        mode = "replace" if i == 0 else "append"
        df_chunk.to_sql(name=target_table, con=engine, if_exists=mode, index=False)
        total_rows += len(df_chunk)
        print("Inserted:", total_rows)

    count = pd.read_sql("SELECT COUNT(*) FROM yellow_taxi_data;", con=engine).iloc[0, 0]
    print(total_rows == count)

    # df_csv = pd.read_csv(
    #     data_path,
    #     dtype=dtype,
    #     parse_dates=parse_dates)
    # 
    # print(len(df_csv))
    # print(df_csv["passenger_count"].sum())
    # print(df_csv["tpep_pickup_datetime"].max())
    # print(df_csv["tpep_pickup_datetime"].min())
if __name__ == '__main__':
    run()
