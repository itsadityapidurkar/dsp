BACKEND_VENV ?= /tmp/dsppr-backend-venv
PYTHONPATH_BACKEND = PYTHONPATH=/mnt/g/DSPPR/backend

.PHONY: backend-install frontend-install backend-test frontend-lint frontend-build frontend-test db-up load-sample

backend-install:
	$(BACKEND_VENV)/bin/pip install -r backend/requirements.txt

frontend-install:
	cd frontend && npm install

backend-test:
	$(PYTHONPATH_BACKEND) $(BACKEND_VENV)/bin/pytest backend/tests -q -o cache_dir=/tmp/dsppr-pytest-cache

frontend-lint:
	cd frontend && npx eslint . --ext .ts,.tsx,.mjs

frontend-build:
	cd frontend && npm run build

frontend-test:
	cd frontend && npm test

db-up:
	docker compose up -d

load-sample:
	$(PYTHONPATH_BACKEND) $(BACKEND_VENV)/bin/python data_pipeline/load_unified_data.py --database-url sqlite:////tmp/job_market.db --chunk-size 2000 --limit 5000 --truncate
