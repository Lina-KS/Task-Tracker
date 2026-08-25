# Task Tracker

A small FastAPI Task Tracker with a static Kanban frontend and local JSON storage.

## Final Project

Branch reviewed: `final-project`

This submission demonstrates that the existing app remains in scope, pytest runs in CI, Docker builds and verifies `/health`, and AI-assisted work was reviewed rather than accepted blindly.

## Project structure

```text
.github/workflows/ci.yml
app/                         FastAPI application and JSON data
frontend/                    Static HTML/CSS/JavaScript frontend
tests/                       Pytest suite
docs/                        Final evidence and AI playbook
Dockerfile
.dockerignore
AGENTS.md
requirements.txt
README.md
```

## How to run locally

Use Python 3.12 or newer. From the repository root:

```bash
python -m venv .venv
# Linux/macOS: source .venv/bin/activate
# Windows PowerShell: .\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python -m uvicorn app.main:app --reload --port 8000
```

The API is at <http://localhost:8000>, `/health` is at <http://localhost:8000/health>, and Swagger documentation is at <http://localhost:8000/docs>.

In a second terminal, serve the frontend:

```bash
cd frontend
python -m http.server 5500
```

Open <http://localhost:5500>. Do not open `index.html` with a `file://` URL.

## How to run tests

From the repository root with the environment activated:

```bash
python -m pip install pytest httpx
python -m pytest tests -q
```

The tests redirect storage to temporary files and do not modify `app/data/`.

## How to run with Docker

From the repository root:

```bash
docker build -t task-tracker:final .
docker run --rm --name task-tracker-final -p 8000:8000 task-tracker:final
```

In another terminal:

```bash
curl --fail http://localhost:8000/health
```

The image runs as an unprivileged user and does not copy `.env` files.

## Evidence files

- `docs/release-evidence.md`
- `docs/final-ai-review.md`
- `docs/ai-playbook.md`

## AI assistance summary

AI helped review CI, Docker, documentation, security checks, and the final folder layout. I verified the result with tests, diff review, direct `/health` checks, CI, and a manual secret scan. I corrected the earlier advice to retain `backend/app/` after the final requirement explicitly confirmed that `app/` must be at the repository root.
