# Prompt log

## Feature 1: Due dates and overdue filtering

### F1-P1: Requirements decomposition
**Prompt:** Break the feature into independently testable stories covering create, edit/clear, visual state, filtering, boundaries, and acceptance criteria.

**AI returned:** Four stories covering creation, modification, overdue display, and server-side filtering.

**Decision:** Accepted the split and ISO dates; edited overdue to use the current UTC calendar date and exclude `Done` tasks.

### F1-P2: Weak prompt rewritten
**Weak prompt:** Add due dates.

**Stronger prompt:** Extend the FastAPI/Pydantic model and vanilla-JavaScript UI with optional `due_date` in `YYYY-MM-DD` form. PATCH omission preserves it; explicit null clears it. Define overdue as before today's UTC date and not Done; support `overdue=true`; preserve AND filters; add tests; do not add a database or framework.

**AI returned:** Coordinated model, API, UI, storage, and test changes.

**Decision:** Accepted the cross-layer checklist; rejected client-only overdue calculation.

### F1-P3: Break tests
**Prompt:** Design tests for yesterday versus today, completed tasks, missing/invalid dates, and combined filters.

**AI returned:** Boundary and negative cases with expected results.

**Decision:** Retained due-today/completed exclusions and combined overdue with priority. Rejected broader time-zone simulation as unnecessary for calendar dates.

## Feature 2: Activity log and restorable deletion

### F2-P1: Event contract
**Prompt:** Propose a minimal contract for create, ordinary update, status change, soft delete, and restore, with one event per successful operation and none for rejected operations.

**AI returned:** IDs, task references, timestamps, types, and small details payloads.

**Decision:** Accepted common fields; edited status events to include previous/new values and prevent duplicate generic events.

### F2-P2: Persistence decision
**Prompt:** Compare JSON with SQLite/SQLAlchemy for a local FastAPI project that must retain deleted tasks and activity across reloads.

**AI returned:** SQLite was more robust; JSON matched the existing architecture and scope.

**Decision:** Accepted JSON; rejected SQLite/ORM as too complex due to configuration and test setup.

### F2-P3: Failure and recovery tests
**Prompt:** Create tests for soft deletion, restore, reload persistence, duplicate events, invalid transitions, and missing IDs.

**AI returned:** API and persisted-state tests.

**Decision:** Retained delete/list/restore, event, transition, missing-ID, and persistence tests. Simplified full process restart to storage reload because the JSON storage module owns persistence.
