# File Inventory

| Path | Purpose | Sensitive? | Tracked? | Owner | Notes |
| --- | --- | --- | --- | --- | --- |
| `README.md` | Project overview and local run instructions. | No | Yes | Engineering | Existing documentation should remain concise and linked to docs. |
| `docker-compose.yml` | Local PostgreSQL, backend, and frontend orchestration. | No | Yes | DevOps/Engineering | Uses `.env` for backend and environment default for frontend API URL. |
| `backend/` | FastAPI backend source, tests, Dockerfile, uploads mount. | Mixed | Yes | Backend Engineering | Source is tracked; runtime uploads and bytecode should not be tracked. |
| `frontend/` | React/Vite frontend source, package manifest, build config. | No | Yes | Frontend Engineering | `node_modules` and `frontend/dist` are ignored. |
| `docs/` | Technical and operational documentation. | No | Yes | Engineering | Includes existing phase docs and Phase 0 operating docs. |
| `backend/uploads/` | Local evidence storage. | Yes | Ignored for runtime data | Ops/Engineering | Evidence is sensitive; production storage/access model is open. |
| `.env.example` | Sanitized environment template. | No | Yes | Engineering | Must contain placeholders only. |
| `.env` | Local secrets/configuration. | Yes | No | Developer/Ops | Removed from Git index; must never be committed. |
| `.gitignore` | Ignore rules for secrets, generated files, uploads, logs, builds. | No | Yes | Engineering | Protects future commits; does not rewrite Git history. |
| `AGENTS.md` | Canonical agent operating instructions. | No | Yes | Architecture | First file future agents must read. |
| `CODEX.md` | Thin Codex adapter. | No | Yes | Architecture | Delegates to `AGENTS.md`. |
| `CLAUDE.md` | Thin Claude Code adapter. | No | Yes | Architecture | Delegates to `AGENTS.md` and `planning/`. |
| `planning/` | Durable project memory and Axon-AI operating system. | No | Yes | Architecture/PM | Contains state, decisions, risks, questions, metrics, sprint handoff. |
| `planning/sprints/000-foundation-metrics/` | Sprint 000 requirements, blueprint, acceptance, handoff. | No | Yes | Architecture/PM | Current sprint folder for Phase 0. |
| `backend/app/services/ocr_providers/` | OCR provider abstraction and provider implementations. | No | Yes | Backend Engineering | Keep OCR decoupled. |
| `backend/tests/` | Backend test suite. | No | Yes | Engineering/QA | Covers auth/permissions, evidence, OCR, review. |
| `frontend/package.json` | Frontend dependencies and scripts. | No | Yes | Frontend Engineering | Build/lint scripts used for validation. |
