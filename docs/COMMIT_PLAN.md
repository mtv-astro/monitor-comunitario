# Plano de commits

## Branch inicial

```bash
git checkout -b chore/bootstrap-project
```

## Commits sugeridos

```bash
git commit -m "chore: bootstrap Python project structure"
git commit -m "docs: add PRD and product justification"
git commit -m "docs: add architecture and stack decision"
git commit -m "chore: add linting typing and test tooling"
git commit -m "feat(api): add FastAPI app with healthcheck"
git commit -m "feat(db): add database models and migrations"
git commit -m "feat(users): add user registration endpoints"
git commit -m "feat(scraper): add Celesc Playwright fetcher"
git commit -m "feat(scraper): persist raw snapshots for audit"
git commit -m "feat(parser): parse Celesc outage notices"
git commit -m "feat(matcher): add address normalization"
git commit -m "feat(matcher): score user addresses against outage notices"
git commit -m "feat(notifications): add in-app notification provider"
git commit -m "feat(worker): run monitoring job daily at 6am"
git commit -m "feat(cli): add development commands"
git commit -m "feat(notifications): add Evolution API provider behind feature flag"
git commit -m "test: add parser matcher and notification coverage"
git commit -m "chore(docker): add Dockerfile and compose setup"
git commit -m "ci: add GitHub Actions workflow"
git commit -m "docs: complete setup guide limitations and roadmap"
```
