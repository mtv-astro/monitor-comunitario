#Requires -Version 5.1

param(
    [string]$RepoName = "monitor-comunitario",
    [string]$GitName = "Carlos Selva",
    [string]$GitEmail = "carlostselva@gmail.com",
    [switch]$Private,
    [switch]$DeleteRemote
)

$ErrorActionPreference = "Stop"

[Console]::InputEncoding = [System.Text.UTF8Encoding]::new()
[Console]::OutputEncoding = [System.Text.UTF8Encoding]::new()
$OutputEncoding = [System.Text.UTF8Encoding]::new()

function Write-Step {
    param([string]$Message)
    Write-Host ""
    Write-Host "==> $Message" -ForegroundColor Cyan
}

function Test-Command {
    param([string]$Name)
    return [bool](Get-Command $Name -ErrorAction SilentlyContinue)
}

if (-not (Test-Command "gh")) {
    throw "GitHub CLI not found. Install it and run gh auth login."
}

if (-not (Test-Command "git")) {
    throw "Git not found."
}

$ProjectRoot = Resolve-Path (Join-Path $PSScriptRoot "..")
Set-Location $ProjectRoot

Write-Step "Checking GitHub auth"
gh auth status

$owner = (gh api user --jq ".login").Trim()
$repoFullName = "$owner/$RepoName"

if ($DeleteRemote) {
    Write-Step "Deleting remote repository: $repoFullName"
    Write-Host "If permission fails, run: gh auth refresh -s delete_repo"
    try {
        gh repo delete $repoFullName --yes
    } catch {
        Write-Host "Could not delete remote. It may not exist or delete_repo scope is missing." -ForegroundColor Yellow
    }
} else {
    Write-Host ""
    Write-Host "Remote deletion is disabled by default." -ForegroundColor Yellow
    Write-Host "To delete and recreate the GitHub repository, run:"
    Write-Host ".\scripts\reset_and_recreate_github.ps1 -DeleteRemote"
    Write-Host ""
}

if (Test-Path ".git") {
    Write-Step "Removing local .git directory"
    Remove-Item ".git" -Recurse -Force
}

Write-Step "Reinitializing local repository"
git init | Out-Null
git checkout -b main

Write-Step "Setting correct local Git author"
git config user.name $GitName
git config user.email $GitEmail

Write-Step "Creating clean commit with correct author"
git add .
git commit --author "$GitName <$GitEmail>" -m "chore: bootstrap Monitor Comunitario project"

$visibility = "--public"
if ($Private) {
    $visibility = "--private"
}

Write-Step "Creating GitHub repository and pushing"
gh repo create $RepoName $visibility --source=. --remote=origin --description "Monitor publico de desligamentos programados da Celesc com alertas por endereco." --push

Write-Step "Repository recreated successfully"
gh repo view --web
