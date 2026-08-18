# Beginner setup

## 1. Install Docker Desktop

Download Docker Desktop for Windows or macOS. On Linux, install Docker Engine and the Compose plugin. Start Docker Desktop and wait until it reports that the engine is running.

Confirm:

```powershell
docker version
docker compose version
```

Both commands must show a server/engine version.

## 2. Download the lab

```powershell
git clone https://github.com/JoelMAnglin/soc-detection-engineering-lab.git
Set-Location soc-detection-engineering-lab
```

## 3. Run the lab

```powershell
docker compose up --build --wait
```

The first run downloads the free Python base image and builds the local container. No account or payment is required.

## 4. Validate

```powershell
python scripts/validate_lab.py
docker compose ps
```

All validation checks should be `true`; the container should be `healthy`.

## 5. Use the dashboard

Open `http://localhost:8080`. Review the critical alert queue, telemetry counts, MITRE coverage, and SPL example. Follow [the analyst runbook](ANALYST_RUNBOOK.md).

## 6. Export an incident

```powershell
.\scripts\export_incident.ps1 -AlertId 1
```

The safe local report appears under `reports/` and is ignored by Git.

## 7. Stop or reset

Stop while retaining data:

```powershell
docker compose down
```

Reset the synthetic database:

```powershell
docker compose down -v
```

