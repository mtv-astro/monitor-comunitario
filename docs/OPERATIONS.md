# Operations

## Overview

The project exposes a small set of operational endpoints for deployment checks,
readiness checks, and protected admin diagnostics.

These endpoints are intentionally simple and frontend-friendly so they can later
be consumed by an internal admin dashboard.

## Public endpoints

### `GET /health`

Liveness check. It only confirms that the API process is responding.

Example response:

```json
{
  "status": "ok",
  "environment": "production",
  "timezone": "America/Sao_Paulo"
}
```

### `GET /ready`

Readiness check. It verifies that the API can execute a minimal database query.

Successful response:

```json
{
  "status": "ready",
  "database": "ok"
}
```

If the database is unavailable, the endpoint returns `503 Service Unavailable`:

```json
{
  "status": "not_ready",
  "database": "error"
}
```

## Protected admin endpoints

All `/admin/*` API endpoints require the `X-Admin-API-Key` header.

```http
X-Admin-API-Key: <strong-admin-api-key>
```

The expected value is configured through:

```env
ADMIN_API_KEY=<strong-admin-api-key>
```

### `GET /admin/diagnostics`

Returns operational metadata for admin usage.

Example response:

```json
{
  "status": "ok",
  "environment": "production",
  "timezone": "America/Sao_Paulo",
  "database": {
    "status": "ok"
  },
  "scheduler": {
    "enabled": true,
    "hour": 6,
    "minute": 0
  },
  "notifications": {
    "provider": "app",
    "evolution_enabled": false
  },
  "latest_run": null
}
```

When monitoring runs exist, `latest_run` contains the most recent run metrics.

### `GET /admin/runs/latest`

Returns the most recent monitoring run or `null` if no run exists yet.

### `GET /admin/runs`

Lists recent monitoring runs.

### `POST /admin/runs/manual`

Triggers a synchronous manual monitoring cycle for MVP/admin usage.

## Admin diagnostics dashboard

The project serves a simple internal admin dashboard at:

```text
/admin
```

The dashboard is intentionally not linked from the public homepage. It is meant
for direct internal access by the operator.

The page itself is public static HTML, but protected data requests still require
`ADMIN_API_KEY`. The key is not hardcoded into JavaScript. The operator enters it
manually in the browser, and the frontend stores it only in `sessionStorage` for
the current browser session.

The dashboard sends protected requests with:

```http
X-Admin-API-Key: <strong-admin-api-key>
```

The dashboard consumes:

```text
GET /health
GET /ready
GET /admin/diagnostics
GET /admin/runs/latest
GET /admin/runs?limit=10
POST /admin/runs/manual
```

It renders:

```text
API status
Database readiness
Scheduler configuration
Notification configuration
Latest monitoring run status
Latest counts for notices, users, matches and notifications
Manual run button
Monitoring history table
```

### Local usage

Start the API:

```powershell
uv run uvicorn monitor_comunitario.api.main:app --reload
```

Open:

```text
http://127.0.0.1:8000/admin
```

Set `ADMIN_API_KEY` in `.env` or in the process environment before using the
protected dashboard actions.

For local manual testing:

```env
ADMIN_API_KEY=change-me-local-admin-key
```

Do not commit real admin keys.
