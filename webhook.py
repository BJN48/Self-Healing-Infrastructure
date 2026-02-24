from http.server import BaseHTTPRequestHandler, HTTPServer
import subprocess
import json

PLAYBOOK_PATH = "/app/restart.yml"

class Handler(BaseHTTPRequestHandler):

    def do_POST(self):
        content_length = int(self.headers.get('Content-Length', 0))
        body = self.rfile.read(content_length)

        print("\n🔔 Alert received")

        try:
            data = json.loads(body.decode("utf-8"))
            print("Alert:", data.get("alerts", [{}])[0].get("status"))
        except:
            print("No JSON payload")

        try:
            result = subprocess.run(
                ["ansible-playbook", PLAYBOOK_PATH],
                capture_output=True,
                text=True
            )

            print(result.stdout)
            print(result.stderr)

            self.send_response(200)
            self.end_headers()
            self.wfile.write(b"Nginx restart triggered")

        except Exception as e:
            print("ERROR:", e)
            self.send_response(500)
            self.end_headers()
            self.wfile.write(b"Error running playbook")


HTTPServer(('', 5001), Handler).serve_forever()
