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
current_date = datetime.today().strftime('%Y-%m-%d')

url = f'https://openexchangerates.org/api/historical/{current_date}.json'
response = requests.get(f'{url}?app_id={api_key}')
revenue_rates = response.json()["rates"]

load_dotenv()
DB_HOST = os.getenv('DB_HOST')
DB_NAME = os.getenv('DB_NAME')
DB_USER = os.getenv('DB_USER')
DB_PASS = os.getenv('DB_PASS')

# Connecting to db
conn = psycopg2.connect(dbname=DB_NAME, user=DB_USER, password=DB_PASS, host=DB_HOST)

# Execute statements 
cur = conn.cursor()

# Inserting new data to date and revenue_rates_usd
cur.execute("INSERT INTO usd_rates (date, revenue_rates_usd) VALUES(%s, %s)", (current_date, json.dumps(revenue_rates)))

conn.commit()
cur.close()
conn.close()
