import json
from datetime import datetime, timezone

from .database import connect

RULES = [
    {
        "id": "SOC-EDR-001",
        "title": "Encoded PowerShell from Office application",
        "severity": "critical",
        "match": lambda e: e["source"] == "crowdstrike" and
        e["event_type"] == "ProcessRollup2" and
        "powershell" in e.get("process_name", "").lower() and
        any(x in e.get("command_line", "").lower() for x in ("-enc", "frombase64string")) and
        e.get("parent_process", "").lower() in {"winword.exe", "excel.exe", "outlook.exe"},
    },
    {
        "id": "SOC-EDR-002",
        "title": "Credential dumping behavior",
        "severity": "critical",
        "match": lambda e: e["source"] == "crowdstrike" and
        ("lsass" in e.get("command_line", "").lower() or e.get("technique") == "T1003.001"),
    },
    {
        "id": "SOC-EDR-003",
        "title": "Suspicious child process from web browser",
        "severity": "high",
        "match": lambda e: e["source"] == "crowdstrike" and
        e.get("parent_process", "").lower() in {"chrome.exe", "msedge.exe", "firefox.exe"} and
        e.get("process_name", "").lower() in {"cmd.exe", "powershell.exe", "wscript.exe"},
    },
    {
        "id": "SOC-EMAIL-001",
        "title": "Proofpoint credential phishing delivered",
        "severity": "high",
        "match": lambda e: e["source"] == "proofpoint" and
        e.get("threat_type") == "credential_phishing" and e.get("delivery_status") == "delivered",
    },
    {
        "id": "SOC-CLOUD-001",
        "title": "Wiz public cloud exposure with critical finding",
        "severity": "critical",
        "match": lambda e: e["source"] == "wiz" and e.get("exposure") == "public" and
        e["severity"] == "critical",
    },
    {
        "id": "SOC-NET-001",
        "title": "Zscaler malware callback blocked",
        "severity": "high",
        "match": lambda e: e["source"] == "zscaler" and e.get("action") == "blocked" and
        e.get("threat_category") == "malware_callback",
    },
]


def run_detections():
    created = 0
    now = datetime.now(timezone.utc).isoformat()
    with connect() as db:
        for row in db.execute("SELECT id, raw_json FROM events"):
            event = json.loads(row["raw_json"])
            for rule in RULES:
                if not rule["match"](event):
                    continue
                cursor = db.execute(
                    """INSERT OR IGNORE INTO alerts
                    (rule_id, title, severity, event_id, created_at) VALUES (?, ?, ?, ?, ?)""",
                    (rule["id"], rule["title"], rule["severity"], row["id"], now),
                )
                created += cursor.rowcount
    return created

