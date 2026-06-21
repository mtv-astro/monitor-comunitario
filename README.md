# Monitor Comunitário — Celesc Outage Watcher

Monitor público e independente para acompanhar avisos de desligamentos programados da Celesc e gerar alertas por endereço.

> Este projeto não é afiliado à Celesc. As informações são obtidas a partir de dados públicos disponíveis no site oficial da distribuidora. A fonte oficial continua sendo a Celesc.

## Problema

A Celesc disponibiliza avisos públicos de desligamentos programados e pode enviar comunicados aos clientes com cadastro atualizado.

Na prática, muitas pessoas afetadas por um desligamento não são necessariamente titulares da unidade consumidora ou não têm acesso fácil ao cadastro oficial. O problema não é a falta de informação pública. O problema é a distância entre essa informação e quem precisa ser avisado.

## Solução

O Monitor Comunitário cria uma camada simples de acesso à informação pública.

O morador cadastra voluntariamente município, bairro, rua e telefone. O sistema consulta diariamente os avisos públicos da Celesc, compara os avisos com os endereços cadastrados e cria alertas quando houver possibilidade de impacto.

```text
Avisos públicos da Celesc
        ↓
Scraper diário
        ↓
Parser de avisos
        ↓
Banco de dados
        ↓
Matching por endereço
        ↓
Alerta ao morador
```

## Status do MVP

O projeto já possui cadastro público de endereço, área do morador com telefone + código privado, notificações in-app, scraper Celesc, parser inicial, matching por endereço, painel admin protegido, worker diário preparado, migrations, Docker e CI.

Ainda estão no roadmap: envio real por WhatsApp/Evolution API, login tradicional com senha, melhorias de leitura dos alertas, seletor de tema/idioma, Postgres/Supabase para demo ou produção e políticas finais de retenção e remoção de dados.

## Como funciona

### Morador

1. O morador cadastra nome, telefone e endereço.
2. O sistema gera um código privado.
3. Esse código aparece apenas uma vez.
4. O morador acessa `/member` com telefone + código privado.
5. Quando houver aviso público potencialmente relacionado ao endereço, o sistema exibe o alerta na área do morador.

A área do morador não é o painel admin.

### Operador/admin

O painel interno fica em `/admin` e usa `ADMIN_API_KEY`, não o código privado do morador.

As rotas protegidas exigem:

```http
X-Admin-API-Key: <strong-admin-api-key>
```

Detalhes completos das rotas públicas e administrativas estão em `docs/OPERATIONS.md`.

## Dados e privacidade

O projeto foi desenhado para minimizar coleta de dados.

O sistema consulta apenas avisos públicos divulgados pela Celesc. Ele não acessa sistemas privados da distribuidora, titularidade, histórico de consumo, faturas ou credenciais de acesso.

O cadastro do morador pode incluir nome, telefone ou WhatsApp, município, bairro, rua, número, CEP e preferência sobre alertas amplos por município.

Esses dados são usados para comparar o endereço cadastrado com avisos públicos e exibir possíveis alertas na área do morador.

O acesso do morador usa telefone + código privado. O código é exibido apenas uma vez no cadastro. A aplicação armazena uma versão derivada do código, não o código em texto puro.

As rotas sensíveis de usuários, notificações e operação ficam protegidas por `X-Admin-API-Key`.

No MVP, a desativação de cadastro preserva histórico operacional. Antes de produção, o projeto deve definir política de retenção, remoção de dados e consentimento para integrações externas.

## Stack

- Python 3.12+
- FastAPI
- Typer CLI
- Playwright
- SQLAlchemy 2 + Alembic
- SQLite local / PostgreSQL em produção
- APScheduler
- RapidFuzz
- Docker / docker-compose
- Ruff, Mypy e Pytest
- GitHub Actions

## Rodar localmente

```powershell
python -m pip install --user uv
uv sync --dev
uv run playwright install chromium
cp .env.example .env
uv run uvicorn monitor_comunitario.api.main:app --reload
```

Acessos locais:

```text
http://127.0.0.1:8000/
http://127.0.0.1:8000/member
http://127.0.0.1:8000/admin
http://127.0.0.1:8000/docs
```

Para acessar o admin localmente:

```powershell
$env:ADMIN_API_KEY="change-me-local-admin-key"
uv run uvicorn monitor_comunitario.api.main:app --reload
```

Depois abra `/admin` e informe a chave configurada.

## Banco de dados

O projeto suporta SQLite local para desenvolvimento rápido/MVP, Postgres local via Docker Compose e Supabase/Postgres externo para demo ou produção.

SQLite é adequado para desenvolvimento local e MVP técnico. Para ambiente público, demo persistente ou produção, o caminho recomendado é PostgreSQL.

Comandos principais:

```powershell
uv run monitor-comunitario db-upgrade
uv run monitor-comunitario db-current
```

## CLI

```powershell
uv run monitor-comunitario doctor
uv run monitor-comunitario run-once
uv run monitor-comunitario run-once --limit 3
uv run monitor-comunitario worker
```

## Validação

```powershell
uv run ruff check .
uv run mypy src
uv run pytest
```

Quando houver mudança de banco:

```powershell
uv run monitor-comunitario db-upgrade
uv run monitor-comunitario db-current
```

## Documentação

Consulte também:

- `docs/PRD.md`
- `docs/ARCHITECTURE.md`
- `docs/DEVELOPMENT.md`
- `docs/OPERATIONS.md`
- `docs/DATABASE.md`
- `docs/DEPLOYMENT.md`
- `docs/COMMIT_PLAN.md`

## Limitações conhecidas

- A página pública da Celesc pode mudar e quebrar o scraper.
- O matching textual não garante cobertura perfeita.
- O envio por WhatsApp via Evolution API está preparado, mas desligado por padrão.
- O sistema não cobre quedas emergenciais.
- A fonte oficial continua sendo a Celesc.
