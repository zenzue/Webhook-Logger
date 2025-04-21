from flask import Flask, request, render_template_string
import datetime
import os

app = Flask(__name__)

os.makedirs("logs", exist_ok=True)
logfile = "logs/payloads.log"

HTML_TEMPLATE = '''
<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Webhook Log Viewer</title>
  <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css" rel="stylesheet">
  <meta http-equiv="refresh" content="5"> <!-- Auto-refresh every 5 seconds -->
  <style>
    body { background-color: #f8f9fa; padding-top: 20px; }
    .log-box {
      background: #212529;
      color: #f8f9fa;
      padding: 15px;
      border-radius: 8px;
      height: 600px;                /* Fixed height for scrolling */
      overflow-y: auto;             /* Vertical scroll */
      white-space: pre-wrap;
      word-wrap: break-word;
    }
    .container { max-width: 900px; }
    h1 { font-size: 2rem; margin-bottom: 1rem; }
  </style>
</head>
<body>
  <div class="container">
    <h1 class="text-center">📜 Webhook Log Viewer</h1>
    <p class="text-center text-muted">by <b>PentestSage</b></p>
    <div class="log-box">{{ logs }}</div>
  </div>
<script>
  const logBox = document.querySelector('.log-box');
  logBox.scrollTop = logBox.scrollHeight;
</script>
</body>
</html>
'''

@app.route('/', methods=['GET'])
def index():
    return "Webhook is live. POST to /log", 200

@app.route('/log', methods=['GET', 'POST'])
def log_data():
    data = request.get_data(as_text=True)
    ip = request.remote_addr
    timestamp = datetime.datetime.now().isoformat()

    log_entry = f"[{timestamp}] From {ip}:\n{data}\n{'-'*50}\n"

    print(log_entry)

    with open(logfile, "a") as f:
        f.write(log_entry)

    return "Logged.", 200

@app.route('/view')
def view_logs():
    if not os.path.exists(logfile):
        return "No logs yet."

    with open(logfile, 'r') as f:
        logs = f.read()

    return render_template_string(HTML_TEMPLATE, logs=logs)

@app.route('/favicon.ico')
def favicon():
    return '', 204

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)