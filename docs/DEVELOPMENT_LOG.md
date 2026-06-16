# Development Log

## 2026-06-16 — feat(database-and-users)

Primeira fatia funcional:

- adiciona sessão de banco com SQLAlchemy;
- cria inicialização local com `Base.metadata.create_all`;
- adiciona schemas Pydantic para usuários;
- adiciona rotas CRUD de `/users`;
- mantém delete como desativação lógica;
- adiciona testes básicos com `TestClient`.

### Observação

Alembic será adicionado em etapa posterior de banco/migrations. Para esta fatia, a inicialização automática mantém o projeto simples para desenvolvimento local.

## 2026-06-16 — feat(celesc-scraper)

Segunda fatia funcional:

- adiciona comando CLI `monitor-comunitario scrape`;
- captura página pública da Celesc com Playwright;
- salva snapshot HTML;
- salva snapshot TXT;
- mantém cópias latest para debug rápido;
- adiciona parser textual conservador;
- adiciona testes de limpeza/extração textual.

### Observação

A extração de avisos reais será feita depois de analisarmos os snapshots capturados localmente. Esta etapa prioriza auditabilidade e estabilidade da coleta.

## 2026-06-16 — feat(municipality-selector-scraper)

Terceira fatia funcional:

- adiciona busca por caixa seletora nativa de municípios;
- enumera opções ativas;
- filtra placeholders como "Selecione";
- adiciona comando `monitor-comunitario scrape-municipalities`;
- captura snapshots HTML/TXT por município selecionado;
- salva índice JSON com opções e arquivos capturados.

### Observação

Esta etapa corrige a premissa do scraper: os avisos reais dependem da seleção de município ativo. A persistência dos avisos deve vir depois da análise dos snapshots por município.

## 2026-06-16 — feat(outage-notice-persistence)

Quarta fatia funcional:

- expande o parser para usar fallback de município vindo do seletor;
- adiciona hash de conteúdo para deduplicação;
- adiciona serviço de persistência de avisos;
- adiciona endpoint `GET /outage-notices`;
- conecta `run-once` ao fluxo selecionar municípios → capturar → parsear → persistir;
- adiciona testes de parser e persistência.

### Observação

Se a captura por município não trouxer blocos detalhados, o parser retorna zero avisos. O pipeline, porém, fica pronto para persistir assim que o texto capturado expuser dados estruturáveis.

## 2026-06-16 — feat(matcher-notifications)

Quinta fatia funcional:

- adiciona tabela de matches entre usuário e aviso;
- adiciona tabela de notificações in-app;
- adiciona serviço de matching por município, bairro, rua e similaridade;
- adiciona deduplicação de matches e notificações;
- adiciona rotas de listagem e leitura de notificações;
- conecta `run-once` ao fluxo completo até notificações in-app.

### Observação

A notificação por WhatsApp via Evolution API ainda permanece desligada por padrão. Esta etapa cria primeiro a camada in-app e auditável.

## 2026-06-16 — feat(worker-monitoring-runs)

Sexta fatia funcional:

- adiciona tabela de histórico `monitoring_runs`;
- centraliza o fluxo em `run_monitoring_cycle`;
- registra status, métricas, erro e snapshot por execução;
- adiciona endpoints admin para consultar e disparar execuções;
- adiciona worker com APScheduler para rodar diariamente no horário configurado.

### Observação

O worker ainda roda no mesmo pacote Python, mas separado da API em deploy. A próxima etapa deve ajustar Docker Compose para subir `api` e `worker` como serviços separados.
