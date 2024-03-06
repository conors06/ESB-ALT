from flask import Flask, request, jsonify
from flask_cors import CORS
import pandas as pd
import json
import time
from datetime import datetime, timedelta, timezone
import os
import requests
from bs4 import BeautifulSoup
import re
import csv
import logging
import plotly.graph_objs as go

app = Flask(__name__)
CORS(app)
df = None
if os.path.exists('../json_data.json'):
    os.remove('../json_data.json')
def load_esb_data(user, password, mpnr, start_date):
    print("[+] open session ...")
    s = requests.Session()
    s.headers.update({
        'User-Agent':
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36',
    })
    print("[+] calling login page. ..")
    login_page = s.get('https://myaccount.esbnetworks.ie/',
                       allow_redirects=True)
    result = re.findall(r"(?<=var SETTINGS = )\S*;", str(login_page.content))
    settings = json.loads(result[0][:-1])
    print("[+] sending credentials ...")
    s.post(
        'https://login.esbnetworks.ie/esbntwkscustportalprdb2c01.onmicrosoft.com/B2C_1A_signup_signin/SelfAsserted?tx='
        + settings['transId'] + '&p=B2C_1A_signup_signin',
        data={
            'signInName': user,
            'password': password,
            'request_type': 'RESPONSE'
        },
        headers={
            'x-csrf-token': settings['csrf'],
        },
        allow_redirects=False)
    print("[+] passing AUTH ...")
    confirm_login = s.get(
        'https://login.esbnetworks.ie/esbntwkscustportalprdb2c01.onmicrosoft.com/B2C_1A_signup_signin/api/CombinedSigninAndSignup/confirmed',
        params={
            'rememberMe': False,
            'csrf_token': settings['csrf'],
            'tx': settings['transId'],
            'p': 'B2C_1A_signup_signin',
        })
    print("[+] confirm_login: ", confirm_login)
    print("[+] doing some BeautifulSoup ...")
    soup = BeautifulSoup(confirm_login.content, 'html.parser')
    print("[DEBUG] soup:", soup)  # Add this line to print the value of soup
    form = soup.find('form', {'id': 'auto'})
    print("[DEBUG] form:", form)  # Add this line to print the value of form
    soup = BeautifulSoup(confirm_login.content, 'html.parser')
    form = soup.find('form', {'id': 'auto'})
    s.post(
        form['action'],
        allow_redirects=False,
        data={
            'state': form.find('input', {'name': 'state'})['value'],
            'client_info': form.find('input',
                                     {'name': 'client_info'})['value'],
            'code': form.find('input', {'name': 'code'})['value'],
        },
    )

    # data = s.get('https://myaccount.esbnetworks.ie/datadub/GetHdfContent?mprn=' + mpnr + '&startDate=' + start_date.strftime('%Y-%m-%d'))
    print("[+] getting CSV file for MPRN ...")
    data = s.get('https://myaccount.esbnetworks.ie/DataHub/DownloadHdf?mprn=' +
                 mpnr + '&startDate=' + start_date.strftime('%Y-%m-%d'))

    print("[+] CSV file received !!!")
    data_decoded = data.content.decode('utf-8').splitlines()
    print("[+] data decoded from Binary format")
    json_data = csv_response_to_json(data_decoded)
    return json_data

def csv_response_to_json(csv_file):
    print("[+] creating JSON file from CSV ...")
    my_json = []
    csv_reader = csv.DictReader(csv_file)
    for row in csv_reader:
        my_json.append(row)
    with open("json_data.json", "w", encoding="utf-8") as jsonf:
        json_out = json.dumps(my_json, indent=2)
        jsonf.write(json_out)
    print("[+] end of JSON OUT.", json_out)
    print("[+] end of JSON OUT, returning value ...")
    return json_out

def parse_date(date_str):
    print("[+] parsing some data fields ...")
    if len(date_str) == 19:
        return datetime.strptime(date_str, '%Y-%m-%dT%H:%M:%S')
    else:
        dt = datetime.strptime(date_str[:19], '%Y-%m-%dT%H:%M:%S')
        tz_offset = int(date_str[-6:-3])
        tz = timezone(timedelta(hours=tz_offset))
        return dt.replace(tzinfo=tz)
def load_smart_meter_stats_v2(user, password, mpnr):
    today_ = datetime.today()
    smart_meter_data = load_esb_data(user, password, mpnr, today_)
    print("[+] smart_meter_data: ", smart_meter_data)
    print("[++] end of smart_meter_data")
    return smart_meter_data

def calculate_kW_usage(start_date_str, end_date_str):
    global df
    #start_date = datetime.strptime(start_date_str, '%d/%m/%y')
    #end_date = datetime.strptime(end_date_str, '%d/%m/%y') + timedelta(days=1)
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
    print(df)
    df['Read Date and End Time'] = pd.to_datetime(df['Read Date and End Time'], dayfirst=True)
    df['Read Value'] = pd.to_numeric(df['Read Value'])

    date_range = (df['Read Date and End Time'] >= start_date) & (df['Read Date and End Time'] < end_date)
    wantedkw_sum = df.loc[date_range, 'Read Value'].sum().round()
    return wantedkw_sum

def convert_date_format(date_string):
    # Parse the date string using the format "%b %d, %Y"
    date = datetime.strptime(date_string, "%b %d, %Y")

    # Convert the date to the desired format: dd/mm/yy
    short_date = date.strftime("%d/%m/%y")

    return short_date

@app.route('/', methods=['POST'])
def process_data():
    data = request.get_json()

    # Extract the necessary data from the request payload
    startTimeIntermediary = data.get('startTime')
    startTime = convert_date_format(startTimeIntermediary)
    print(startTime)
    endTimeIntermediary = data.get('endTime')
    endTime = convert_date_format(endTimeIntermediary)
    print(endTime)
    mprn = data.get('mprn')
    print(mprn)
    email = data.get('email')
    print(email)
    password = data.get('password')
    print(password)
    #time.sleep(5)

    esbnumber = load_smart_meter_stats_v2(email, password, mprn)
    total_kw = calculate_kW_usage(startTime, endTime)
    print(total_kw)
    return {'total_kw': total_kw}

@app.route('/graph', methods=['GET'])
def get_graph():
    # Use the global DataFrame
    global df

    if df is not None:
        fig = go.Figure(data=go.Scatter(x=df['Read Date and End Time'], y=df['Read Value'], mode='lines'))
        fig.update_layout(title='Energy Usage Over Time', xaxis_title='Date and Time', yaxis_title='kW Usage')
        json_data = fig.to_json()
        print(json_data)
        fig.show
        return json_data
    else:
        return "'error': 'No data available'"

if __name__ == '__main__':
    app.run()