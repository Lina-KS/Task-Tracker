# Verification evidence

**Author:** Lina Kassis
**Report:** Task Tracker Feature Development Mid-Course Report

## Baseline check

Before the feature work, `GET /health` returned HTTP 200 with status `ok`. The recorded baseline command and result were:

```powershell
$env:PYTHONPATH = (Resolve-Path 'backend').Path
.\backend\.venv\Scripts\python.exe -m pytest -q

17 passed, 3 warnings in 0.24s
```

Recorded July 23, 2026. The warnings were FastAPI/Starlette dependency deprecations, not failures.

## Final backend test results

- Date: August 6, 2026
- Commit: `75df590`
- Environment: Windows PowerShell, repository virtual environment
- Status: Passed

```powershell
# Run from backend/
$env:PYTHONPATH = (Resolve-Path '.').Path
.\.venv\Scripts\python.exe -m pytest ..\tests -q

...........................                              [100%]
27 passed, 3 warnings in 1.01s
```

Coverage includes due-date validation and clearing, overdue boundaries and combined filters, activity event types, and permanent deletion. The three warnings are FastAPI/Starlette deprecations. This is historical evidence from before the scope correction; current results are recorded below after rerunning the suite.

## Scope-correction validation

- Date: August 10, 2026
- Branch-root suite: `25 passed, 3 warnings in 0.68s`
- Standalone `final-submission/` suite: `25 passed, 3 warnings in 0.57s`
- Runtime check: `GET /health` returned HTTP 200 and the frontend returned HTTP 200.
- Removed capability check: `POST /tasks/missing/restore` returned HTTP 404.

Both suites were run with `python -m pytest ../tests -q` from their respective `backend/` directories using the repository virtual environment. The warnings remain FastAPI/Starlette dependency deprecations. The current suite verifies permanent deletion and the retained `deleted` Activity Log event; it contains no restore or deleted-view tests.

## Manual browser checks

Checks were completed August 6, 2026 in the Codex in-app browser at a 1265-by-720 CSS-pixel viewport against the local frontend and API.

| ID | Check | Result | Evidence |
|---|---|---|---|
| M1 | Created `Report browser verification` with due date `2026-08-08`; the card displayed the date. | Pass | Browser observation |
| M2 | Opened Edit, confirmed the stored date, cleared it, and saved. The card removed the date and activity showed `Updated due_date`. Invalid date rejection is covered by the backend test because the native date control blocks malformed text. | Pass | Browser plus automated test |
| M3 | Enabled Overdue only; exactly the past-due incomplete task remained and all three columns stayed visible. | Pass | Screenshot below |
| M4 | Recent activity displayed created, updated, status-changed, and deleted entries with timestamps. | Pass | Browser observation |

![Overdue filter retains all status columns](evidence/overdue-filter.png)

## Behavior contract before and after refactor

| Behavior | Before | After / invariant |
|---|---|---|
| Existing task CRUD | Existing fields and valid operations worked. | Existing response fields and successful operations remain compatible; new fields are additive. |
| Status transitions | Forward transitions were allowed; forbidden backward transitions were rejected. | The rule remains unchanged. A valid transition adds one activity event; a rejected transition adds none. |
| Task listing | Tasks could be filtered by status and priority with AND logic. | Existing filters retain AND logic; overdue is additive. |
| Deletion | `del _tasks[task_id]` permanently removed the in-memory task. | Permanent deletion remains the behavior and now records one `deleted` activity event with the task ID and title snapshot. |
| Validation/errors | Invalid enums/dates and missing tasks returned client errors. | Failed requests remain non-mutating and create no activity event. |

## Break Test evidence

### BT-1: Overdue boundary and completion exclusion

**Risk:** A naive comparison might mark a task due today or a completed task as overdue.

**Test:** `test_list_tasks_overdue_filter_returns_only_overdue_tasks`

**Deliberate defect introduced:** In `backend/app/models.py`, change the overdue boundary from:

```python
self.due_date < datetime.now(timezone.utc).date()
```

to:

```python
self.due_date <= datetime.now(timezone.utc).date()
```

**Observed failing run:**

```text
FAILED tests/test_tasks.py::test_list_tasks_overdue_filter_returns_only_overdue_tasks
AssertionError: assert ['Overdue high', 'Due today'] == ['Overdue high']
1 failed, 1 warning in 0.25s
```

This failure proves the test detects the exact boundary regression: a task due today incorrectly enters the overdue results.

**Restoration:** Restore `<=` to `<`, then rerun the same focused test.

```powershell
.\.venv\Scripts\python.exe -m pytest `
  ..\tests\test_tasks.py::test_list_tasks_overdue_filter_returns_only_overdue_tasks -q
1 passed, 1 warning in 0.11s
```

The restored implementation excludes the task due today. The same test also combines `overdue=true` with `priority=High`, protecting AND behavior.

### BT-2: Permanent deletion retains an activity event

**Risk:** Permanently removing the task could also erase the audit evidence needed by Activity Log.

**Test:** `test_delete_permanently_removes_task_and_generates_activity_event`

**Deliberate defect introduced:** In `backend/app/storage.py`, temporarily remove this line from `delete_task`:

```python
_record_event(ActivityEventType.DELETED, task, {"title": task.title})
```

**Observed failing run:**

```text
FAILED tests/test_tasks.py::test_delete_permanently_removes_task_and_generates_activity_event
AssertionError: assert 'created' == 'deleted'
1 failed, 1 warning in 0.22s
```

The task was permanently removed, but the newest event remained `created`. This proves the test independently protects the required deletion audit event.

**Restoration:** Put the `_record_event(...)` line back unchanged, then rerun the focused test.

```powershell
.\.venv\Scripts\python.exe -m pytest `
  ..\tests\test_tasks.py::test_delete_permanently_removes_task_and_generates_activity_event -q
1 passed, 1 warning in 0.12s
```

The restored implementation permanently deletes the task and retains the `deleted` event with the original task ID and title snapshot. Both deliberate defects were removed before the final suite run.
