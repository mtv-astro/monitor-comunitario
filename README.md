# Monitor Comunitário — Celesc Outage Watcher

Monitor público e independente para acompanhar avisos de desligamentos programados da Celesc e gerar alertas por endereço.

> Este projeto não é afiliado à Celesc. As informações são obtidas exclusivamente a partir de dados públicos disponíveis no site oficial da distribuidora. A programação pode sofrer alteração, cancelamento ou erro de interpretação. A fonte oficial continua sendo a Celesc.

## Problema

A Celesc disponibiliza avisos públicos de desligamentos programados e pode enviar comunicados por e-mail/SMS aos clientes com cadastro atualizado.

Na prática, muitas pessoas afetadas por um desligamento não são necessariamente titulares da unidade consumidora ou não têm acesso fácil ao cadastro oficial. Isso inclui:

- moradores de imóveis alugados;
- contratos informais;
- casas compartilhadas;
- imóveis em nome de terceiros;
- pequenos negócios locais;
- pessoas que dependem de proprietário, imobiliária ou titular da conta.

O problema não é a falta de informação pública. O problema é a distância entre essa informação e quem precisa ser avisado.

## Solução

O Monitor Comunitário cria uma camada simples de acesso à informação pública.

O usuário cadastra voluntariamente seu município, bairro, rua e WhatsApp. O sistema consulta diariamente os avisos públicos da Celesc, compara os avisos com os endereços cadastrados e cria alertas quando houver possibilidade de impacto.

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
Notificação ao usuário
```

## Estado atual

Implementado:

- cadastro público de endereço;
- geração de código privado no cadastro;
- área do morador com acesso por telefone + código privado;
- notificações in-app;
- scraper Playwright para a página pública da Celesc;
- parser inicial dos avisos;
- persistência de avisos e snapshots;
- matching por município, bairro, rua e similaridade textual;
- painel admin interno;
- endpoints admin protegidos por `X-Admin-API-Key`;
- execução manual de monitoramento;
- worker diário preparado;
- migrations com Alembic;
- suporte a SQLite local e PostgreSQL em produção;
- Docker e docker-compose;
- CI com Ruff, Mypy e Pytest.

Em andamento / próximos passos:

- polimento da experiência pública, área do morador e painel admin;
- melhoria da leitura dos alertas longos;
- seletor de tema;
- seletor de idioma;
- endurecimento do hash do código privado;
- login tradicional com senha como evolução planejada;
- preparação para envio real via Evolution API;
- migração operacional para Postgres/Supabase em ambiente de demo/produção.

Fora do escopo atual:

- consulta de CPF, CNPJ ou unidade consumidora;
- acesso à Agência Web da Celesc;
- garantia de precisão por unidade consumidora;
- previsão de quedas emergenciais;
- substituição dos canais oficiais da Celesc;
- envio real de WhatsApp em produção sem instância validada;
- autenticação completa com recuperação de senha.

## Como funciona para o morador

1. O morador cadastra nome, telefone e endereço.
2. O sistema gera um código privado.
3. Esse código aparece apenas uma vez.
4. O morador guarda o código.
5. Depois, acessa `/member` com telefone + código privado.
6. Quando houver aviso público potencialmente relacionado ao endereço, o sistema exibe o alerta na área do morador.

A área do morador não é o painel admin.

```text
Morador:
telefone + código privado
/member
```

## Como funciona para o operador/admin

O operador acessa o painel interno em:

```text
/admin
```

O painel permite acompanhar:

- status da API;
- readiness do banco;
- configuração do scheduler;
- provider de notificação ativo;
- última execução de monitoramento;
- histórico de runs;
- execução manual do monitoramento.

O painel admin usa chave administrativa, não o código privado do morador.

```text
Admin:
ADMIN_API_KEY
/admin
```

Os dados protegidos do admin exigem o header:

```http
X-Admin-API-Key: <strong-admin-api-key>
```

A chave deve ser configurada via variável de ambiente:

```env
ADMIN_API_KEY=<strong-admin-api-key>
```

Nunca commite uma chave real.

## Rotas principais

Públicas:

```text
GET  /
GET  /member
GET  /health
GET  /ready
POST /users
POST /member/access
```

Admin protegidas:

```text
GET    /admin
GET    /admin/diagnostics
GET    /admin/runs
GET    /admin/runs/latest
GET    /admin/runs/{run_id}
POST   /admin/runs/manual

GET    /admin/users
GET    /admin/users/{user_id}
PATCH  /admin/users/{user_id}
DELETE /admin/users/{user_id}

GET    /admin/notifications
GET    /admin/users/{user_id}/notifications
PATCH  /admin/notifications/{notification_id}/read
```

As rotas `/admin/*` exigem `X-Admin-API-Key`.

## Stack

- Python 3.12+
- FastAPI
- Typer CLI
- Playwright
- SQLAlchemy 2
- Alembic
- PostgreSQL
- SQLite para desenvolvimento rápido
- APScheduler
- RapidFuzz
- Pydantic Settings
- httpx
- Docker / docker-compose
- Ruff
- Mypy
- Pytest
- GitHub Actions

## Estrutura principal

```text
monitor-comunitario/
├── .github/workflows/      # CI
├── alembic/                # migrations
├── docs/                   # documentação técnica e produto
├── scripts/                # scripts auxiliares
├── src/monitor_comunitario/
│   ├── api/                # FastAPI, rotas públicas, morador, admin e páginas web
│   ├── core/               # settings e logging
│   ├── db/                 # modelos, sessão e inicialização do banco
│   ├── matcher/            # normalização e pontuação de endereços
│   ├── notifications/      # providers de notificação
│   ├── scraper/            # captura e parser Celesc
│   ├── services/           # orquestração do monitoramento
│   └── worker/             # agendamento diário
├── tests/                  # testes automatizados
├── docker-compose.yml
├── Dockerfile
├── pyproject.toml
└── README.md
```

## Rodar localmente

Pré-requisitos:

- Python 3.12+
- Git
- PowerShell
- `uv`
- Chromium do Playwright

Instalação:

```powershell
python -m pip install --user uv
uv sync --dev
uv run playwright install chromium
cp .env.example .env
```

Rodar API local:

```powershell
uv run uvicorn monitor_comunitario.api.main:app --reload
```

Acessos locais:

```text
http://127.0.0.1:8000/
http://127.0.0.1:8000/member
http://127.0.0.1:8000/admin
http://127.0.0.1:8000/docs
http://127.0.0.1:8000/health
http://127.0.0.1:8000/ready
```

Para acessar o admin localmente:

```powershell
$env:ADMIN_API_KEY="change-me-local-admin-key"
uv run uvicorn monitor_comunitario.api.main:app --reload
```

Depois abra `/admin` e informe:

```text
change-me-local-admin-key
```

## CLI

Diagnóstico básico:

```powershell
uv run monitor-comunitario doctor
```

Executar monitoramento manual:

```powershell
uv run monitor-comunitario run-once
```

Executar scraping limitado para desenvolvimento:

```powershell
uv run monitor-comunitario run-once --limit 3
```

Iniciar worker agendado:

```powershell
uv run monitor-comunitario worker
```

## Banco de dados

O projeto suporta:

```text
1. SQLite local para desenvolvimento rápido/MVP
2. Postgres local via Docker Compose
3. Supabase/Postgres externo para demo/produção
```

SQLite é adequado para desenvolvimento local e MVP técnico. Para ambiente público, demo persistente ou produção, o caminho recomendado é PostgreSQL, preferencialmente Supabase/Postgres externo.

Aplicar migrations:

```powershell
uv run monitor-comunitario db-upgrade
```

Ver estado atual:

```powershell
uv run monitor-comunitario db-current
```

Criar nova migration:

```powershell
uv run monitor-comunitario db-revision "short migration message" --autogenerate
```

## Variáveis de ambiente principais

Copie o arquivo de exemplo:

```powershell
cp .env.example .env
```

Configurações importantes:

```env
APP_ENV=development
APP_TIMEZONE=America/Sao_Paulo

DATABASE_URL=sqlite:///./data/monitor_comunitario.db

ADMIN_API_KEY=change-me-local-admin-key

NOTIFICATION_PROVIDER=app
EVOLUTION_ENABLED=false
```

O provider Evolution existe, mas deve permanecer desligado até haver instância conectada e validação operacional.

## Docker

Subir ambiente com Docker:

```powershell
docker compose up --build
```

Use `.env.example` como referência. Não coloque segredos reais no `docker-compose.yml`.

## Segurança e privacidade

Este projeto:

- usa somente dados públicos;
- não consulta dados privados da unidade consumidora;
- não acessa CPF, CNPJ, titularidade ou Agência Web;
- não armazena credenciais da Celesc;
- não garante precisão absoluta do matching;
- não substitui os canais oficiais da distribuidora.

O matching por endereço é probabilístico e pode gerar falso positivo ou falso negativo.

As rotas sensíveis de usuários, notificações e operação ficam atrás de `X-Admin-API-Key`.

## Autenticação atual e roadmap

Modelo atual:

```text
Morador:
telefone + código privado

Admin:
ADMIN_API_KEY
```

Evolução planejada:

```text
telefone/e-mail + senha
recuperação de senha
papéis de usuário/admin
sessões mais robustas
```

Essa evolução deve ser feita em PR próprio, porque muda banco, telas, testes, fluxo de recuperação e política de autenticação.

## Validação

Antes de abrir PR, rode:

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

## Desenvolvimento

Fluxo recomendado:

```text
Issue → Branch → Implementação → Validação local → Commit → Push → PR → CI → Revisão → Merge
```

Padrão de branch:

```text
feat/scope-short-name
fix/scope-short-name
docs/scope-short-name
```

Padrão de commit:

```text
feat(scope): short description
fix(scope): short description
docs(scope): short description
```

Exemplo:

```powershell
git checkout main
git pull origin main
git checkout -b docs/readme-current-project-state

uv run ruff check .
uv run mypy src
uv run pytest

git add README.md
git commit -m "docs(readme): align README with current project state"
git push -u origin docs/readme-current-project-state
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
