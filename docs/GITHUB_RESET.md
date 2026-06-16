# Recriar o repositório GitHub com autor correto

Use este guia se o primeiro commit apareceu com outro autor/contribuidor.

## 1. Entrar na pasta

```powershell
cd C:\Users\carlo\projects\monitor-comunitario
```

## 2. Garantir login no GitHub CLI

```powershell
gh auth status
```

Se precisar:

```powershell
gh auth login
```

## 3. Permitir apagar repositório via CLI

O `gh repo delete` exige permissão `delete_repo`.

```powershell
gh auth refresh -s delete_repo
```

## 4. Apagar e recriar tudo

```powershell
.\scripts\reset_and_recreate_github.ps1 -DeleteRemote
```

## 5. Conferir autor local

```powershell
git config user.name
git config user.email
git log --format=fuller -1
```

Esperado:

```text
Author: Carlos Selva <carlostselva@gmail.com>
Commit: Carlos Selva <carlostselva@gmail.com>
```

## 6. Se não quiser apagar o remoto

Rode sem `-DeleteRemote` para recriar apenas o histórico local.

```powershell
.\scripts\reset_and_recreate_github.ps1
```

Depois crie um repositório novo com outro nome, ou apague o antigo manualmente no GitHub.
