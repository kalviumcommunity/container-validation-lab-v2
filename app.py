"""incident-api: lists incidents from a JSON data file. Standard library only."""
import json
import os
import sys
from http.server import BaseHTTPRequestHandler, HTTPServer

VERSION = "1.1"
DATA_FILE = os.environ.get("DATA_FILE")


def load_incidents():
    with open(DATA_FILE) as handle:
        return json.load(handle)


class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/health":
            body = {"status": "ok"}
        elif self.path == "/version":
            body = {"version": VERSION}
        elif self.path == "/incidents":
            try:
                body = {"incidents": load_incidents()}
            except Exception as error:
                print(f"ERROR reading {DATA_FILE}: {error}", flush=True)
                self.send_error(500, "cannot read incident data")
                return
        else:
            self.send_error(404)
            return
        data = (json.dumps(body) + "\n").encode()
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(data)))
        self.end_headers()
        self.wfile.write(data)

    def log_message(self, fmt, *args):
        print(f"request {self.command} {self.path}", flush=True)


if __name__ == "__main__":
    if not DATA_FILE:
        print("ERROR: DATA_FILE is not set (expected /app/data/incidents.json)", flush=True)
        sys.exit(1)
    print(f"incident-api {VERSION} using data file {DATA_FILE}", flush=True)
    print("incident-api listening on 0.0.0.0:8080", flush=True)
    HTTPServer(("0.0.0.0", 8080), Handler).serve_forever()
