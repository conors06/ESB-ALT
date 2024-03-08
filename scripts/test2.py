from flask import Flask, jsonify
from flask_cors import CORS
import pandas as pd
import os
import json
import matplotlib.pyplot as plt

app = Flask(__name__)
CORS(app)

def process_data(startTime, endTime):
    try:
        with open('../json_data.json') as file:
            data = json.load(file)
    except FileNotFoundError:
        current_directory = os.path.dirname(os.path.abspath(__file__))
        print(current_directory)
        file_path = os.path.join(current_directory, '../json_data.json')
        with open(file_path) as file:
            data = json.load(file)

    df = pd.DataFrame(data)
    df.drop(columns=['MPRN', 'Read Type', 'Meter Serial Number'], inplace=True)
    df['Read Date and End Time'] = pd.to_datetime(df['Read Date and End Time'], format='%d-%m-%Y %H:%M')
    df['Read Value'] = pd.to_numeric(df['Read Value'])

    date_range = (df['Read Date and End Time'] >= startTime) & (df['Read Date and End Time'] < endTime)
    filtered_df = df[date_range]


    chart_data = {
        'labels': filtered_df['Read Date and End Time'].dt.strftime('%Y-%m-%d %H:%M:%S').tolist(),
        'data': filtered_df['Read Value'].tolist()
    }

    return chart_data

def show_chart(filtered_df):
    plt.figure(figsize=(10, 6))
    plt.plot(filtered_df['Read Date and End Time'], filtered_df['Read Value'])
    plt.xlabel('Read Date and End Time')
    plt.ylabel('Read Value')
    plt.title('Energy Usage')
    plt.savefig('chart.png')

@app.route('/chart_data')
def get_chart_data():
    startTime = "22/05/22"
    endTime = "23/05/22"

    chart_data = process_data(startTime, endTime)

    return jsonify(chart_data)

if __name__ == '__main__':
    app.run(debug=True)