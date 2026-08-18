import json
import os
import sqlite3
from pathlib import Path

DB_PATH = Path(os.environ.get("SOC_DB_PATH", "soc.db"))

SCHEMA = """
CREATE TABLE IF NOT EXISTS events (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  timestamp TEXT NOT NULL,
  source TEXT NOT NULL,
  event_type TEXT NOT NULL,
  severity TEXT NOT NULL,
  host TEXT,
  user TEXT,
  technique TEXT,
  summary TEXT NOT NULL,
  raw_json TEXT NOT NULL
);
CREATE TABLE IF NOT EXISTS alerts (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  rule_id TEXT NOT NULL,
  title TEXT NOT NULL,
  severity TEXT NOT NULL,
  event_id INTEGER NOT NULL,
  status TEXT NOT NULL DEFAULT 'new',
  disposition TEXT NOT NULL DEFAULT 'undetermined',
  analyst_notes TEXT NOT NULL DEFAULT '',
  created_at TEXT NOT NULL,
  UNIQUE(rule_id, event_id),
  FOREIGN KEY(event_id) REFERENCES events(id)
);
CREATE TABLE IF NOT EXISTS incidents (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  title TEXT NOT NULL,
  severity TEXT NOT NULL,
  status TEXT NOT NULL,
  owner TEXT NOT NULL,
  alert_ids TEXT NOT NULL,
  timeline TEXT NOT NULL,
  created_at TEXT NOT NULL
);
"""


def connect():
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    connection = sqlite3.connect(DB_PATH)
    connection.row_factory = sqlite3.Row
    connection.execute("PRAGMA foreign_keys=ON")
    return connection


def initialize():
    with connect() as db:
        db.executescript(SCHEMA)


def load_events(dataset_path):
    with connect() as db:
        if db.execute("SELECT COUNT(*) FROM events").fetchone()[0]:
            return 0
        count = 0
        with open(dataset_path, encoding="utf-8") as handle:
            for line in handle:
                if not line.strip():
                    continue
                event = json.loads(line)
                db.execute(
                    """INSERT INTO events
                    (timestamp, source, event_type, severity, host, user, technique, summary, raw_json)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)""",
                    (
                        event["timestamp"], event["source"], event["event_type"],
                        event["severity"], event.get("host"), event.get("user"),
                        event.get("technique"), event["summary"], json.dumps(event),
                    ),
                )
                count += 1
        return count
