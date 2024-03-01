import pandas as pd
import json
from datetime import datetime, timedelta, time, date
import os
import tkinter as tk
from tkcalendar import Calendar, DateEntry
import sv_ttk

# Load JSON data
try:
    with open('json_data.json') as file:
        data = json.load(file)
except FileNotFoundError:
    current_directory = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(current_directory, 'json_data.json')
    with open(file_path) as file:
        data = json.load(file)

# Create Tkinter GUI
root = tk.Tk()
root.title("Date Range Selector")

# Function to calculate and display kW usage
def calculate_kW_usage():
    start_date = datetime.combine(cal_start.get_date(), time.min)
    end_date = datetime.combine(cal_end.get_date(), time.min) + timedelta(days=1)
    
    df = pd.DataFrame(data)
    df.drop(columns=['MPRN', 'Read Type', 'Meter Serial Number'], inplace=True)
    df['Read Date and End Time'] = pd.to_datetime(df['Read Date and End Time'], dayfirst=True)
    df['Read Value'] = pd.to_numeric(df['Read Value'])
    
    date_range = (df['Read Date and End Time'] >= start_date) & (df['Read Date and End Time'] < end_date)
    wantedkw_sum = df.loc[date_range, 'Read Value'].sum().round()
    result_label.config(text="Your kW usage is: {} KW".format(wantedkw_sum))

# Create calendar date entry widgets
cal_start = DateEntry(root, width=12, background='darkblue', foreground='white', borderwidth=2, date_pattern='dd/mm/yy')
cal_end = DateEntry(root, width=12, background='darkblue', foreground='white', borderwidth=2, date_pattern='dd/mm/yy')
cal_start.grid(row=0, column=0, padx=10, pady=10)
cal_end.grid(row=0, column=1, padx=10, pady=10)

# Create calculate button
calculate_button = tk.Button(root, text="Calculate", command=calculate_kW_usage )
calculate_button.grid(row=1, columnspan=2, padx=10, pady=10, )

# Create result label
result_label = tk.Label(root, text="")
result_label.grid(row=2, columnspan=2, padx=10, pady=10)

sv_ttk.set_theme("dark")
root.mainloop()