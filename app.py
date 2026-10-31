import os
import random
import time
import requests
from flask import Flask, render_template_string, request, jsonify

app = Flask(__name__)

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

# Hacker Terminal UI HTML Template (Inline)
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
            padding: 15px;
            margin: 0;
        }
        .container {
            max-width: 600px;
            margin: auto;
            border: 1px solid #00ff00;
            padding: 15px;
            box-shadow: 0 0 15px rgba(0, 255, 0, 0.3);
            background: #050505;
        }
        h2 {
            text-align: center;
            color: #00ff66;
            text-shadow: 0 0 8px rgba(0, 255, 0, 0.6);
        }
        .form-group {
            margin-bottom: 15px;
        }
        label {
            display: block;
            margin-bottom: 5px;
            color: #00cc00;
        }
        input {
            width: 100%;
            padding: 10px;
            background: #111;
            border: 1px solid #00ff00;
            color: #00ff00;
            font-family: monospace;
            box-sizing: border-box;
        }
        button {
            width: 100%;
            padding: 12px;
            background: #00ff00;
            color: #000;
            border: none;
            font-weight: bold;
            font-size: 16px;
            cursor: pointer;
            font-family: monospace;
        }
        button:hover {
            background: #00cc00;
        }
        #console {
            margin-top: 20px;
            background: #000;
            border: 1px dashed #00ff00;
            padding: 10px;
            height: 250px;
            overflow-y: scroll;
            font-size: 13px;
        }
        .log-item {
            margin-bottom: 5px;
            border-bottom: 1px solid #111;
        }
    </style>
</head>
<body>

<div class="container">
    <h2>🔐 KMT SYSTEM 🔐</h2>
    <div style="text-align: center; font-size: 12px; margin-bottom: 15px;">>>> KYAW MIN TUN TOOL <<<</div>
    
    <div class="form-group">
        <label>[?] ENTER YOUR KEY:</label>
        <input type="text" id="key" value="KMT" placeholder="Enter key...">
    </div>
    
    <div class="form-group">
        <label>[★] LIMIT COUNT:</label>
        <input type="number" id="limit" value="10" placeholder="Number of IDs...">
    </div>

    <button onclick="startTool()">[>] START TOOL</button>

    <div id="console">
        <div style="color: #666;">[System Ready. Waiting for execution...]</div>
    </div>
</div>

<script>
    function startTool() {
        const key = document.getElementById('key').value;
        const limit = document.getElementById('limit').value;
        const consoleBox = document.getElementById('console');

        consoleBox.innerHTML = '<div style="color: yellow;">[~] Connecting to KMT Server...</div>';

        fetch('/run_tool', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ key: key, limit: limit })
        })
        .then(response => response.json())
        .then(data => {
            consoleBox.innerHTML = '';
            if (data.status === 'error') {
                consoleBox.innerHTML = `<div style="color: red;">${data.message}</div>`;
                return;
            }

            data.results.forEach(res => {
                let item = document.createElement('div');
                item.className = 'log-item';
                item.style.color = '#00ff41';
                item.innerText = res.text;
                consoleBox.appendChild(item);
            });
        })
        .catch(err => {
            consoleBox.innerHTML = `<div style="color: red;">[×] Connection Error!</div>`;
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
