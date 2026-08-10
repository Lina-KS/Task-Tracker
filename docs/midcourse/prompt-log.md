# Prompt log

**Author:** Lina Kassis
**Report:** Task Tracker Feature Development Mid-Course Report

## Feature 1: Due dates and overdue filtering

### Prompt F1-P1: Requirements decomposition

**Prompt:** Break the due-date and overdue-filter feature into independently testable user stories. Include create, edit/clear, visual state, filtering, boundary dates, and acceptance criteria.

**AI return:** Four stories covering date creation, modification, overdue display, and server-side filtering.

**Accepted, edited, or rejected:** The story split and ISO-date validation were accepted. The overdue definition was edited to use the current UTC calendar date and explicitly exclude `Done` tasks.

### Prompt F1-P2: Weak prompt rewritten

**Weak prompt:** Add due dates.

**Why it was weak:** It did not identify the affected layers, date format, overdue rule, update semantics, failure behavior, or tests.

**Stronger prompt:** Extend the FastAPI/Pydantic task model and vanilla-JavaScript UI with an optional `due_date` in `YYYY-MM-DD` form. In PATCH, omission must preserve the value and explicit null must clear it. Define overdue as before today's UTC date and not Done; support `GET /tasks?overdue=true`; keep existing status/priority filters with AND behavior; add boundary and validation tests. Do not add a database or frontend framework.

**AI return:** Coordinated model, route, business-rule, UI, storage, and test changes.

**Accepted, edited, or rejected:** The cross-layer checklist was accepted. Client-only overdue calculation was rejected so the backend remains the source of truth.

### Prompt F1-P3: Break-test design

**Prompt:** Design adversarial tests for overdue behavior, especially today versus yesterday, completed tasks, missing dates, invalid dates, and combinations with status and priority filters.

**AI return:** Positive, negative, and boundary cases with expected response codes and result sets.

**Accepted, edited, or rejected:** Boundary and validation cases were accepted. The test `test_list_tasks_overdue_filter_returns_only_overdue_tasks` retains the due-today and completed-task exclusions and combines overdue with priority to prove AND behavior. Broader time-zone simulation was rejected because the contract uses calendar dates.

## Feature 2: Activity log

### Prompt F2-P1: Event contract

**Prompt:** Propose a minimal activity-event contract for create, ordinary update, status change, and permanent delete. Require exactly one event per successful operation and no event for rejected operations.

**AI return:** Event IDs, task references, timestamps, event types, and small type-specific details.

**Accepted, edited, or rejected:** The common fields and single-event rule were accepted. Status events were edited to include explicit previous/new values and not create a duplicate generic update event.

### Prompt F2-P2: Persistence decision

**Prompt:** Compare JSON persistence and SQLite/SQLAlchemy for a small local FastAPI learning project that must retain activity across restarts. Recommend the smallest design consistent with ADR-001.

**AI return:** SQLite was described as more robust, while JSON was identified as consistent with the existing architecture and scope.

**Accepted, edited, or rejected:** JSON persistence was accepted. SQLite and the ORM were rejected as too complex because they require additional configuration and test setup.

### Prompt F2-P3: Failure and activity tests

**Prompt:** Create break tests for permanent deletion, duplicate activity events, invalid status transitions, and missing task IDs. State the invariant each test protects.

**AI return:** Tests inspecting API results and persisted/event state after operations.

**Accepted, edited, or rejected:** Permanent-delete coverage, one event per successful operation, and rejected-transition and missing-ID tests were retained. Restore and deleted-state persistence tests were removed as out of scope.
