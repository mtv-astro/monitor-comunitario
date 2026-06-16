# Consentimento, ads e analytics

## Objetivo

O projeto suporta dois estados operacionais:

```text
ADS_ENABLED=false  → pré-ads, sem scripts de terceiros
ADS_ENABLED=true   → ads, scripts condicionados ao consentimento
```

O mesmo vale para analytics:

```text
ANALYTICS_ENABLED=false
ANALYTICS_ENABLED=true
```

## Flags

```env
ADS_ENABLED=false
ADS_PROVIDER=placeholder
ADSENSE_CLIENT_ID=
ADSENSE_DEFAULT_SLOT=

ANALYTICS_ENABLED=false
ANALYTICS_PROVIDER=none
GOOGLE_ANALYTICS_ID=

CONSENT_REQUIRED=true
CONSENT_VERSION=2026-06-16-v1
```

## Modo pré-ads

Com ads e analytics desativados:

```text
não carrega Google AdSense
não carrega Google Analytics
não carrega pixel de terceiros
mantém placeholders visuais de anúncio
usa localStorage apenas para cadastro e consentimento
```

## Modo ads

Com AdSense:

```env
ADS_ENABLED=true
ADS_PROVIDER=google_adsense
ADSENSE_CLIENT_ID=ca-pub-xxxxxxxxxxxxxxxx
ADSENSE_DEFAULT_SLOT=0000000000
```

O script só é injetado depois que o usuário aceita publicidade.

## Analytics

Com Google Analytics:

```env
ANALYTICS_ENABLED=true
ANALYTICS_PROVIDER=google_analytics
GOOGLE_ANALYTICS_ID=G-XXXXXXXXXX
```

O script só é injetado depois que o usuário aceita analytics.

## Consent version

Sempre que mudar a política, finalidade, provedor ou tipo de dado tratado, aumente:

```env
CONSENT_VERSION=2026-06-16-v2
```

Isso força o banner a pedir uma nova decisão do usuário.

## Próxima melhoria

Registrar consentimento também no backend quando houver autenticação ou identificação forte do usuário.
