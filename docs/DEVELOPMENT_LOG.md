# Development Log

## 2026-06-16 — feat(database-and-users)

Primeira fatia funcional planejada:

- adiciona sessão de banco com SQLAlchemy;
- cria inicialização local com `Base.metadata.create_all`;
- adiciona schemas Pydantic para usuários;
- adiciona rotas CRUD de `/users`;
- mantém delete como desativação lógica;
- adiciona testes básicos com `TestClient`.

### Observação

Alembic será adicionado na próxima etapa de banco/migrations. Para esta fatia, a inicialização automática mantém o projeto simples para desenvolvimento local.
