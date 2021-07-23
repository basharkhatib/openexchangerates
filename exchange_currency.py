import requests
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from datetime import date, timedelta

import psycopg2
import os

from dotenv import load_dotenv

"""
In this script you can choose start and end date, and it will show you the transfer from USD to SAR for each day.
And if you want to check for another currency just change the desired_currency to the symbol of the currency you would like check.
Remember it converts USD to the symbol you chose. 
"""


api_key='b0f11c5769c54c23b381f0ad0d19c619'
desired_currency = 'SAR'

sdate = date(2021, 4, 23)   # start date
edate = date(2021, 7, 23)   # end date

delta = edate - sdate       # as timedelta
revenue_list_per_day = []
day_list = []

for i in range(delta.days + 1):
    day = sdate + timedelta(days=i)
    day_list.append(day)
    url = f'https://openexchangerates.org/api/historical/{day}.json'
    response = requests.get(f'{url}?app_id={api_key}')
    
    exchange_rate = response.json()["rates"][desired_currency]
    revenue_list_per_day.append(exchange_rate)


# the label locations
x = np.arange(len(day_list))
# the width of the bars
width = 0.35
fig, ax = plt.subplots()
rects2 = ax.bar(x + width/20, revenue_list_per_day, width)


# Add some text for labels, title and custom x-axis tick labels, etc.
ax.set_ylabel('Exchange from USD to SAR')
ax.set_title('USD to SAR')
ax.set_xticks(x)
ax.set_xticklabels(day_list)
ax.set_ylim([3,4])

# To display price top of the bar
# ax.bar_label(rects2)

# To display the graph
plt.show(block=True)

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

# Create table, add to it three coloms id, exchange and exchange_date
# cur.execute("CREATE TABLE exchange_currency (id SERIAL PRIMARY KEY, exchange NUMERIC, exchange_date DATE);")

# Inserting new data to revenue_list_per_day and day_list
for revenue, date_ in zip(revenue_list_per_day, day_list):
    cur.execute("INSERT INTO exchange_currency (exchange, exchange_date) VALUES(%s, %s)", (revenue, date_))


# Read db table
all_data = pd.read_sql("SELECT * FROM exchange_currency;", conn)
print(all_data)

conn.commit()

cur.close()
# Closing
conn.close()