# Monitor Comunitário — Celesc Outage Watcher

Monitor público e independente para acompanhar avisos de desligamentos programados da Celesc e gerar alertas por endereço.

> Este projeto não é afiliado à Celesc. As informações são obtidas a partir de dados públicos disponíveis no site oficial da distribuidora. A programação pode sofrer alteração ou cancelamento pela própria Celesc.

## Por que este projeto existe

A Celesc já disponibiliza consulta pública de desligamentos programados e informa que envia avisos por e-mail/SMS aos clientes com cadastro atualizado. Porém, na prática, o aviso oficial depende do vínculo cadastral com a unidade consumidora, dos dados do titular e da atualização correta do cadastro.

Isso pode deixar de fora pessoas que moram em imóveis alugados, moradias temporárias, contratos informais, imóveis em nome de terceiros, casas divididas, pequenos negócios ou pessoas que simplesmente não conseguem lidar com o fluxo de atualização cadastral.

O Monitor Comunitário propõe uma camada simples de acesso à informação pública: o usuário cadastra município, bairro, rua e WhatsApp, e o sistema avisa quando houver um desligamento programado potencialmente relacionado ao endereço informado.

## O que o MVP faz

- Monitora a página pública de desligamentos programados da Celesc.
- Roda automaticamente 1x ao dia, às 06:00, no fuso America/Sao_Paulo.
- Permite cadastro de usuários e endereços.
- Normaliza municípios, bairros e ruas.
- Compara avisos públicos com os endereços cadastrados.
- Gera notificações in-app durante o desenvolvimento.
- Deixa o provider Evolution API preparado, mas desligado por padrão.
- Mantém logs e snapshots para auditoria do scraper.
- Expõe API FastAPI e comandos CLI para desenvolvimento.

## Stack

- Python 3.12+
- FastAPI
- Typer CLI
- Playwright
- PostgreSQL em produção
- SQLite somente para desenvolvimento rápido
- SQLAlchemy 2 + Alembic
- APScheduler no worker
- httpx
- Pydantic Settings
- RapidFuzz
- Docker + docker-compose
- Ruff, Mypy, Pytest, Pre-commit
- GitHub Actions
- GitHub CLI

## Estrutura

```text
monitor-comunitario/
├── .github/workflows/ci.yml
├── docs/
│   ├── PRD.md
│   ├── ARCHITECTURE.md
│   ├── ADR-001-stack.md
│   ├── DEVELOPMENT.md
│   └── COMMIT_PLAN.md
├── scripts/
│   ├── install.ps1
│   └── bootstrap_github.ps1
├── src/monitor_comunitario/
│   ├── api/
│   ├── cli.py
│   ├── core/
│   ├── db/
│   ├── matcher/
│   ├── notifications/
│   ├── scraper/
│   ├── services/
│   └── worker/
├── tests/
├── .env.example
├── .gitignore
├── .pre-commit-config.yaml
├── docker-compose.yml
├── Dockerfile
├── Makefile
└── pyproject.toml
```

## Instalação rápida no Windows

Extraia este pacote `.zip`, abra o PowerShell na pasta extraída e rode:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.\scripts\install.ps1
```

Por padrão, o script cria e instala o projeto em:

```powershell
C:\Users\carlo\projects\monitor-comunitario
```

Para forçar sobrescrita em uma pasta já existente:

```powershell
.\scripts\install.ps1 -Force
```

Para pular a instalação do Chromium do Playwright:

```powershell
.\scripts\install.ps1 -SkipPlaywright
```

## Criar repositório com GitHub CLI

Depois da instalação:

```powershell
cd C:\Users\carlo\projects\monitor-comunitario
.\scripts\bootstrap_github.ps1
```

O script verifica `gh auth status`, inicializa Git, cria o primeiro commit e cria o repositório público no GitHub.

## Rodar local

```powershell
cd C:\Users\carlo\projects\monitor-comunitario
uv run uvicorn monitor_comunitario.api.main:app --reload
```

Healthcheck:

```text
GET http://127.0.0.1:8000/health
```

CLI:

```powershell
uv run monitor-comunitario doctor
```



## Recriar o repositório no GitHub com autor correto

Se o primeiro commit apareceu com outro contribuidor, como Codex, recrie o histórico local e o repositório remoto:

```powershell
cd C:\Users\carlo\projects\monitor-comunitario
gh auth refresh -s delete_repo
.\scripts\reset_and_recreate_github.ps1 -DeleteRemote
```

O script:

- remove o `.git` local;
- configura `user.name` como `Carlos Selva`;
- configura `user.email` como `carlostselva@gmail.com`;
- cria um commit limpo com `--author`;
- apaga o repositório remoto se `-DeleteRemote` for usado;
- recria o repositório com `gh repo create`;
- faz push para `main`.

## UTF-8 e acentuação

Este pacote inclui:

- `.editorconfig`;
- `.gitattributes`;
- scripts PowerShell salvos com UTF-8 BOM;
- configuração de console UTF-8 nos scripts.

Isso reduz problemas de caracteres quebrados no Windows PowerShell e no GitHub.

## Desenvolvimento

Consulte:

- `docs/PRD.md`
- `docs/ARCHITECTURE.md`
- `docs/DEVELOPMENT.md`
- `docs/COMMIT_PLAN.md`

## Limitações conhecidas

- O projeto trabalha com dados públicos e não consulta dados privados da unidade consumidora.
- O matching por endereço é probabilístico e pode gerar falso positivo ou falso negativo.
- O envio por WhatsApp via Evolution API fica desativado até existir instância conectada.
- O scraper pode precisar de ajuste caso a Celesc altere a página.
