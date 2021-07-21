import requests
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import queue
from datetime import date, timedelta, datetime

import psycopg2


api_key='1f3bb4f6de4f4a8e9a0776acff943430'
desired_currency = 'SAR'
sdate = date(2021, 4, 20)   # start date
edate = date(2021, 4, 23)   # end date
delta = edate - sdate       # as timedelta

revenue_list_per_day = []
day_list = []


for i in range(delta.days + 1):
    day = sdate + timedelta(days=i)
    day_list.append(day)
#     print(day_list, "day")
    url = f'https://openexchangerates.org/api/historical/{day}.json'
    response = requests.get(f'{url}?app_id={api_key}')
    
    exchange_rate = response.json()["rates"][desired_currency]
    revenue_list_per_day.append(exchange_rate)
# print(array)

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
# ax.legend()

"""To display price top of the bar"""
# ax.bar_label(rects2)

"""To display the graph"""
# plt.show(block=True)

# //////////////////////////////////////////
# /////////////////DATABASE/////////////////
# //////////////////////////////////////////
DB_HOST = 'tai.db.elephantsql.com'
DB_NAME = "fwuilylv"
DB_USER = "fwuilylv"
DB_PASS = "jWza7o9Uvcph9z8zFrbUAjZd70tziMRh"

# Connecting to db
conn = psycopg2.connect(dbname=DB_NAME, user=DB_USER, password=DB_PASS, host=DB_HOST)

# Execute statements 
cur = conn.cursor()

# cur.execute("CREATE TABLE sar_exchange_currency (id SERIAL PRIMARY KEY, exchange NUMERIC, exchange_date DATE);")
# cur.execute('DELETE FROM sar_exchange_currency;')
for revenue, date_ in zip(revenue_list_per_day, day_list):
    cur.execute("INSERT INTO sar_exchange_currency (exchange, exchange_date) VALUES(%s, %s)", (revenue,date_))
all_data = pd.read_sql("SELECT * FROM sar_exchange_currency;", conn)
print(all_data)

conn.commit()

cur.close()
# Closing
conn.close()