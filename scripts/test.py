import pandas as pd
import json
from datetime import datetime, timedelta, timezone
import os
import requests
from bs4 import BeautifulSoup
import re
import csv
import matplotlib.pyplot as plt, mpld3

meter_mprn = "10005513593"
esb_user_name = "conorwstorey@gmail.com"
esb_password = "MarlfieldMuffin17??"

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


esbnumber = load_smart_meter_stats_v2(esb_user_name, esb_password, meter_mprn)
print("[Done]: ", esbnumber)

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
    wanted_data = df.loc[date_range, ['Read Date and End Time', 'Read Value']]
    first_date = df['Read Date and End Time'].min()
    print("First Date:", first_date)
    last_date = df['Read Date and End Time'].max()
    print("Last Date:", last_date)

    return wanted_data



start_input = "22/02/24"
end_input = "29/02/24"

wanted_data = calculate_kW_usage(start_input, end_input)


fig, ax = plt.subplots()
ax.plot(wanted_data['Read Date and End Time'], wanted_data['Read Value'])
ax.set_title('Energy Usage Over Time')
ax.set_xlabel('Date and Time')
ax.set_ylabel('kW Usage')
html_fig = mpld3.fig_to_html(fig)
print(html_fig)
mpld3.show()
total_kw = calculate_kW_usage(start_input, end_input)
print("Total kW usage:", total_kw)