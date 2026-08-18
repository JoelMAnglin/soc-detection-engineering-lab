param(
  [Parameter(Mandatory=$true)][int]$AlertId,
  [string]$ApiBase = "http://localhost:8080"
)

$alerts = Invoke-RestMethod "$ApiBase/api/alerts"
$alert = $alerts | Where-Object id -eq $AlertId
if (-not $alert) { throw "Alert $AlertId was not found." }

$report = [ordered]@{
  title = $alert.title
  severity = $alert.severity
  status = $alert.status
  source = $alert.source
  host = $alert.host
  user = $alert.user
  mitre_technique = $alert.technique
  summary = $alert.summary
  analyst_actions = @("Validate telemetry", "Scope affected identity and host", "Preserve evidence", "Escalate per severity matrix")
  generated_utc = (Get-Date).ToUniversalTime().ToString("o")
}

$output = "reports/alert-$AlertId-incident.json"
$report | ConvertTo-Json -Depth 4 | Set-Content -LiteralPath $output
Write-Host "Created $output"

