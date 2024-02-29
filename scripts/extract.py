import pandas as pd
import json
from datetime import datetime, timedelta

with open('C:/Users/Conor/Documents/Coding/Project/scripts/json_data.json') as file:
    data = json.load(file)

df = pd.DataFrame(data)
df.drop(columns=['MPRN', 'Read Type' ,'Meter Serial Number'], inplace=True)
df['Read Date and End Time'] = pd.to_datetime(df['Read Date and End Time'])
print(df)
#print(df.columns)