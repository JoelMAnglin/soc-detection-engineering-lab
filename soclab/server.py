import json
import mimetypes
import os
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import urlparse

from .database import connect, initialize, load_events
from .detections import RULES, run_detections

ROOT = Path(__file__).resolve().parent.parent
WEB = ROOT / "web"


def rows(query, parameters=()):
    with connect() as db:
        return [dict(item) for item in db.execute(query, parameters).fetchall()]


class Handler(BaseHTTPRequestHandler):
    def log_message(self, fmt, *args):
        print(f"http {self.client_address[0]} {fmt % args}")

    def json_response(self, payload, status=200):
        body = json.dumps(payload, indent=2).encode()
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        self.wfile.write(body)

    def serve_file(self, path):
        target = WEB / ("index.html" if path == "/" else path.lstrip("/"))
        if not target.is_file() or WEB not in target.resolve().parents:
            self.send_error(404)
            return
        body = target.read_bytes()
        self.send_response(200)
        self.send_header("Content-Type", mimetypes.guess_type(target)[0] or "application/octet-stream")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self):
        path = urlparse(self.path).path
        if path == "/api/health":
            self.json_response({"status": "healthy", "mode": os.getenv("SOC_MODE", "synthetic")})
        elif path == "/api/metrics":
            self.json_response(self.metrics())
        elif path == "/api/alerts":
            self.json_response(rows("""SELECT a.*, e.timestamp, e.source, e.host, e.user,
                e.technique, e.summary FROM alerts a JOIN events e ON e.id=a.event_id
                ORDER BY CASE a.severity WHEN 'critical' THEN 1 WHEN 'high' THEN 2 ELSE 3 END, a.id"""))
        elif path == "/api/events":
            self.json_response(rows("SELECT * FROM events ORDER BY timestamp DESC LIMIT 100"))
        elif path == "/api/detections":
            self.json_response([{k: v for k, v in rule.items() if k != "match"} for rule in RULES])
        else:
            self.serve_file(path)

    @staticmethod
    def metrics():
        with connect() as db:
            total_events = db.execute("SELECT COUNT(*) FROM events").fetchone()[0]
            total_alerts = db.execute("SELECT COUNT(*) FROM alerts").fetchone()[0]
            critical = db.execute("SELECT COUNT(*) FROM alerts WHERE severity='critical'").fetchone()[0]
            sources = [dict(x) for x in db.execute(
                "SELECT source, COUNT(*) AS count FROM events GROUP BY source ORDER BY count DESC"
            )]
            techniques = [dict(x) for x in db.execute(
                """SELECT COALESCE(technique, 'Unmapped') AS technique, COUNT(*) AS count
                FROM events GROUP BY technique ORDER BY count DESC"""
            )]
        return {
            "events": total_events,
            "alerts": total_alerts,
            "critical": critical,
            "detection_rate": round(total_alerts / total_events * 100, 1) if total_events else 0,
            "sources": sources,
            "techniques": techniques,
        }


def main():
    initialize()
    dataset = os.environ.get("SOC_DATASET_PATH", str(ROOT / "data" / "events.jsonl"))
    loaded = load_events(dataset)
    alerts = run_detections()
    print(f"SOC lab ready: loaded={loaded} alerts_created={alerts}")
    server = ThreadingHTTPServer(("0.0.0.0", 8080), Handler)
    print("Dashboard: http://localhost:8080")
    server.serve_forever()

