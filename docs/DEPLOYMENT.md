# Deployment — Docker Compose

## Visão geral

O projeto deve rodar em produção com processos separados:

```text
api      → FastAPI/Uvicorn
worker   → APScheduler diário às 06:00
postgres → banco relacional
```

A separação evita que o scheduler rode dentro do processo web e duplique execuções em cenários de reload ou múltiplas instâncias.

## Arquivos principais

```text
Dockerfile
docker-compose.yml
.env.docker.example
```

## Rodar local com Docker

```powershell
cd C:\Users\carlo\projects\monitor-comunitario

docker compose --env-file .env.docker.example up --build
```

Acessar:

```text
http://127.0.0.1:8000/health
http://127.0.0.1:8000/docs
```

## Logs

```powershell
docker compose --env-file .env.docker.example logs -f api
docker compose --env-file .env.docker.example logs -f worker
docker compose --env-file .env.docker.example logs -f postgres
```

## Parar

```powershell
docker compose --env-file .env.docker.example down
```

## Parar e apagar banco local Docker

Atenção: remove os dados do Postgres local.

```powershell
docker compose --env-file .env.docker.example down -v
```

## Variáveis principais

```env
DATABASE_URL=postgresql+psycopg://monitor:monitor@postgres:5432/monitor_comunitario
APP_TIMEZONE=America/Sao_Paulo
SCHEDULER_HOUR=6
SCHEDULER_MINUTE=0
SCRAPER_HEADLESS=true
SNAPSHOT_DIR=/app/snapshots
```

## Snapshots

Os snapshots ficam montados em volume bind:

```text
./snapshots:/app/snapshots
```

Isso permite auditar capturas mesmo depois de reiniciar containers.

## Evolution API

A integração WhatsApp continua desligada por padrão:

```env
NOTIFICATION_PROVIDER=app
EVOLUTION_ENABLED=false
```

Quando houver instância Evolution conectada, configurar:

```env
NOTIFICATION_PROVIDER=evolution
EVOLUTION_ENABLED=true
EVOLUTION_BASE_URL=
EVOLUTION_API_KEY=
EVOLUTION_INSTANCE=
```

## VPS

Em VPS, usar uma cópia real do `.env.docker.example`:

```bash
cp .env.docker.example .env.docker
```

Editar senhas e secrets antes de subir:

```bash
docker compose --env-file .env.docker up -d --build
```

## Próxima melhoria recomendada

Adicionar migrations Alembic antes de produção real. Hoje o app usa `Base.metadata.create_all` no startup para simplicidade do MVP.
