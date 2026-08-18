# CrowdStrike-compatible validation

## What is validated

- Falcon-style endpoint identity (`aid`) and `event_simpleName` fields;
- `ProcessRollup2`-style process, parent, command-line, user, host, and hash context;
- process ancestry detections and MITRE mappings;
- positive and benign PowerShell cases;
- credential-dumping and browser-child-process alerts;
- source-health counts in the dashboard;
- live API and container health through `scripts/validate_lab.py`.

## What is not claimed

- no CrowdStrike tenant was accessed;
- no Falcon API credential was created or transmitted;
- no sensor was installed;
- no proprietary event export was copied;
- no RTR, containment, or remediation command was executed;
- no vendor certification or endorsement is implied.

## How to validate against an authorized tenant later

1. Obtain written authorization and a least-privilege API client.
2. Store credentials in a secret manager or ignored `.env`, never Git.
3. Export a minimal, redacted sample from the tenant's supported API.
4. Compare actual field names/types with `data/events.jsonl` and document version/provenance.
5. Run detections read-only and compare results with Falcon console investigations.
6. Have a Falcon-qualified analyst review false positives/negatives.
7. Enable response actions only through a separately approved change workflow.

