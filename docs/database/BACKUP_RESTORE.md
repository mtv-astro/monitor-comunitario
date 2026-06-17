# Backup e Restauração

Manter backups adequados é essencial para preservar dados de usuários. Este projeto fornece orientações genéricas; adapte conforme seu ambiente.

## Backup

- **SQLite**: copie o arquivo `./data/monitor_comunitario.db` para um local seguro. Pare a aplicação durante o backup para garantir consistência.
- **Postgres**: use `pg_dump` ou ferramentas do provedor (por exemplo, Supabase oferece backup automático em alguns planos). No Docker Compose, você pode executar:

```bash
docker compose exec postgres pg_dump -U monitor -d monitor_comunitario -Fc -f /var/lib/postgresql/data/backup.dump
```

- **Export JSON**: o comando `db-export` gera um arquivo legível e portátil contendo apenas as tabelas usadas pelo Monitor. Use este método para migrações ou compartilhamento de dados de demonstração.

## Restauração

- **SQLite**: substitua o arquivo `.db` antigo pelo backup.
- **Postgres**: use `pg_restore` ou a funcionalidade de restauração do seu provedor.
- **Import JSON**: use `db-import` para carregar um arquivo gerado via `db-export`.

## LGPD e Dados Pessoais

- Backup de dados pessoais deve ser armazenado com segurança e acessado apenas por pessoas autorizadas.
- Remova informações sensíveis antes de compartilhar backups com terceiros.
