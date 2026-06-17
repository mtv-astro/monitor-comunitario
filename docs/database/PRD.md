# Banco de Dados – Monitor Comunitário

Este documento descreve a especificação de endurecimento e preparação para o uso de bancos de dados PostgreSQL/Supabase no projeto **Monitor Comunitário**. O objetivo é evoluir a camada de persistência, mantendo suporte a SQLite para desenvolvimento rápido e preparando a aplicação para operar em Postgres local (via Docker Compose) e em um banco gerenciado como o Supabase.

## Contexto

O projeto coleta avisos públicos de desligamentos programados, persiste avisos, cruza com usuários cadastrados, gera notificações e executa um worker agendado. Até agora, a aplicação utiliza SQLite como padrão de desenvolvimento, com suporte inicial a Postgres local via Docker Compose e Supabase. Para um portfólio robusto, é necessário consolidar a camada de banco, adicionando versionamento de schema, migrações controladas e ferramentas de importação/exportação.

## Objetivos

- Suportar três modos de banco: SQLite local, Postgres local via Docker Compose e Supabase/Postgres externo.
- Versionar o schema com Alembic, permitindo evoluções controladas sem depender de `create_all()` em produção.
- Adicionar comandos CLI para exportar e importar dados entre ambientes.
- Criar comando para seed demo com dados fictícios.
- Documentar a arquitetura, uso de Supabase, processos de backup e restore, e orientações de LGPD.
- Configurar integração contínua (CI) que valida as migrations e roda testes contra um Postgres real.

## Escopo

1. **Migrations Alembic**  
   - Implementar `alembic.ini` e um diretório `migrations/` contendo `env.py` e uma migration inicial.  
   - Adicionar comandos CLI (`db-upgrade`, `db-downgrade`, `db-current`, `db-history`, `db-revision`, `db-stamp`).  
   - Garantir que as migrations rodem em SQLite e Postgres, com autogeração funcionando.

2. **Perfis de banco**  
   - Definir variáveis em `.env.example`, `.env.docker.example` e `.env.supabase.example`.  
   - Configurar `docker-compose.yml` com serviço Postgres local e `docker-compose.supabase.yml` para uso de banco externo.  
   - Garantir que arquivos `.env` reais não sejam commitados.

3. **CI com Postgres real**  
   - Adicionar job GitHub Actions que inicia um serviço Postgres, aplica as migrations e roda os testes (`ruff`, `mypy`, `pytest`).

4. **Export/import de dados**  
   - Implementar comandos `db-export` e `db-import` para gerar e restaurar um JSON determinístico contendo users, outage_notices, user_outage_matches, notifications e monitoring_runs.  
   - Prever remapeamento de IDs e evitar duplicações.

5. **Seed demo**  
   - Implementar comando `db-seed-demo` que cria dados fictícios (usuários, avisos, correspondências, notificações e execuções de monitoramento) sem informações pessoais reais.

6. **Documentação**  
   - Criar documentos em `docs/database/` detalhando PRD, arquitetura, processos de migração, export/import, uso do Supabase, seed demo e rotinas de backup/restore.  
   - Explicar diferenças entre SQLite e Postgres, quando utilizar cada perfil, como rodar e gerar migrations, e precauções com dados pessoais (LGPD).

## Fora de escopo

Esta etapa não inclui autenticação completa de usuários, regras de acesso row-level no Supabase, integração com Evolution API/WhatsApp, painel admin completo, ads reais ou backup automático em produção.
