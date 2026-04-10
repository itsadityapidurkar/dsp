# Job Market Intelligence Platform

Production-minded full-stack application for market-facing career insights, role comparison, and resume analysis.

## Structure

- `frontend/`: Next.js, TypeScript, Tailwind, shadcn-style UI patterns, Recharts
- `backend/`: FastAPI, SQLAlchemy, Pydantic
- `database/`: PostgreSQL schema
- `data_pipeline/`: unified data cleaning and database loading
- `docs/`: architecture and API notes

## Features

- Analytics dashboard focused on demand, hiring activity, location trends, and salaries
- Explore Trends page with shared filters
- Role Explorer page for role-specific market detail
- Compare Roles tool for exactly two roles
- Resume Analyzer with PDF and DOCX parsing
- Optional Gemini summaries with safe fallback behavior
- Dark and light mode support

## Backend Setup

```bash
cd backend
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
uvicorn main:app --reload
```

## Frontend Setup

```bash
cd frontend
npm install
cp .env.example .env.local
npm run dev
```

## Database Setup

```bash
createdb job_market_intelligence
psql job_market_intelligence -f database/schema.sql
```

Or start PostgreSQL locally with Docker:

```bash
docker compose up -d
```

## Load Unified Job Market Data

The app expects the cleaned master file at:

`/mnt/g/DSPPR/DataSets/outputs/unified_jobs_dataset.csv`

Load it into PostgreSQL:

```bash
python data_pipeline/load_unified_data.py \
  --csv /mnt/g/DSPPR/DataSets/outputs/unified_jobs_dataset.csv \
  --database-url postgresql+psycopg://postgres:postgres@localhost:5432/job_market_intelligence \
  --chunk-size 5000 \
  --truncate
```

For a fast local smoke load without changing the dataset file:

```bash
python data_pipeline/load_unified_data.py \
  --csv /mnt/g/DSPPR/DataSets/outputs/unified_jobs_dataset.csv \
  --database-url sqlite:////tmp/job_market.db \
  --chunk-size 2000 \
  --limit 5000 \
  --truncate
```

## Environment Variables

Backend:

- `DATABASE_URL`
- `GEMINI_API_KEY`
- `CORS_ORIGINS`
- `APP_ENV`
- `LOG_LEVEL`

Frontend:

- `NEXT_PUBLIC_API_BASE_URL`

## Tests

```bash
cd backend
pytest
```

Or use the Makefile:

```bash
make backend-test
make frontend-lint
make frontend-build
make frontend-test
```

## Notes

- Gemini is optional and never drives scoring or aggregations.
- If Gemini is unavailable, the platform falls back to deterministic explanations.
