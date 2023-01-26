#!/usr/bin/env python
# coding: utf-8

import os
import argparse

from time import time

import pandas as pd

from sqlalchemy import create_engine

def main(params):
    user = params.user
    password = params.password
    host = params.host
    port = params.port
    db = params.db
    table_name = params.table_name
    url = params.url
    file_path = 'related_taxi_data.csv'

    os.system(f"wget {url} -O {file_path}")
    # download the csv

    # engine = create_engine('postgresql://nnesco:nnesco100@localhost:5433/ny_taxi')
    engine = create_engine(f'postgresql://{user}:{password}@{host}:{port}/{db}')

    engine.connect()

    

    df_iter = pd.read_csv(file_path, iterator=True, chunksize=100000)
    df = next(df_iter)

    print(pd.io.sql.get_schema(df, name='yellow_tripdata', con=engine))
    
    df.head(n=0).to_sql(name=table_name, con=engine, if_exists='replace')

    df.to_sql(name=table_name, con=engine, if_exists='append')

    while True:
        t_start = time()
        df = next(df_iter)
        
        df.lpep_pickup_datetime = pd.to_datetime(df.lpep_pickup_datetime)
        df.lpep_dropoff_datetime = pd.to_datetime(df.lpep_dropoff_datetime)
        
        df.to_sql(name=table_name, con=engine, if_exists='append')
        
        t_end = time()
        print('inserted another chunk..., took %.3f seconds' % (t_end - t_start))

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Injest CSV data to postgres')

    parser.add_argument('--user', help='username for postgres')
    parser.add_argument('--password', help='password for postgres')
    parser.add_argument('--host', help='host for postgres')
    parser.add_argument('--db', help='database for postgres')
    parser.add_argument('--port', help='port for postgres')
    parser.add_argument('--table_name', help='name of the table we will write the results to')
    parser.add_argument('--url', help='url of the csv')

    args = parser.parse_args()
    main(args)

