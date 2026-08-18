# SOC analyst runbook

## Severity and escalation

| Severity | Target | Expected action |
|---|---:|---|
| Critical | 15 minutes | Validate, scope, contain recommendation, incident escalation |
| High | 30 minutes | Validate, enrich, owner notification, decide escalation |
| Medium | 4 hours | Contextualize, tune or assign |
| Informational | 1 business day | Review for baseline or telemetry quality |

## Triage workflow

1. Confirm the alert is supported by original telemetry.
2. Validate time, source, user, host, command, hash, and MITRE mapping.
3. Search for related events on the same endpoint, identity, sender, URL, or cloud resource.
4. Determine true positive, benign positive, false positive, or insufficient evidence.
5. Document scope, confidence, business impact, and recommended containment.
6. Escalate by SLA and preserve evidence.
7. Close only after independent remediation/validation evidence.

## Scenario: finance compromise chain

Start with `SOC-EDR-001`. The Word-to-encoded-PowerShell ancestry is unlikely for routine administration. Pivot to the same host and user; identify `SOC-EDR-002` LSASS access. Correlate the Proofpoint event for the same finance identity. Treat the combined signals as a likely phishing-to-credential-access incident.

Recommended actions: isolate the endpoint through an authorized EDR operator, disable/review the account through identity operations, revoke sessions, block the phishing infrastructure, preserve volatile evidence, and search peer hosts. This lab does not execute those actions.

## Alert tuning

Tune on stable context, not broad process names. The included benign PowerShell inventory event demonstrates why `powershell.exe` alone is too noisy. Preserve malicious parent/command combinations, log every exception, assign an owner, set an expiration, and measure false-negative risk.

## Shift handoff

Document active incident IDs, pending evidence, SLA deadlines, containment status, blocked actions, owners, and the next explicit analyst action. Avoid ambiguous notes such as “monitoring.”

