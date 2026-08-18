# Troubleshooting

## Docker client works but server is unavailable

Symptom: `failed to connect to the docker API` or no server section in `docker version`.

Cause: Docker Desktop is installed but its engine is stopped. Start Docker Desktop, wait for “Engine running,” then retry.

## Port 8080 is already allocated

Find the owner:

```powershell
Get-NetTCPConnection -LocalPort 8080 -State Listen
```

Stop the known service or change the host side in `compose.yaml`, for example `8081:8080`, and browse to port 8081.

## Container is unhealthy

```powershell
docker compose ps
docker compose logs --tail 100 soc-lab
docker inspect soc-detection-lab --format '{{json .State.Health}}'
```

Reset only this lab:

```powershell
docker compose down -v
docker compose up --build --wait
```

## Dashboard loads but metrics remain dashes

Open `http://localhost:8080/api/metrics`. If it fails, review container logs. Hard-refresh the dashboard with `Ctrl+Shift+R` after the API is healthy.

## Validation script cannot connect

Run it only after `docker compose up --build --wait`. Confirm the health endpoint:

```powershell
Invoke-RestMethod http://localhost:8080/api/health
```

## Alerts are duplicated or missing

Alerts are unique per rule/event. Reset the named volume to reload pristine fixtures: `docker compose down -v`. Do not delete unrelated Docker volumes.

## JSON fixture parsing fails

Current versions ignore blank lines in JSONL exports. For other parsing errors, validate that every non-empty line is one complete JSON object and check the line reported in `docker compose logs soc-lab`.

## PowerShell script execution is blocked

Do not weaken machine-wide policy. Run the script for this process only if organizational policy permits:

```powershell
powershell -ExecutionPolicy Bypass -File .\scripts\export_incident.ps1 -AlertId 1
```

## Real CrowdStrike events do not match

This lab uses synthetic schema-shaped data. Vendor fields vary by API, export, and version. Follow the tenant-validation steps in `CROWDSTRIKE_VALIDATION.md`; do not paste credentials or raw sensitive telemetry into an issue.
