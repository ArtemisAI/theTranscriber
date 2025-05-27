# Backend – FastAPI Service

This directory contains the Python source code for the **YouTube Transcript Retrieval Service**.  The implementation follows a layered, service-oriented architecture so that each concern (API routing, domain logic, data access, infrastructure) can evolve independently.

## Layout

```
backend/
└─ app/
   ├─ api/           # FastAPI routers
   │   └─ routes/    # Individual endpoint modules (search, transcripts, …)
   ├─ core/          # Settings, startup & common utilities
   ├─ services/      # Business logic (YT client, transcript formatting, …)
   ├─ cache/         # Redis helpers
   ├─ models/        # Pydantic request/response models
   └─ utils/         # Logging, helpers
```

## Quick start (dev)

```
cd backend
uvicorn app.main:app --reload
```

Or run the full stack with Redis:

```
docker compose up --build
```

Unit tests live under `../tests/` at the project root.
