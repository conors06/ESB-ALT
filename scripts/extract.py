import pandas as pd
import json
from datetime import datetime, timedelta
import os

# Load JSON data
try:
    with open('json_data.json') as file:
        data = json.load(file)
except FileNotFoundError:
    current_directory = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(current_directory, 'json_data.json')
    with open(file_path) as file:
        data = json.load(file)

# Function to calculate and display kW usage
def calculate_kW_usage(start_date_str, end_date_str):
    start_date = datetime.strptime(start_date_str, '%d/%m/%y')
    end_date = datetime.strptime(end_date_str, '%d/%m/%y') + timedelta(days=1)

    df = pd.DataFrame(data)
    df.drop(columns=['MPRN', 'Read Type', 'Meter Serial Number'], inplace=True)
    df['Read Date and End Time'] = pd.to_datetime(df['Read Date and End Time'], dayfirst=True)
    df['Read Value'] = pd.to_numeric(df['Read Value'])

    date_range = (df['Read Date and End Time'] >= start_date) & (df['Read Date and End Time'] < end_date)
    wantedkw_sum = df.loc[date_range, 'Read Value'].sum().round()
    return wantedkw_sum

start_input = input("Enter start date (dd/mm/yy): ")
end_input = input("Enter end date (dd/mm/yy): ")

total_kw = calculate_kW_usage(start_input, end_input)
print("Total kW usage:", total_kw)