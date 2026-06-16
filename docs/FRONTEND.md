# Frontend do usuário final

## Visão geral

O frontend inicial é uma página estática servida pelo próprio FastAPI.

```text
GET /
GET /static/styles.css
GET /static/app.js
```

A decisão foi manter HTML/CSS/JS simples nesta etapa para evitar introduzir React/Vite antes da base de produto estar fechada.

## Funcionalidades

- apresentação pública do monitor;
- cadastro de usuário usando `POST /users`;
- armazenamento do ID do cadastro no `localStorage`;
- consulta de notificações via `GET /users/{user_id}/notifications`;
- espaços reservados para publicidade local;
- link para documentação da API em `/docs`.

## Espaços de anúncio

Os blocos de anúncio são placeholders visuais:

```text
Publicidade
Espaço para anúncio local
Anúncio do bairro
Espaço horizontal para campanha, patrocinador ou utilidade pública
```

Não há integração com rede de anúncios nesta etapa.

## Limitações atuais

- não existe autenticação do usuário final;
- o ID do cadastro fica salvo apenas no navegador;
- a consulta por ID é aberta;
- não há edição de cadastro pela interface;
- não há integração real com anúncios.

## Próximas melhorias

- autenticação simples por telefone/código;
- edição de cadastro;
- tela de preferências de alerta;
- painel de parceiros/anúncios;
- separar frontend em React/Vite apenas se a interface crescer.
