#!/usr/bin/env python3
"""Run Swish Tracker locally - no Netlify needed.

  python3 serve.py            -> http://localhost:8000  (camera works on this computer)
  python3 serve.py --https    -> https://<your-LAN-IP>:8443  (for iPhone camera on same Wi-Fi)

--https creates a self-signed certificate (needs `openssl`). On the iPhone you'll
see a certificate warning: tap Show Details > visit this website.
"""
import http.server, os, socket, ssl, subprocess, sys

ROOT = os.path.dirname(os.path.abspath(__file__))
os.chdir(ROOT)

def lan_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(("8.8.8.8", 80)); return s.getsockname()[0]
    except Exception:
        return "127.0.0.1"
    finally:
        s.close()

class Handler(http.server.SimpleHTTPRequestHandler):
    def end_headers(self):
        self.send_header("Cache-Control", "no-store")
        super().end_headers()

if "--https" in sys.argv:
    ip = lan_ip()
    cert, key = os.path.join(ROOT, ".cert.pem"), os.path.join(ROOT, ".key.pem")
    if not (os.path.exists(cert) and os.path.exists(key)):
        subprocess.check_call([
            "openssl", "req", "-x509", "-newkey", "rsa:2048", "-nodes", "-days", "365",
            "-keyout", key, "-out", cert, "-subj", "/CN=swish-tracker",
            "-addext", f"subjectAltName=DNS:localhost,IP:127.0.0.1,IP:{ip}"],
            stderr=subprocess.DEVNULL)
    port = 8443
    srv = http.server.ThreadingHTTPServer(("0.0.0.0", port), Handler)
    ctx = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
    ctx.load_cert_chain(cert, key)
    srv.socket = ctx.wrap_socket(srv.socket, server_side=True)
    print(f"Open on your iPhone (same Wi-Fi): https://{ip}:{port}")
else:
    port = 8000
    srv = http.server.ThreadingHTTPServer(("127.0.0.1", port), Handler)
    print(f"Open: http://localhost:{port}")

print("Ctrl+C to stop")
try:
    srv.serve_forever()
except KeyboardInterrupt:
    pass
