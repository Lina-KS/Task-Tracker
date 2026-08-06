# Mini ADR: Task extensions in JSON storage

**Status:** Accepted and implemented  
**Decision date:** July 26, 2026

## Context
The Task Tracker needed due dates, overdue filtering, activity history, and restorable deletion without production-scale infrastructure. The browser and API needed one overdue rule, and deleted state needed to survive reloads.

## Decision
- Keep tasks and activity in the existing JSON storage layer.
- Store optional ISO due dates and an `is_deleted` flag.
- Compute overdue in the backend; combine filters with AND logic.
- Exclude deleted tasks from normal results and expose them with `deleted=true`.
- Restore through `POST /tasks/{task_id}/restore`.
- Return newest-first events from `GET /activity`.
- Record one event per successful create, ordinary update, status change, delete, or restore; failed operations record none.

## AI alternatives and disposition
- **SQLite/SQLAlchemy:** rejected as too complex because it adds configuration and test setup.
- **Frontend-only overdue logic:** rejected because browser and API filtering could disagree.
- **Permanent deletion:** rejected because restoration is required.
- **Per-task activity endpoints:** deferred because one recent feed meets the scope.
- Authentication, notifications, real-time updates, and a frontend framework remain out of scope.

## Consequences
The project remains locally runnable with few dependencies. JSON persistence is unsuitable for high-volume concurrent writes.
