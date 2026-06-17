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

All `/admin/*` endpoints require the `X-Admin-API-Key` header.

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

## Future admin dashboard

A future admin dashboard can use these endpoints to render:

```text
API status
Database readiness
Scheduler configuration
Notification configuration
Latest monitoring run status
Latest counts for notices, matches and notifications
Manual run button
Monitoring history table
```

The admin frontend must not hardcode `ADMIN_API_KEY` into public JavaScript.
For an MVP internal dashboard, the key can be entered by the operator and stored
in `sessionStorage` for the browser session.
