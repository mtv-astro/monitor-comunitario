# Exportação e Importação de Dados

O Monitor Comunitário oferece comandos de CLI para exportar e importar dados em formato JSON. Isso é útil para migrar de um ambiente SQLite para Postgres/Supabase ou para criar backups legíveis.

## Exportar dados

Use o comando `db-export` e especifique um caminho de arquivo de saída:

```bash
uv run monitor-comunitario db-export --output data/export.json
```

O arquivo conterá chaves para `users`, `outage_notices`, `user_outage_matches`, `notifications` e `monitoring_runs`. Os valores são listas de objetos com os campos das tabelas, convertendo datas para ISO 8601.

## Importar dados

Para carregar um arquivo JSON previamente exportado, use:

```bash
uv run monitor-comunitario db-import --input data/export.json
```

A importação realiza merge de registros existentes com base em IDs, preservando ou remapeando conforme necessário. Os dados são adicionados dentro de uma transação.

## Boas práticas

- Nunca commit arquivos de exportação contendo dados reais no repositório.
- Para clonar dados de desenvolvimento para Supabase, exporte de SQLite, substitua `DATABASE_URL` e importe no novo ambiente.
- Documente quais dados estão incluídos para atender requisitos de LGPD.
