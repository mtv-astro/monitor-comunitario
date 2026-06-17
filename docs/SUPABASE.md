# Supabase/Postgres profile

## Por que usar Supabase

Para portfólio, o projeto demonstra dois modos:

```text
Postgres local via Docker Compose
Supabase/Postgres gerenciado para produção/demo
```

Isso mostra tanto domínio de infraestrutura local quanto uso pragmático de banco gerenciado.

## Criar arquivo de ambiente

```powershell
Copy-Item .env.supabase.example .env.supabase
```

Edite:

```env
DATABASE_URL=postgresql+psycopg://postgres.<project-ref>:<password>@<host>:6543/postgres?sslmode=require
```

Não commite `.env.supabase`.

## Rodar migrations

```powershell
uv run monitor-comunitario db-upgrade
```

Ou via Docker:

```powershell
docker compose -f docker-compose.supabase.yml --env-file .env.supabase up --build
```

## Rodar API e worker com Supabase

```powershell
docker compose -f docker-compose.supabase.yml --env-file .env.supabase up -d --build
```

## Segurança

- não commitar connection string real;
- usar senha forte no banco;
- manter `EVOLUTION_API_KEY` fora do git;
- configurar backup e retenção no painel do provedor;
- revisar regras de acesso antes de produção real.
