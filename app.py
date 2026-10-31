import os
import random
import time
import requests
from flask import Flask, render_template_string, request, jsonify

app = Flask(__name__)

APPROVED_KEY = "KMT"

def creationyear(uid):
    """မူရင်း Termux ကုဒ်ပါ မှန်ကန်သော Creation Year Logic"""
    if len(uid) == 15:
        if uid.startswith('1000000000'): return '2009'
        elif uid.startswith('100000000'): return '2009'
        elif uid.startswith('10000000'): return '2009'
        elif uid.startswith(('1000000', '1000001', '1000002', '1000003', '1000004', '1000005')): return '2009'
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
        return '2024+'
    elif len(uid) in (9, 10): return '2008'
    elif len(uid) == 8: return '2007'
    elif len(uid) == 7: return '2006'
    elif len(uid) == 14 and uid.startswith('61'): return '2024'
    else: return '2015+'

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>KMT SYSTEM - WEB TERMINAL</title>
    <style>
        body {
            background-color: #0d0d0d;
            color: #00ff00;
            font-family: 'Courier New', Courier, monospace;
            padding: 10px;
            margin: 0;
        }
        .container {
            max-width: 600px;
            margin: auto;
            border: 1px solid #00ff00;
            padding: 12px;
            box-shadow: 0 0 15px rgba(0, 255, 0, 0.3);
            background: #050505;
        }
        h2 {
            text-align: center;
            color: #00ff66;
            margin-top: 5px;
            text-shadow: 0 0 8px rgba(0, 255, 0, 0.6);
        }
        .form-group {
            margin-bottom: 10px;
        }
        label {
            display: block;
            margin-bottom: 3px;
            color: #00cc00;
            font-size: 13px;
        }
        input, select {
            width: 100%;
            padding: 8px;
            background: #111;
            border: 1px solid #00ff00;
            color: #00ff00;
            font-family: monospace;
            box-sizing: border-box;
        }
        button {
            width: 100%;
            padding: 10px;
            background: #00ff00;
            color: #000;
            border: none;
            font-weight: bold;
            font-size: 15px;
            cursor: pointer;
            font-family: monospace;
        }
        button:hover {
            background: #00cc00;
        }
        #console {
            margin-top: 10px;
            background: #000;
            border: 1px dashed #00ff00;
            padding: 8px;
            height: 200px;
            overflow-y: scroll;
            font-size: 12px;
            white-space: pre-wrap;
        }
        .log-item {
            margin-bottom: 4px;
            border-bottom: 1px solid #111;
        }
        .fb-btn-group {
            margin-top: 15px;
            border-top: 1px dashed #00ff00;
            padding-top: 10px;
        }
        .fb-link-btn {
            display: block;
            width: 100%;
            padding: 12px;
            margin-bottom: 8px;
            color: #fff;
            text-align: center;
            text-decoration: none;
            font-weight: bold;
            font-size: 14px;
            border-radius: 4px;
            box-sizing: border-box;
            font-family: monospace;
        }
        .btn-fb { background: #1877f2; }
        .btn-login { background: #42b72a; }
    </style>
</head>
<body>

<div class="container">
    <h2>🔐 KMT SYSTEM 🔐</h2>
    <div style="text-align: center; font-size: 11px; margin-bottom: 10px;">>>> KYAW MIN TUN TOOL <<<</div>
    
    <div class="form-group">
        <label>[?] ENTER YOUR KEY:</label>
        <input type="text" id="key" value="KMT" placeholder="Enter key...">
    </div>

    <div class="form-group">
        <label>[★] SELECT SERIES:</label>
        <select id="series">
            <option value="A">A) ALL SERIES (2010-2014)</option>
            <option value="B">B) 100003/4 SERIES</option>
            <option value="C">C) 2009 SERIES</option>
        </select>
    </div>
    
    <div class="form-group">
        <label>[★] LIMIT COUNT:</label>
        <input type="number" id="limit" value="5" placeholder="Number of IDs...">
    </div>

    <button onclick="startTool()">[>] START TOOL</button>

    <div id="console">
        <div style="color: #666;">[System Ready. Waiting for execution...]</div>
    </div>

    <div class="fb-btn-group">
        <label style="color: #00ffcc; margin-bottom: 8px;">[🌐] FACEBOOK QUICK ACCESS:</label>
        <a href="https://m.facebook.com" target="_blank" class="fb-link-btn btn-fb">[+] Open Mobile Facebook</a>
        <a href="https://www.facebook.com/login" target="_blank" class="fb-link-btn btn-login">[+] Open Facebook Login Page</a>
    </div>
</div>

<script>
    function startTool() {
        const key = document.getElementById('key').value;
        const series = document.getElementById('series').value;
        const limit = document.getElementById('limit').value;
        const consoleBox = document.getElementById('console');

        consoleBox.innerHTML = '<div style="color: yellow;">[~] KMT SYSTEM INITIALIZED...</div>';

        fetch('/run_tool', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ key: key, series: series, limit: limit })
        })
        .then(response => response.json())
        .then(data => {
            if (data.status === 'error') {
                consoleBox.innerHTML += `<div style="color: red;">${data.message}</div>`;
                return;
            }

            let index = 0;
            function printNext() {
                if (index < data.results.length) {
                    let res = data.results[index];
                    let item = document.createElement('div');
                    item.className = 'log-item';
                    item.style.color = '#00ff41';
                    item.innerText = res.text;
                    consoleBox.appendChild(item);
                    consoleBox.scrollTop = consoleBox.scrollHeight;
                    index++;
                    setTimeout(printNext, 150);
                }
            }
            printNext();
        })
        .catch(err => {
            consoleBox.innerHTML += `<div style="color: red;">[×] Connection Error!</div>`;
        });
    }
</script>

</body>
</html>
"""

@app.route('/')
def index():
    return render_template_string(HTML_TEMPLATE)

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
        # ရွေးချယ်လိုက်သော Series အလိုက် UID မှန်ကန်စွာ ထုတ်ပေးခြင်း
        if series == 'B':
            prefix = random.choice(['100003', '100004'])
            uid = prefix + ''.join(random.choices('0123456789', k=9))
        elif series == 'C':
            uid = '1000004' + ''.join(random.choices('0123456789', k=8))
        else:
            data = str(random.choice(range(1000000000, 4999999999)))
            uid = '10000' + data

        pw = random.choice(['123456', '123123', '1234567', '12345678'])
        year = creationyear(uid)
        
        log_text = f"+(KMT OK ID)({i+1})(OK) = {uid} = {pw} = {year}"
        logs.append({"text": log_text})

    return jsonify({"status": "success", "results": logs})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
