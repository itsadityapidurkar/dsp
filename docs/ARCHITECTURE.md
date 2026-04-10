# Architecture

The project uses a pragmatic monorepo split:

- `frontend/`: Next.js App Router client for dashboards and tools
- `backend/`: FastAPI service with repository and service layers
- `database/`: PostgreSQL schema
- `data_pipeline/`: cleaning and loading scripts tied to the unified jobs file
- `docs/`: architecture and API documentation

Analytics are deterministic and computed server-side from canonical job fields. Gemini is only used for concise narrative summaries and never for core scoring or aggregations.
