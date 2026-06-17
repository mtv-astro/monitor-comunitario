# Seed de Demonstração

Para fins de portfólio e testes, é importante popular o banco com dados fictícios, evitando exposição de informações reais. O comando `db-seed-demo` cria usuários, avisos e notificações artificiais para mostrar o fluxo completo da aplicação.

## Executando o seed

```bash
uv run monitor-comunitario db-seed-demo
```

Esse comando:

- Cria de 3 a 5 usuários fictícios com nomes e telefones genéricos.
- Gera de 2 a 4 avisos de desligamento com endereços e descrições plausíveis.
- Associa usuários e avisos com níveis de correspondência variados.
- Cria notificações simuladas para cada match.
- Registra uma execução de monitoramento (`monitoring_runs`) que resume a operação.

## Observações

- O seed utiliza dados aleatórios ou estáticos que não correspondem a pessoas reais.
- Se desejar limpar o banco antes de um novo seed, use o comando do Alembic para recriar a base ou drope as tabelas manualmente.
- O seed não roda automaticamente; execute apenas quando necessário demonstrar o projeto.
