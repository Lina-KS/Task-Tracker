# Working agreement for AI-assisted changes

These instructions apply to the entire repository.

## Read first and project stack

- Read `README.md`, relevant files under `docs/`, and existing tests before editing. Prefer a documentation correction when behavior is already correct.
- The stack is FastAPI/Pydantic in `app/`, JSON storage in `app/data/`, a static HTML/CSS/JavaScript frontend in `frontend/`, and pytest tests in `tests/`.
- Preserve the root-level final-project structure and do not create duplicate project copies.

## Scope and safety

- Keep this a small Task Tracker. Do not add authentication, comments, notifications, a production database, or unrelated UI features.
- Treat `app/` and `frontend/` as protected product code. Change them only for a demonstrated bug, security issue, or documented correction, and record the reason in `docs/final-ai-review.md`.
- Never place secrets, `.env` contents, tokens, production logs, or real personal/customer data in prompts, commits, tests, or documentation.
- Do not weaken tests, validation, TLS checks, container permissions, or CI failure behavior.

## Required validation

- Run the API from the repository root with `python -m uvicorn app.main:app --reload --port 8000`.
- Run the frontend from `frontend/` with `python -m http.server 5500`.
- Run `python -m pytest tests -q` from the repository root after Python changes.
- After Docker changes, run `docker build -t task-tracker:final .`, start the container, and verify `GET /health` returns HTTP 200 before claiming success.
- Review the diff manually and keep only lines you can explain.

## Review expectations

- Grade AI findings and cite file or command evidence.
- Record failures, warnings, and blocked checks honestly.
- Prefer the smallest change that satisfies the requirement and preserves behavior.
