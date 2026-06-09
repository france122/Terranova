# AGENTS.md

## Project overview

Terranova is a gamified learning platform that renders university course structures as explorable RPG-style maps. Knowledge graphs drive fog-of-war mechanics, quest systems, and achievement badges. See `CLAUDE.md` for full product spec.

## Repository layout

```
src/
  backend/       # Python FastAPI (SQLModel + SQLite)
    app/
      main.py          # FastAPI app entry, mounts all routers under /api/
      config.py        # JWT secret, DB URL, gamification constants (EXP, level thresholds)
      database.py      # SQLite engine, init_db(), get_session()
      graph_data.py    # In-memory NetworkX knowledge graph (seed data, query API)
      models/          # SQLModel ORM: user, progress, achievement, quest, social
      routers/         # auth, graph, map, learn, quest, achievement, social
      services/        # Business logic: auth, map, quest, achievement, seed, social, graph
  frontend/      # React 19 SPA (Vite + TypeScript)
    src/
      api/             # Axios client (baseURL: localhost:8000/api) + endpoint wrappers
      hooks/useAuth.tsx # AuthProvider context, JWT token management
      components/      # Map/, Profile/, Quest/, Achievement/, Leaderboard/, Auth/, Layout/
      pages/           # Thin wrappers that render components
docker-compose.yml     # Neo4j 5 (ports 7474/7687, password: terranova123)
```

## Dev commands

### Frontend (`src/frontend/`)

```sh
pnpm install          # install deps (pnpm, not npm)
pnpm dev              # vite dev server on :5173
pnpm build            # tsc -b && vite build
pnpm lint             # eslint
npx tsc --noEmit      # typecheck without build
```

### Backend (`src/backend/`)

```sh
uv sync               # install deps (uv, not pip)
uv run uvicorn app.main:app --reload --port 8000   # dev server
uv run pytest          # tests (httpx for async)
```

Backend working directory matters — run commands from `src/backend/` because `terranova.db` is created relative to cwd and `app/` imports expect that root.

### Neo4j (optional — graph DB not yet wired into backend)

```sh
docker compose up -d   # neo4j:5 with APOC on :7474/:7687
```

## Architecture notes

- **Knowledge graph** lives in `graph_data.py` as an in-memory NetworkX `DiGraph` built from `SEED_DATA` at import time. Neo4j container exists but is not connected to the backend yet. All graph queries go through `graph_data.*` functions.
- **Auth** uses JWT (HS256, 7-day expiry). Token stored in `localStorage`, injected via Axios request interceptor. 401 responses auto-redirect to `/login`.
- **Map state** (fog-of-war) is computed server-side in `services/map_service.py` per user per domain. Node states: `locked → visible → unlocked → explored → mastered`.
- **EXP/Level** thresholds in `config.py`: 学徒(0), 入门(500), 进阶(2000), 精通(5000), 大师(10000). Level is recalculated whenever EXP changes.
- **SQLite DB** file is `src/backend/terranova.db`. Auto-created on first run via `init_db()`. Delete it to reset all user data.
- **Seed data** (`services/seed_service.py`) populates quest templates and achievement definitions on startup.

## Frontend conventions

- **Unified RPG pixel style**: all components use `rpgBorder()` helper (3px solid borders, inset box-shadow). Do NOT use rounded `borderRadius` cards.
- **Header pattern**: every page uses Press Start 2P font, 14px, gold `#f1c40f` with textShadow, icon + title.
- **Fonts**: `Press Start 2P` for headings/labels/buttons, `VT323` for body/descriptions/tabs, `Inter` only in Layout nav.
- **No shared style module** — `rpgBorder()` is copy-pasted per component file. This is intentional for now.
- **Learning auto-complete**: `LearnPage` auto-triggers `completeNode` when simulated video reaches 100%. No manual complete button.

## Key gotchas

- CORS only allows `http://localhost:5173`. If frontend port changes, update `main.py`.
- `graph_data.py` is the single source of truth for all courses and knowledge points. Adding a course requires adding nodes (domain→course→chapter→knowledge_point) and edges (CONTAINS, PREREQUISITE, optionally RELATED_TO) here.
- `user.level` is a Chinese string (e.g. "学徒"), not a number. Frontend displays it as `Lv.学徒`.
- `streak_days` calculation uses `timedelta(days=1)` for yesterday detection — do not use `date.replace(day=day-1)`.
- Star ratings on knowledge points can only increase, never decrease. Backend rejects downgrades.
- Quest auto-completion in `update_quest_progress()` must recalculate user level after awarding bonus EXP.
