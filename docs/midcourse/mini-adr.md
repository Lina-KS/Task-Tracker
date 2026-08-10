# Mini ADR: Task extensions in JSON storage

**Author:** Lina Kassis
**Status:** Accepted and implemented
**Decision date:** July 26, 2026

## Context

The Task Tracker needed due dates, overdue filtering, and activity history without introducing production-scale infrastructure. Browser and API behavior needed one shared overdue rule, while successful task changes needed a durable audit trail.

## Decision

The implementation extends the existing JSON storage layer:

- Tasks store an optional ISO `YYYY-MM-DD` due date.
- The backend determines overdue state and supports `GET /tasks?overdue=true`.
- Existing status, priority, and overdue filters combine using AND logic.
- `GET /activity` returns events newest first.
- Successful create, ordinary update, status change, and permanent delete operations each record one event. Invalid, rejected, or missing-task operations record none.

## Alternatives suggested by AI

- SQLite with SQLAlchemy for stronger querying and transaction support.
- Frontend-only overdue calculation for a smaller UI-only change.
- Permanent deletion with a retained activity event.
- Separate activity endpoints for individual tasks.

## Rejected or deferred

- **SQLite/SQLAlchemy:** rejected as too complex because it requires additional configuration and test setup.
- **Frontend-only overdue logic:** rejected because browser and API filtering could disagree.
- **Restorable deletion:** rejected because it is a separate product capability outside the approved Activity Log scope.
- **Per-task activity endpoints:** deferred because one read-only recent feed meets the current scope.
- Authentication, notifications, real-time updates, and a frontend framework remain out of scope.

## Consequences

The project remains locally runnable with few dependencies, and business rules are consistent across the API and browser. JSON persistence is not suitable for high-volume concurrent writes and should be reconsidered if production-scale requirements are introduced.
