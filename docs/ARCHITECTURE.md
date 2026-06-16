# Arquitetura — Monitor Comunitário Celesc

## 1. Visão geral

A arquitetura separa API, worker, scraper, matcher e providers de notificação. Essa separação evita que o agendamento diário rode dentro do processo web e facilita testes, manutenção e deploy.

```text
Usuário/Admin
    ↓
FastAPI
    ↓
Banco de dados
    ↑
Worker diário 06:00
    ↓
Scraper Playwright
    ↓
Parser de avisos
    ↓
Matcher de endereços
    ↓
Notification Provider
    ├── In-app
    └── Evolution API futura
```

## 2. Componentes

### API

Responsável por healthcheck, cadastro de usuários, consulta de notificações, execução manual admin e documentação Swagger/OpenAPI.

### Worker

Responsável pelo job diário, timezone, scraper, parser, matcher, notificações e logs de execução.

### Scraper

Responsável por abrir a página pública da Celesc, lidar com conteúdo dinâmico, salvar snapshot bruto e retornar conteúdo para parsing.

### Parser

Responsável por transformar o conteúdo bruto em objetos estruturados de aviso.

### Matcher

Responsável por comparar avisos com usuários e produzir nível de match, score, motivo legível e decisão de notificar.

### Notifications

Camada de abstração para envio/criação de notificações:

- `AppNotificationProvider`;
- `EvolutionNotificationProvider`;
- `ConsoleNotificationProvider`, opcional para testes.

## 3. Processos

### Execução diária

```text
06:00 America/Sao_Paulo
    ↓
worker inicia run
    ↓
scraper captura página
    ↓
parser extrai avisos
    ↓
banco salva avisos novos
    ↓
matcher avalia usuários ativos
    ↓
notificações são criadas
    ↓
run é finalizada com métricas
```

### Execução manual

```text
POST /admin/runs/manual
ou
monitor-comunitario run-once
```

Executa o mesmo fluxo do worker, mas com logs explícitos para desenvolvimento.

## 4. Decisão: worker separado

Não rodar o scheduler dentro do mesmo processo do Uvicorn no deploy.

Motivo:

- reload local pode duplicar jobs;
- múltiplas réplicas podem executar o mesmo agendamento;
- worker separado facilita logs e escala;
- API e job têm ciclos de vida diferentes.

## 5. Banco

### Desenvolvimento

SQLite pode ser usado para instalação rápida local.

### Produção

PostgreSQL é recomendado.

Se o projeto já estiver em ecossistema Supabase, o Postgres do Supabase pode ser usado desde o início.

## 6. Idempotência

O sistema deve gerar um `content_hash` para cada aviso com base em:

- município;
- data/hora;
- descrição;
- área afetada;
- URL de origem.

Notificações devem ter restrição lógica:

```text
user_id + outage_notice_id + channel
```

Assim, reexecutar o job não duplica alerta.

## 7. Observabilidade

Cada run deve registrar status, duração, avisos encontrados, usuários avaliados, matches, notificações criadas, falhas e caminho do snapshot.

## 8. Estrutura de código

```text
src/monitor_comunitario/
├── api/
│   └── main.py
├── cli.py
├── core/
│   ├── config.py
│   └── logging.py
├── db/
│   ├── models.py
│   └── session.py
├── matcher/
│   ├── normalizer.py
│   └── scoring.py
├── notifications/
│   ├── base.py
│   ├── app_provider.py
│   └── evolution_provider.py
├── scraper/
│   ├── celesc_page.py
│   └── parser.py
├── services/
│   └── monitoring_service.py
└── worker/
    └── scheduler.py
```

## 9. Limites técnicos

- Playwright aumenta o peso do container.
- A página pode mudar.
- O matching textual não garante cobertura perfeita.
- O provider Evolution deve ser tratado como integração externa e falível.
