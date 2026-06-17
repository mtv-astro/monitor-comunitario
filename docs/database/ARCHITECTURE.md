# Arquitetura de Banco de Dados

Este documento descreve a arquitetura de persistência do Monitor Comunitário.

## Camadas

O backend usa SQLAlchemy 2 para definir modelos e acesso ao banco. A camada de persistência é isolada em `monitor_comunitario/db`, permitindo que a aplicação seja executada com diferentes motores:

- **SQLite local** – facilitador de onboarding e desenvolvimento rápido. O arquivo fica em `./data/monitor_comunitario.db` e é criado automaticamente.
- **Postgres local via Docker Compose** – serviço de banco real usado em desenvolvimento robusto e testes de integração. A senha, usuário e porta são configurados em `.env.docker.example` e no `docker-compose.yml`.
- **Supabase/Postgres externo** – banco gerenciado para demonstrações públicas. Use `.env.supabase.example` para apontar a aplicação para sua instância Supabase.

## SQLAlchemy e Alembic

Os modelos são definidos em `db/models.py`. As migrations são gerenciadas pelo Alembic e ficam no diretório `migrations/`. Cada alteração no modelo deve gerar uma nova migration via:

```bash
uv run monitor-comunitario db-revision --message "descrição"
```

e aplicada com:

```bash
uv run monitor-comunitario db-upgrade
```

## Inicialização

- Em SQLite, a aplicação chama `Base.metadata.create_all()` ao iniciar (`init_db()`) para criar as tabelas, simplificando o setup.
- Em Postgres ou Supabase, as tabelas devem ser criadas via migrations. O `init_db()` só é usado em SQLite.

Consulte `docs/database/MIGRATIONS.md` para detalhes sobre criação e execução de migrations.
