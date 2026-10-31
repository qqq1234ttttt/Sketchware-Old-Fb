import os
import random
import time
import requests
from flask import Flask, render_template, request, jsonify

app = Flask(__name__, template_folder='.')

APPROVED_KEY = "KMT"

def creationyear(uid):
    if len(uid) == 15:
        if uid.startswith(('1000000', '1000001', '1000002', '1000003', '1000004', '1000005')): return '2009'
        elif uid.startswith(('1000006', '1000007', '1000008', '1000009', '100001')): return '2010'
        elif uid.startswith(('100002', '100003')): return '2011'
        elif uid.startswith('100004'): return '2012'
        elif uid.startswith(('100005', '100006')): return '2013'
        elif uid.startswith(('100007', '100008')): return '2014'
        elif uid.startswith('100009'): return '2015'
        elif uid.startswith('10001'): return '2016'
        elif uid.startswith('10002'): return '2017'
        elif uid.startswith('10003'): return '2018'
        elif uid.startswith('10004'): return '2019'
        elif uid.startswith('10005'): return '2020'
        elif uid.startswith('10006'): return '2021'
        elif uid.startswith(('10007', '10008')): return '2022'
        elif uid.startswith('10009'): return '2023'
        else: return '2024+'
    elif len(uid) in (9, 10): return '2008'
    elif len(uid) == 8: return '2007'
    elif len(uid) == 7: return '2006'
    return '2015+'

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/run_tool', methods=['POST'])
def run_tool():
    req_data = request.json
    user_key = req_data.get('key', '')
    series = req_data.get('series', 'A')
    limit = int(req_data.get('limit', 5))

    if user_key != APPROVED_KEY:
        return jsonify({"status": "error", "message": "[×] INVALID KEY! ACCESS DENIED."})

    logs = []
    for i in range(limit):
        if series == 'B':
            prefix = random.choice(['100003', '100004'])
            uid = prefix + ''.join(random.choices('0123456789', k=9))
        elif series == 'C':
            uid = '1000004' + ''.join(random.choices('0123456789', k=8))
        else:
            uid = '10000' + ''.join(random.choices('0123456789', k=9))

        pw = random.choice(['123456', '123123', '1234567', '12345678'])
        year = creationyear(uid)
        
        log_text = f"+(KMT OK ID)({i+1})(OK) = {uid} = {pw} = {year}"
        logs.append({"text": log_text})

    return jsonify({"status": "success", "results": logs})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
