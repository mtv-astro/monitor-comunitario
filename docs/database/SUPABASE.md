# Supabase / Postgres Externo

Supabase é uma plataforma que oferece Postgres gerenciado com autenticação, armazenamento e APIs prontas. Neste projeto, usamos apenas o banco Postgres do Supabase para demonstrar um deploy cloud sem gerenciar infraestrutura.

## Preparação

1. Crie um projeto no [Supabase](https://supabase.com).
2. Acesse as configurações do banco e copie a string de conexão.
3. Preencha o valor de `DATABASE_URL` em `.env.supabase.example` com a string de conexão, substituindo `username` e `password`.
4. Ajuste outros parâmetros conforme necessário (SSL obrigatório).

Exemplo de `DATABASE_URL`:

```
postgresql+psycopg://postgres:YOUR_PASSWORD@db.your-project.supabase.co:6543/postgres?sslmode=require
```

## Deploy

Para rodar a aplicação apontando para o Supabase, utilize o `docker-compose.supabase.yml`:

```bash
docker compose -f docker-compose.supabase.yml up --build
```

Isso iniciará os serviços `api` e `worker` usando o arquivo `.env.supabase.example`. Certifique-se de gerar e aplicar as migrations no Supabase antes de iniciar:

```bash
uv run monitor-comunitario db-upgrade
```

## Considerações

- Supabase tem limitações de recursos e quotas no plano gratuito. Ajuste o volume de dados de acordo.
- Não armazene dados pessoais reais; use o seed de demonstração para mostrar o funcionamento do sistema.
- Ative as Regras de Segurança (RLS) e autenticação apenas se for necessário evoluir para um produto real.
