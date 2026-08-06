# Verification evidence

## Baseline check
Before feature work, `GET /health` returned HTTP 200 with status `ok`.

```text
17 passed, 3 warnings in 0.24s
```

Recorded July 23, 2026. Warnings were FastAPI/Starlette deprecations.

## Final backend tests
- Date: August 6, 2026
- Commit: `75df590`
- Result: `27 passed, 3 warnings in 1.01s`
- Status: Passed

```powershell
# Run from backend/
$env:PYTHONPATH = (Resolve-Path '.').Path
.\.venv\Scripts\python.exe -m pytest ..\tests -q
```

Coverage includes due-date validation/clearing, overdue boundaries and combined filters, activity event types, soft deletion, restoration, and persistence after storage reload.

## Manual browser checks
Completed August 6, 2026 in the Codex in-app browser against the local frontend/API.

| Check | Result |
|---|---|
| Created a task with a due date; the card displayed it. | Pass |
| Confirmed the date in Edit, cleared it, and saved; activity showed `Updated due_date`. | Pass |
| Overdue only returned the qualifying task while all columns remained visible. | Pass |
| Activity displayed created, updated, status-changed, deleted, and restored entries. | Pass |
| Show deleted displayed a task with a Restore action. | Pass |

## Behavior contract before and after refactor

| Behavior | Before | After / invariant |
|---|---|---|
| CRUD | Existing fields/operations worked. | Existing responses remain compatible; new fields are additive. |
| Status | Forward transitions allowed; backward transitions rejected. | Same rule; valid transitions add one event, rejected ones add none. |
| Listing | Status and priority used AND logic. | Existing logic remains; overdue is additive; deleted tasks are excluded by default. |
| Deletion | `del _tasks[task_id]` permanently removed the task. | Soft deletion is recoverable, persisted, and records one event. |
| Errors | Invalid input and missing tasks returned client errors. | Failed requests remain non-mutating and create no event. |

## Break Test evidence

### BT-1: Overdue boundary and completion exclusion
- Test: `test_list_tasks_overdue_filter_returns_only_overdue_tasks`
- Result: `1 passed`
- Evidence: Only the incomplete task due yesterday is returned; due-today/completed tasks are excluded. Combining priority proves AND behavior.

### BT-2: Deleted state survives storage reload
- Test: `test_deleted_task_state_persists_after_storage_reload`
- Result: `1 passed`
- Evidence: After deletion and reload, the deleted listing returns the same task ID with `is_deleted=true`.
