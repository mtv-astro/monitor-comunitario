# Migrations com Alembic

Este documento explica como gerenciar a evolução do esquema de banco de dados usando Alembic.

## Configuração

O arquivo `alembic.ini` na raiz configura a localização dos scripts de migration e o log. O script de ambiente `migrations/env.py` injeta a `DATABASE_URL` configurada na aplicação, carregando o `metadata` de `monitor_comunitario.db.models`.

## Comandos principais

- **Criar nova migration**: gera um arquivo em `migrations/versions` comparando o modelo atual com o banco.

```bash
uv run monitor-comunitario db-revision --message "nova alteração"
```

- **Aplicar migrations**:

```bash
uv run monitor-comunitario db-upgrade  # aplica até a última versão
uv run monitor-comunitario db-upgrade <versão>  # aplica até versão específica
```

- **Desfazer migrations**:

```bash
uv run monitor-comunitario db-downgrade <versão>  # volta até versão específica
```

- **Ver estado atual**:

```bash
uv run monitor-comunitario db-current
```

- **Histórico completo**:

```bash
uv run monitor-comunitario db-history
```

- **Marcar versão sem rodar script**:

```bash
uv run monitor-comunitario db-stamp <versão>
```

## Observações

- Em ambientes de produção (Postgres e Supabase), sempre execute as migrations antes de rodar a aplicação.
- Não edite scripts de migrations que já foram aplicados em produção.
- Para desenvolvimento rápido em SQLite, é aceitável usar `create_all()`, mas novas mudanças devem ser refletidas em migrations antes de subir para Postgres.
