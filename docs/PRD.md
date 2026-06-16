# PRD — Monitor Comunitário Celesc

Data: 2026-06-16  
Status: Draft inicial consolidado  
Produto: Monitor Comunitário — Celesc Outage Watcher

## 1. Resumo executivo

O Monitor Comunitário é um serviço em Python para monitorar diariamente os avisos públicos de desligamentos programados da Celesc e alertar usuários cadastrados quando houver possibilidade de impacto em seu município, bairro ou endereço.

O serviço roda uma vez ao dia, às 06:00, no fuso America/Sao_Paulo. No MVP, as notificações ficam registradas no próprio app. A integração com WhatsApp via Evolution API ficará preparada, porém desativada por configuração até haver número conectado.

## 2. Contexto

A Celesc oferece uma página pública de avisos de desligamentos programados. A página informa que são listados apenas os municípios com desligamentos agendados e que, se o município não aparece na lista, não há programação de desligamento naquele momento.

A Celesc também informa que envia e-mail e SMS aos clientes sobre desligamentos previstos, mas condiciona o recebimento à manutenção do cadastro atualizado. Para pessoa física, a atualização pode exigir comparecimento a loja de atendimento presencial com documento oficial com foto e CPF, além da informação de e-mail e telefone.

Também há fluxos ligados à Agência Web, unidade consumidora, titularidade e documentação. A troca de titularidade, por exemplo, pode exigir número da unidade consumidora, leitura atual, ausência de débitos vencidos e documentação do imóvel.

Essas características criam uma dor prática: nem toda pessoa afetada por um desligamento é necessariamente titular da unidade consumidora ou consegue atualizar o cadastro oficial.

## 3. Problema

Muitos moradores podem não receber avisos oficiais mesmo sendo diretamente afetados por desligamentos programados.

Casos comuns:

- imóvel alugado;
- aluguel informal;
- imóvel em nome do proprietário anterior;
- casa ou sala comercial compartilhada;
- morador que não é titular da conta;
- morador sem acesso aos dados do titular;
- dificuldade com Agência Web;
- cadastro desatualizado;
- dependência de imobiliária ou proprietário;
- pequeno negócio sem processo organizado de consulta diária.

O problema não é a inexistência do aviso oficial. O problema é a fricção entre o dado público disponível e a vida real de quem precisa ser avisado.

## 4. Proposta

Criar uma camada comunitária e independente de alerta baseada somente em dados públicos.

O usuário informa:

- nome;
- WhatsApp;
- município;
- bairro;
- rua/logradouro;
- número opcional;
- preferência sobre receber alerta amplo por município.

O sistema monitora a página pública da Celesc, normaliza os avisos encontrados, compara com os cadastros e cria notificações quando houver possibilidade de impacto.

## 5. Não proposta

O produto não pretende:

- substituir a Celesc;
- representar informação oficial;
- garantir precisão por unidade consumidora;
- consultar CPF, CNPJ, titularidade ou dados privados;
- acessar a Agência Web do usuário;
- prever quedas emergenciais;
- contornar sistemas privados;
- enviar mensagens em massa sem consentimento.

## 6. Persona principal

### Morador não titular

Pessoa que mora em um imóvel, mas não é titular da conta de luz. Quer receber aviso preventivo sem depender do proprietário, imobiliária ou acesso à Agência Web.

### Pequeno negócio local

Precisa se preparar para interrupções, mas não acompanha diariamente o site oficial.

### Administrador técnico

Pessoa que mantém o serviço, monitora logs, verifica snapshots e ajusta o parser quando necessário.

## 7. Escopo do MVP

### Incluído

- Cadastro de usuários.
- Cadastro de endereço textual.
- Execução diária às 06:00.
- Execução manual via CLI e endpoint admin.
- Scraping com Playwright.
- Snapshot bruto da página para auditoria.
- Parser inicial dos avisos.
- Persistência dos avisos encontrados.
- Normalização de município, bairro e rua.
- Matching por município, bairro, rua e similaridade.
- Notificação in-app.
- Provider Evolution API implementado, mas desligado.
- Logs de execução.
- Docker e documentação.
- Setup automatizado para Windows.
- GitHub CLI para criação do repositório.

### Fora do MVP

- Painel visual completo.
- App mobile.
- Push notification nativo.
- Login social.
- Consulta privada de unidade consumidora.
- Integração com CPF ou CNPJ.
- Geocoding avançado.
- Envio real de WhatsApp em produção.
- Monitoramento de falta de energia emergencial.
- Multiestado ou outras distribuidoras.

## 8. Requisitos funcionais

### RF01 — Cadastro de usuário

O sistema deve permitir criar, listar, editar e desativar usuários.

Campos mínimos:

- nome;
- telefone/WhatsApp;
- município;
- bairro;
- rua/logradouro;
- número;
- complemento opcional;
- CEP opcional;
- aceitar alertas amplos por município;
- status ativo/inativo.

### RF02 — Monitoramento diário

O sistema deve executar automaticamente todos os dias às 06:00 no fuso America/Sao_Paulo.

### RF03 — Execução manual

O sistema deve permitir execução manual para desenvolvimento e auditoria:

```bash
uv run monitor-comunitario run-once
```

e, futuramente:

```http
POST /admin/runs/manual
```

### RF04 — Scraping

O scraper deve:

- abrir a página pública da Celesc;
- aguardar carregamento do conteúdo;
- lidar com conteúdo dinâmico;
- capturar HTML bruto;
- capturar snapshot textual;
- registrar erros com clareza;
- não executar múltiplas requisições desnecessárias.

### RF05 — Parser

O parser deve converter o conteúdo bruto em avisos estruturados.

Campos esperados, quando disponíveis:

- município;
- bairro;
- logradouro;
- descrição;
- data de início;
- horário de início;
- horário de término;
- texto bruto;
- hash de conteúdo;
- URL de origem.

### RF06 — Normalização

O sistema deve normalizar:

- acentos;
- caixa alta/baixa;
- pontuação;
- espaços duplicados;
- abreviações de logradouro;
- variações como Rua/R, Avenida/Av, Servidão/Serv, Rodovia/Rod;
- nomes de municípios com pequenas diferenças.

### RF07 — Matching

O matcher deve gerar níveis de correspondência:

- `municipality`: município igual;
- `neighborhood`: município e bairro compatíveis;
- `street`: município e rua compatíveis;
- `fuzzy`: similaridade textual suficiente;
- `uncertain`: município compatível, mas sem detalhe suficiente;
- `none`: sem correspondência.

### RF08 — Política de alerta

O sistema deve gerar alerta quando:

- houver match por rua;
- houver match por bairro;
- houver match fuzzy acima do limite configurado;
- houver match incerto e o usuário aceitar alerta amplo por município.

### RF09 — Deduplicação

O sistema não deve criar notificações duplicadas para o mesmo usuário e o mesmo aviso.

### RF10 — Notificação in-app

Durante o desenvolvimento, a notificação deve ser salva no banco com status:

- `created`;
- `read`;
- `dismissed`;
- `failed`.

### RF11 — Provider Evolution

O provider Evolution deve existir, mas ficar desativado por padrão:

```env
NOTIFICATION_PROVIDER=app
EVOLUTION_ENABLED=false
```

Quando ativado, deve enviar mensagem para o WhatsApp cadastrado.

### RF12 — Logs

Cada execução deve registrar:

- início;
- fim;
- status;
- quantidade de avisos encontrados;
- quantidade de usuários avaliados;
- quantidade de matches;
- quantidade de notificações criadas;
- erro, se houver;
- caminho do snapshot, se houver.

## 9. Requisitos não funcionais

### RNF01 — Responsabilidade com fonte pública

O sistema deve consultar a página em baixa frequência, começando por 1x ao dia.

### RNF02 — Idempotência

Reexecutar o job no mesmo dia não deve duplicar notificações.

### RNF03 — Auditabilidade

Snapshots e logs devem permitir entender por que um alerta foi ou não gerado.

### RNF04 — Privacidade

O MVP não deve exigir CPF, CNPJ ou titularidade. A coleta deve ser mínima.

### RNF05 — Portfólio

O repositório deve ser legível, bem documentado e demonstrar boas práticas:

- README forte;
- PRD;
- ADR;
- arquitetura;
- CI;
- lint;
- testes;
- Docker;
- scripts de setup;
- comentários úteis;
- docstrings em serviços principais.

### RNF06 — Manutenibilidade

O scraper deve ficar isolado, porque a página pública pode mudar.

## 10. Modelo de dados inicial

### users

```text
id
name
phone
municipality
neighborhood
street
number
zipcode
accept_municipality_wide_alerts
is_active
created_at
updated_at
```

### outage_notices

```text
id
source
source_url
municipality
neighborhood
street
description
starts_at
ends_at
raw_text
content_hash
created_at
```

### monitoring_runs

```text
id
started_at
finished_at
status
notices_found
users_checked
matches_found
notifications_created
error_message
raw_snapshot_path
```

### user_outage_matches

```text
id
user_id
outage_notice_id
match_level
match_score
match_reason
created_at
```

### notifications

```text
id
user_id
outage_notice_id
channel
status
title
message
sent_at
read_at
error_message
created_at
```

## 11. API inicial

### Healthcheck

```http
GET /health
```

### Usuários

```http
POST /users
GET /users
GET /users/{user_id}
PATCH /users/{user_id}
DELETE /users/{user_id}
```

### Notificações

```http
GET /users/{user_id}/notifications
PATCH /notifications/{notification_id}/read
```

### Admin

```http
POST /admin/runs/manual
GET /admin/runs
GET /admin/runs/{run_id}
```

## 12. CLI inicial

```bash
monitor-comunitario doctor
monitor-comunitario run-once
monitor-comunitario scrape
monitor-comunitario match-debug
monitor-comunitario seed-user
```

## 13. Configuração

```env
APP_ENV=development
APP_TIMEZONE=America/Sao_Paulo
DATABASE_URL=sqlite:///./data/monitor_comunitario.db

CELESC_OUTAGES_URL=https://www.celesc.com.br/avisos-de-desligamentos
SCRAPER_HEADLESS=true
SCRAPER_TIMEOUT_MS=30000
SNAPSHOT_DIR=./snapshots

SCHEDULER_ENABLED=true
SCHEDULER_HOUR=6
SCHEDULER_MINUTE=0

NOTIFICATION_PROVIDER=app

EVOLUTION_BASE_URL=
EVOLUTION_API_KEY=
EVOLUTION_INSTANCE=
EVOLUTION_ENABLED=false
```

## 14. Template de mensagem

```text
Aviso de desligamento programado da Celesc

Encontramos um desligamento programado que pode afetar seu endereço:

Município: {municipality}
Área: {area}
Data/Horário: {period}

Descrição:
{description}

Este projeto usa informações públicas da Celesc e não é um canal oficial. A programação pode sofrer alteração ou cancelamento. Confira os canais oficiais antes de tomar decisões importantes.
```

## 15. Critérios de aceite do MVP

O MVP será aceito quando:

- o projeto instalar em Windows com script;
- o projeto rodar local via `uv`;
- o healthcheck responder;
- for possível cadastrar usuário;
- o scraper capturar a página;
- o parser persistir avisos;
- o matcher comparar aviso e usuário;
- o sistema criar notificação in-app;
- execuções repetidas não duplicarem alerta;
- logs e snapshots forem salvos;
- Evolution estiver preparado por feature flag;
- testes principais passarem;
- README explicar instalação, limitações e roadmap;
- GitHub Actions rodar lint e testes.

## 16. Riscos

### Mudança no layout da Celesc

Mitigação: snapshots, parser isolado e teste com fixtures.

### Avisos com dados incompletos

Mitigação: níveis de confiança e alertas incertos opcionais.

### Falso positivo

Mitigação: usar linguagem “pode afetar”.

### Falso negativo

Mitigação: permitir alerta amplo por município.

### WhatsApp indisponível

Mitigação: provider in-app e status de falha/retry.

### Dados pessoais

Mitigação: não pedir CPF/CNPJ; coletar apenas dados necessários.

## 17. Roadmap

### Fase 1 — Documentação e bootstrap

- PRD.
- Arquitetura.
- ADR da stack.
- README.
- Scripts de instalação.
- pyproject.
- CI.

### Fase 2 — API e banco

- FastAPI.
- Models.
- Migrations.
- Users.
- Notifications.

### Fase 3 — Scraper

- Playwright.
- Snapshot.
- Parser.
- Persistência dos avisos.

### Fase 4 — Matching

- Normalização.
- Score.
- Deduplicação.
- Testes.

### Fase 5 — Worker

- Scheduler diário.
- Execução manual.
- Logs de runs.

### Fase 6 — Evolution

- Provider HTTP.
- Mensagem.
- Feature flag.
- Retry básico.

### Fase 7 — Polimento de portfólio

- README final.
- Diagrama.
- Screenshots.
- Exemplos.
- Issues iniciais.
- Roadmap público.

## 18. Fontes de referência

- Página pública de avisos de desligamentos da Celesc.
- Notícia da Celesc sobre consulta no site/app e envio de e-mail/SMS.
- Página da Celesc sobre atualização cadastral.
- Página da Celesc sobre troca de titularidade.
- Página oficial/GitHub da Evolution API.
