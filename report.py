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

start_date = sys.argv[0]
end_date = sys.argv[1]

# Select all records from usd_rates from start_date to end_date
# Get data
# Draw report
