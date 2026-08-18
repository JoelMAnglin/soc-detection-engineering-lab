import json
from urllib.request import urlopen

with urlopen("http://127.0.0.1:8080/api/health", timeout=2) as response:
    payload = json.load(response)
    if response.status != 200 or payload.get("status") != "healthy":
        raise SystemExit(1)

