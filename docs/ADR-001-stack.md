# ADR-001 — Stack inicial do projeto

Data: 2026-06-16  
Status: Aceita

## Contexto

O projeto precisa ser simples o suficiente para um MVP, mas bem estruturado para portfólio GitHub. Ele precisa demonstrar produto, scraping responsável, API backend, worker agendado, matching textual, notificações e documentação.

## Decisão

Usaremos:

- Python 3.12+
- FastAPI
- Typer CLI
- Playwright
- SQLAlchemy 2
- Alembic
- PostgreSQL em produção
- SQLite para desenvolvimento rápido
- APScheduler no worker
- httpx
- Pydantic Settings
- RapidFuzz
- Docker e docker-compose
- Ruff, Mypy, Pytest
- Pre-commit
- GitHub Actions
- GitHub CLI

## Consequências positivas

- FastAPI gera documentação automática.
- Typer facilita comandos de desenvolvimento.
- Playwright lida melhor com página dinâmica.
- Worker separado evita duplicação de job dentro do processo web.
- PostgreSQL prepara o projeto para produção.
- SQLite reduz fricção local.
- RapidFuzz melhora matching aproximado.
- Docker facilita deploy.
- GitHub Actions melhora apresentação de portfólio.

## Consequências negativas

- Playwright deixa a instalação mais pesada.
- Ter API + worker é mais estrutura que um script cron simples.
- Alembic adiciona curva de aprendizado.
- Evolution API exigirá cuidado com credenciais e instância conectada.

## Alternativas consideradas

### Script Python + cron

Mais simples, mas pobre como portfólio e menos preparado para cadastro, histórico e notificações.

### Celery + Redis

Mais robusto, mas exagerado para MVP. Pode ser avaliado depois se houver fila real de mensagens.

### GitHub Actions como scheduler

Útil para protótipo, mas ruim para estado persistente e scraping com Playwright em ambiente controlado.

### Supabase Edge Functions

Interessante se o produto virar full Supabase, mas Playwright e scraping ficam menos naturais em edge runtime.

## Decisão final

Começar com FastAPI + worker separado + Playwright + banco relacional, com Evolution API preparada por feature flag.
