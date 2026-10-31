import os
import random
import time
import requests
from flask import Flask, render_template, request, jsonify

app = Flask(__name__, template_folder='.')

APPROVED_KEY = "KMT"

def creationyear(uid):
    """Estimates the Facebook account creation year based on the UID."""
    if len(uid) == 15:
        if uid.startswith('10000000'): return '2009'
        elif uid.startswith('100001'): return '2010'
        elif uid.startswith('100002'): return '2011'
        elif uid.startswith('100003'): return '2012'
        elif uid.startswith('100005'): return '2020'
        else: return '2021+'
    return '2015+'

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/run_tool', methods=['POST'])
def run_tool():
    req_data = request.json
    user_key = req_data.get('key', '')
    limit = int(req_data.get('limit', 5))

    if user_key != APPROVED_KEY:
        return jsonify({"status": "error", "message": "[×] INVALID KEY! ACCESS DENIED."})

    logs = []
    for _ in range(limit):
        uid = '10000' + ''.join(random.choices('0123456789', k=9))
        pw = random.choice(['123456', '1234567', '12345678'])
        year = creationyear(uid)
        logs.append({
            "uid": uid,
            "pw": pw,
            "year": year,
            "text": f"[KMT-OK] UID: {uid} | PW: {pw} | YEAR: {year}"
        })
        time.sleep(0.1)

    return jsonify({"status": "success", "results": logs})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
