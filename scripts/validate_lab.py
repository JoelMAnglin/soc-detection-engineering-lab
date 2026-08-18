import json
import sys
from urllib.request import urlopen

BASE = "http://127.0.0.1:8080"


def get(path):
    with urlopen(BASE + path, timeout=5) as response:
        assert response.status == 200
        return json.load(response)


health = get("/api/health")
metrics = get("/api/metrics")
alerts = get("/api/alerts")
detections = get("/api/detections")

checks = {
    "health": health["status"] == "healthy",
    "synthetic_mode_disclosed": health["mode"] == "synthetic",
    "crowdstrike_source_loaded": any(x["source"] == "crowdstrike" for x in metrics["sources"]),
    "proofpoint_source_loaded": any(x["source"] == "proofpoint" for x in metrics["sources"]),
    "critical_alerts_created": metrics["critical"] >= 3,
    "encoded_powershell_detected": any(x["rule_id"] == "SOC-EDR-001" for x in alerts),
    "credential_dumping_detected": any(x["rule_id"] == "SOC-EDR-002" for x in alerts),
    "email_phishing_detected": any(x["rule_id"] == "SOC-EMAIL-001" for x in alerts),
    "six_detection_rules_loaded": len(detections) == 6,
}

print(json.dumps({"checks": checks, "metrics": metrics}, indent=2))
if not all(checks.values()):
    sys.exit(1)

