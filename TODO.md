# YouTube Transcript Retrieval Service – Master TODO

This file enumerates **all** development and QA tasks, grouped by phase and component.  Use it as a living backlog – update, re-order, or break down tasks during sprint planning.

## Legend

- `[ ]` = not started  `[~]` = in progress  `[x]` = done
- **🔄 recurring** = maintenance task that repeats (e.g. dependency upgrades)

---

## Phase 1 – Project scaffolding & CI

| # | Task | Owner | Status |
|---|------|-------|--------|
| 1 | Create repo structure (`backend/`, `frontend/`, `docker-compose.yml`, etc.) | Dev-Ops | [ ] |
| 2 | Add `Dockerfile` for FastAPI image | Backend | [ ] |
| 3 | Add `Dockerfile` (multi-stage) for React/Vite frontend | Frontend | [ ] |
| 4 | Implement GitHub Actions workflow (lint → test → build) | Dev-Ops | [ ] |
| 5 | Write basic `/health` endpoint & unit test | Backend | [ ] |
| 6 | Publish image to internal registry | Dev-Ops | [ ] |

## Phase 2 – Core API (search & single transcript)

| # | Task | Owner | Status |
|---|------|-------|--------|
| 10 | Add `/search` endpoint – proxy to YouTube Data API | Backend | [ ] |
| 11 | Add `/transcripts` endpoint – single `videoId`, JSON/text output | Backend | [ ] |
| 12 | Integrate youtube-transcript-api library | Backend | [ ] |
| 13 | Pydantic response models & OpenAPI docs | Backend | [ ] |
| 14 | Frontend: Search form + basic results list | Frontend | [ ] |
| 15 | Frontend: Transcript viewer component | Frontend | [ ] |

## Phase 3 – Bulk & Playlists

| # | Task | Owner | Status |
|---|------|-------|--------|
| 20 | Accept multiple `videoIds` (comma-separated or JSON array) | Backend | [ ] |
| 21 | `/playlists/{id}/transcripts` endpoint | Backend | [ ] |
| 22 | SRT formatter support | Backend | [ ] |
| 23 | Async concurrent fetching for bulk requests | Backend | [ ] |
| 24 | UI: Bulk input text-area & downloadable ZIP | Frontend | [ ] |

## Phase 4 – Caching & Performance

| # | Task | Owner | Status |
|---|------|-------|--------|
| 30 | Add Redis container & cache layer | Backend | [ ] |
| 31 | Cache transcripts with TTL | Backend | [ ] |
| 32 | Prometheus metrics endpoint | Dev-Ops | [ ] |
| 33 | Load testing with k6/Locust | QA | [ ] |

## Phase 5 – Observability & Hardening

| # | Task | Owner | Status |
|---|------|-------|--------|
| 40 | Structured logging (JSON) | Backend | [ ] |
| 41 | Error handling / Sentry integration | Backend | [ ] |
| 42 | Rate limiting middleware | Backend | [ ] |
| 43 | Swagger/OpenAPI customisation & examples | Backend | [ ] |
| 44 | CI: security scanning (Bandit, Trivy) | Dev-Ops | [ ] |

## Phase 6 – Integration & E2E testing

| # | Task | Owner | Status |
|---|------|-------|--------|
| 50 | Deploy via Docker Compose on staging server | Dev-Ops | [ ] |
| 51 | n8n workflow to call API & store transcript | Integrations | [ ] |
| 52 | E2E tests with Playwright (frontend + API) | QA | [ ] |

## Future (Phase 7+) – Security, Auth, Monetisation

| # | Task | Owner | Status |
|---|------|-------|--------|
| 60 | API key authentication layer | Backend | [ ] |
| 61 | Usage tiers / billing model | Product | [ ] |
| 62 | Optional web dashboard & admin UI | Frontend | [ ] |

---

### Recurring tasks

- 🔄 Dependabot / pip-compile to keep dependencies up-to-date
- 🔄 Review CVEs & patch Docker base images

