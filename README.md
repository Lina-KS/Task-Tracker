# Task Tracker

A task-tracking application with a FastAPI backend, a static HTML frontend,
and local JSON-file storage.

## Project structure

```text
backend/            FastAPI application and JSON data
frontend/           Static browser frontend
tests/              Pytest test suite
docs/               Required mid-course Markdown deliverables
```

## Documentation deliverables

The concise mid-course documentation is in `docs/`:

- `user-stories.md`
- `mini-adr.md`
- `prompt-log.md`
- `verification.md`
- `reflection.md`

## Windows PowerShell setup

Run these commands from the project root:

```powershell
cd backend
python -m venv venv
.\venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
Copy-Item .env.example .env
```

If PowerShell prevents the activation script from running, allow scripts only
for the current terminal session, then activate the environment again:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.\venv\Scripts\Activate.ps1
```

Successful activation adds `(venv)` to the beginning of the PowerShell prompt.
The `source` command is for Linux and macOS and does not work in PowerShell.

## Linux/macOS setup

Run these commands from the project root:

```bash
cd backend
python3 -m venv venv
source venv/bin/activate
python -m pip install -r requirements.txt
cp .env.example .env
```

## Run the project locally

The backend and frontend need to run at the same time, so use two terminals.

### 1. Start the backend

In the first terminal, change to `backend`, activate its virtual environment,
and run Uvicorn as a Python module.

Windows PowerShell:

```powershell
cd backend
.\venv\Scripts\Activate.ps1
python -m uvicorn app.main:app --reload --port 8000
```

Linux/macOS:

```bash
cd backend
source venv/bin/activate
python -m uvicorn app.main:app --reload --port 8000
```

If Python reports `No module named uvicorn`, install the backend dependencies
inside the activated environment:

```powershell
python -m pip install -r requirements.txt
```

If startup reports `WinError 10013` or says the address is already in use,
another process may already be using port `8000`. Check it in PowerShell:

```powershell
netstat -ano | Select-String ':8000'
```

The number in the last column is the process ID (PID). If it is an old backend
process, stop it and start Uvicorn again:

```powershell
Stop-Process -Id <PID>
python -m uvicorn app.main:app --reload --port 8000
```

Do not stop the process if it belongs to another application you still need.

The API is available at <http://localhost:8000>. Its interactive Swagger
documentation is at <http://localhost:8000/docs>.

### 2. Open the frontend

In a second terminal, start a static file server from the project root:

```powershell
cd frontend
python -m http.server 5500
```

Then open <http://localhost:5500> in a browser. Keep the backend terminal
running. Do not open `frontend/index.html` directly with a `file://` URL.

## Run the tests

Install the test dependencies once inside the activated backend environment:

```powershell
cd backend
.\venv\Scripts\Activate.ps1
python -m pip install pytest httpx
```

Then run the test suite from the `backend` directory:

```powershell
python -m pytest ../tests
```

The tests use temporary JSON files and do not modify the data in
`backend/data/`.

## Check the API

With the backend running, open <http://localhost:8000/health> or run:

```powershell
Invoke-RestMethod http://localhost:8000/health
```

Expected response shape:

```json
{
  "status": "ok",
  "timestamp": "<current ISO timestamp>"
}
```

To leave the virtual environment, run `deactivate`.
