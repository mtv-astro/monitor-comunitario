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
