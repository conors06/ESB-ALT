import pandas as pd
import json
from datetime import datetime, timedelta
import os



try:
    with open('json_data.json') as file:
        data = json.load(file)
except FileNotFoundError:
    current_directory = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(current_directory, 'json_data.json')
    with open(file_path) as file:
        data = json.load(file)

#daystoshow = int(input("Enter number of days to show: "))
df = pd.DataFrame(data)
df.drop(columns=['MPRN', 'Read Type' ,'Meter Serial Number'], inplace=True)
df['Read Date and End Time'] = pd.to_datetime(df['Read Date and End Time'])

print(df)
#print(df.columns)