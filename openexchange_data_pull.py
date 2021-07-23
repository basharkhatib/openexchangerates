import requests
import pandas as pd
from datetime import datetime

import psycopg2
import json
import os

from dotenv import load_dotenv

"""
The code is scheduled to be run everyday at 3AM, and it will insert the new field to the table 
"""

api_key='b0f11c5769c54c23b381f0ad0d19c619'
day_list = ""

date_ = datetime.today().strftime('%Y-%m-%d')
day_list += date_ 
# print(day_list)

# url = f'https://openexchangerates.org/api/historical/{date_}.json'

url = f'https://openexchangerates.org/api/historical/{day_list}.json'
response = requests.get(f'{url}?app_id={api_key}')

exchange_rate = response.json()["rates"]
my_json = json.dumps(exchange_rate)


# //////////////////////////////////////////
# /////////////////DATABASE/////////////////
# //////////////////////////////////////////
load_dotenv()

DB_HOST = os.getenv('DB_HOST')
DB_NAME = os.getenv('DB_NAME')
DB_USER = os.getenv('DB_USER')
DB_PASS = os.getenv('DB_PASS')

# Connecting to db
conn = psycopg2.connect(dbname=DB_NAME, user=DB_USER, password=DB_PASS, host=DB_HOST)

# Execute statements 
cur = conn.cursor()

# Create table, add to it two coloms, date and revenue_rates_usd
# cur.execute("CREATE TABLE usd_rates (id SERIAL PRIMARY KEY, date DATE , revenue_rates_usd JSONB NOT NULL );")

# Inserting new data to date and revenue_rates_usd
cur.execute("INSERT INTO usd_rates (date, revenue_rates_usd) VALUES(%s, %s)", (day_list, my_json))

# Shows everything in usd_rates table
# all_data = pd.read_sql("SELECT * FROM usd_rates;", conn)

# Read db table, converting from USD to 
all_data = pd.read_sql("SELECT date as date, revenue_rates_usd ->> 'SAR' AS SAR FROM usd_rates;", conn)

print(all_data)

conn.commit()

cur.close()
# Closing
conn.close()

