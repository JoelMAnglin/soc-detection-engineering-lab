# Build and troubleshooting record

| Observation | Root cause | Action |
|---|---|---|
| Docker CLI installed but daemon unavailable | Docker Desktop engine was stopped | Started Docker Desktop and waited for the engine |
| Container initially restarted during fixture ingestion | JSONL input contained harmless blank lines that the loader tried to parse | Made ingestion whitespace-tolerant, reset only the lab volume, and reran validation |
| Commercial platforms requested but no authorized tenants supplied | Vendor validation requires licensed access and credentials | Used clearly disclosed synthetic schema-shaped telemetry; disabled live connectors |
| Job requires Splunk ES/Core but lab must incur no cost | Bundling Splunk would introduce licensing/terms and a heavy image | Supplied advanced SPL content and tests; kept Splunk execution optional and external |
| Dashboard needs repeatable evidence | Manual screenshots alone do not prove ingestion/detection | Added live health, metrics, alerts, and deterministic validation endpoints |

## Validation evidence

The final validation runs unit tests, SPL content checks, Compose configuration validation, a live container healthcheck, endpoint assertions, source assertions, and detection assertions. The running dashboard was also exercised in a browser: the Refresh control was clicked and the rendered state was checked for 12 events, 6 alerts, and the synthetic CrowdStrike disclosure. The repository screenshot is a 1584 x 1444 full-page capture from that live container.

## Cost record

Project software cost: **$0.00**. Docker Desktop eligibility depends on the user's organization and Docker subscription terms; this project does not purchase or activate a subscription. No commercial security API or cloud resource is enabled.
