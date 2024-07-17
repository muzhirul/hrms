import requests
from datetime import datetime
from decouple import config

def product_registration():
    # pass
    # For insert attendance data for each employee
    url = f"{config('BASE_URL')}/staff/api/attendance/process"
    payload={}
    headers = {}
    response = requests.request("GET", url, headers=headers, data=payload)
    print('Insert Attendance data process DONE')
    url = f"{config('BASE_URL')}/staff/api/attendance/update/process"
    payload={}
    headers = {}
    response = requests.request("GET", url, headers=headers, data=payload)
    print('Attendance data update process DONE')