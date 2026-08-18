# Detection catalog

| Rule | Data source | Severity | MITRE | Tuning intent |
|---|---|---:|---|---|
| SOC-EDR-001 | CrowdStrike process | Critical | T1059.001 | Require Office parent plus encoded/decode behavior |
| SOC-EDR-002 | CrowdStrike process | Critical | T1003.001 | Review approved credential tools and IR accounts |
| SOC-EDR-003 | CrowdStrike process | High | T1059.003 | Allow documented browser automation only |
| SOC-EMAIL-001 | Proofpoint message | High | T1566.002 | Require delivery; exclude quarantine-only messages |
| SOC-CLOUD-001 | Wiz cloud issue | Critical | T1530 | Require public exposure and critical severity |
| SOC-NET-001 | Zscaler web | High | T1071.001 | Require malware-callback classification and block action |

## Detection lifecycle

Every change should include a hypothesis, data prerequisites, positive test, benign test, MITRE mapping, severity rationale, query/runbook, tuning constraints, owner, review date, and measurable precision/recall proxy.

## SPL notes

SPL queries use concrete example indexes and sourcetypes. Adapt them to your authorized environment's CIM, data model, field normalization, and acceleration strategy. For Splunk ES, package searches as correlation searches with risk objects, throttling, adaptive response permissions, and analyst runbooks.

