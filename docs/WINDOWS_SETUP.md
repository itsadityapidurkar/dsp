# Windows Local Setup

This guide starts the project locally on Windows without changing the master dataset file.

## 1. Prerequisites

Install these first:

- Python 3.11 or newer
- Node.js 22 or newer
- Git
- Docker Desktop
- PostgreSQL client tools optional but useful

Recommended:

- Windows Terminal
- VS Code

## 2. Open the Project Folder

Open PowerShell and move to the project root:

```powershell
cd G:\DSPPR
```

If your repo is on a different drive or folder, use that path instead.

## 3. Confirm the Master File Exists

Do not edit or replace it.

Check that this file exists:

```powershell
dir G:\DSPPR\DataSets\outputs\unified_jobs_dataset.csv
```

## 4. Start PostgreSQL with Docker

From the project root:

```powershell
docker compose up -d
```

Confirm the container is running:

```powershell
docker ps
```

You should see `job-market-postgres`.

## 5. Create a Backend Virtual Environment

From the project root:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

If PowerShell blocks activation, run:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.\.venv\Scripts\Activate.ps1
```

## 6. Install Backend Dependencies

```powershell
pip install -r .\backend\requirements.txt
```

## 7. Create the Backend Environment File

Copy the example:

```powershell
Copy-Item .\backend\.env.example .\backend\.env
```

Open `backend\.env` and confirm these values:

```env
DATABASE_URL=postgresql+psycopg://postgres:postgres@localhost:5432/job_market_intelligence
GEMINI_API_KEY=
CORS_ORIGINS=http://localhost:3000
APP_ENV=development
LOG_LEVEL=INFO
```

Leave `GEMINI_API_KEY` blank if you do not have one yet.

## 8. Load the Existing Master File into PostgreSQL

Run this from the project root while the virtual environment is active:

```powershell
$env:PYTHONPATH="G:\DSPPR\backend"
python .\data_pipeline\load_unified_data.py `
  --csv G:\DSPPR\DataSets\outputs\unified_jobs_dataset.csv `
  --database-url postgresql+psycopg://postgres:postgres@localhost:5432/job_market_intelligence `
  --chunk-size 5000 `
  --truncate
```

Notes:

- This reads the master file but does not modify it.
- The first full load can take time because the file is large.

## 9. Start the Backend API

Open a new PowerShell window.

Go to the project root and activate the venv again:

```powershell
cd G:\DSPPR
.\.venv\Scripts\Activate.ps1
```

Set `PYTHONPATH` and start the API:

```powershell
$env:PYTHONPATH="G:\DSPPR\backend"
uvicorn backend.main:app --reload --host 0.0.0.0 --port 8000
```

Open these URLs in your browser:

- API health/docs: `http://localhost:8000/docs`
- API root docs page should load if startup is correct

## 10. Install Frontend Dependencies

Open another new PowerShell window:

```powershell
cd G:\DSPPR\frontend
npm install
```

## 11. Create the Frontend Environment File

```powershell
Copy-Item .\.env.example .\.env.local
```

Confirm it contains:

```env
NEXT_PUBLIC_API_BASE_URL=http://localhost:8000/api/v1
```

## 12. Start the Frontend

From `G:\DSPPR\frontend`:

```powershell
npm run dev
```

Open:

`http://localhost:3000`

## 13. Recommended Startup Order

Each time you work locally:

1. `docker compose up -d`
2. Activate backend venv
3. Start backend with Uvicorn
4. Start frontend with `npm run dev`

You only need to reload the master file when the database is empty or you want a fresh import.

## 14. Useful Verification Commands

Backend tests:

```powershell
cd G:\DSPPR
$env:PYTHONPATH="G:\DSPPR\backend"
pytest .\backend\tests -q
```

Frontend lint:

```powershell
cd G:\DSPPR\frontend
npx eslint . --ext .ts,.tsx,.mjs
```

Frontend production build:

```powershell
cd G:\DSPPR\frontend
npm run build
```

## 15. If Something Fails

If Docker is not running:

- Start Docker Desktop first

If port `5432` is busy:

- Stop the local PostgreSQL service using that port
- Or change the port mapping in `docker-compose.yml`

If port `8000` or `3000` is busy:

- Stop the process using the port
- Or run Uvicorn/Next on a different port

If PowerShell blocks scripts:

- Use the temporary execution-policy command shown earlier

If the data load fails:

- Confirm the dataset path is correct
- Confirm Docker Postgres is running
- Confirm the backend dependencies are installed

## 16. Optional Gemini Setup

If you want AI summaries:

1. Get a Gemini API key
2. Add it to `backend\.env`

```env
GEMINI_API_KEY=your_key_here
```

3. Restart the backend

The app still works without Gemini.

## 17. Main Local Paths

- Project root: `G:\DSPPR`
- Dataset: `G:\DSPPR\DataSets\outputs\unified_jobs_dataset.csv`
- Backend env: `G:\DSPPR\backend\.env`
- Frontend env: `G:\DSPPR\frontend\.env.local`

## 18. One-Line Summary

Start Docker, load the existing master file into Postgres, run the FastAPI backend on port `8000`, then run the Next.js frontend on port `3000`.
