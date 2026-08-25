# Release evidence

## Baseline

- Branch: `final-project`
- Original functional check: 2026-08-06
- API result: `GET /health` returned HTTP 200 with `status: "ok"`.
- Frontend result: the three Kanban columns, task cards, Edit controls, and New Task form were visible.
- Original full-suite result: 28 passed with three dependency-deprecation warnings.

The final layout correction on 2026-08-14 moved the functional backend from `backend/app/` to the required root `app/`. It did not add product behavior. Current verification is recorded below.

## CI evidence

- Workflow: `.github/workflows/ci.yml`
- Trigger: pushes to `main` and `final-project`, plus pull requests.
- Python: explicit version `3.12`.
- Install: `python -m pip install -r requirements.txt pytest httpx`.
- Test: `python -m pytest tests -q` from the repository root.
- Shortcut check: no `continue-on-error`, no `|| true`, and pytest is not skipped.
- Successful root-layout test/Docker run: <https://github.com/Lina-KS/Task-Tracker/actions/runs/31791350995> for commit `1396403`.

## Docker evidence

```text
docker build -t task-tracker:final .
docker run --rm --name task-tracker-final -p 8000:8000 task-tracker:final
curl --fail http://localhost:8000/health
```

The Dockerfile uses `USER appuser`, copies `requirements.txt` and `app/`, excludes `.env` through `.dockerignore`, declares port 8000, and starts `python -m uvicorn app.main:app --host 0.0.0.0 --port 8000`. Local Docker was unavailable. In the linked root-layout CI run, both `test` and `docker` succeeded; the Docker job built the image, ran the container, and passed `/health`.

## Current root-layout verification

- Final merged-tree test command: `.\.venv\Scripts\python.exe -m pytest tests -q -p no:cacheprovider`.
- Test result: **26 passed, 3 warnings in 0.95s**.
- Environment note: pytest's cache plugin was disabled only to avoid a local cache artifact; no test was skipped or weakened.
- API command: `.\.venv\Scripts\python.exe -m uvicorn app.main:app --host 127.0.0.1 --port 8010`.
- Health result: **HTTP 200**, `{"status":"ok","timestamp":"2026-08-14T09:51:36.806397+00:00"}`.
- Protected-code reason: `app/storage.py` now resolves JSON data under `app/data/`, matching the required root layout.

## Documentation claim-vs-reality log

| Claim checked | Evidence | Result |
|---|---|---|
| The API imports from root `app/`. | Root pytest run plus Uvicorn `/health` request. | Confirmed: 26 tests passed and `/health` returned HTTP 200. |
| Tests do not modify application JSON. | `tests/conftest.py` redirects storage to pytest `tmp_path`. | Confirmed by inspection. |
| CI installs dependencies and runs pytest. | `.github/workflows/ci.yml` and linked Actions run. | Confirmed: online `test` job succeeded. |
| Docker runs non-root without `.env`. | `Dockerfile`, `.dockerignore`, and linked Actions run. | Confirmed: online build/run/health job succeeded. |
