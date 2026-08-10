# User stories and acceptance criteria

**Author:** Lina Kassis
**Report:** Task Tracker Feature Development Mid-Course Report

## Feature 1: Due dates and overdue filtering

### US-F1-1: Create a task with a due date

As a team member, I want to set an optional due date while creating a task so that I can plan work against a calendar date.

Acceptance criteria:

- A create request accepts no due date or a valid ISO `YYYY-MM-DD` date.
- The created task response contains the saved due date.
- An invalid date returns HTTP 422 and the frontend displays validation feedback.
- The New Task form includes an optional date input.

### US-F1-2: Change or clear a due date

As a team member, I want to change or clear a task's due date so that its schedule stays accurate.

Acceptance criteria:

- The Edit form displays the current due date.
- A valid replacement is persisted and displayed.
- Explicit `null` clears the date; an omitted field leaves it unchanged.
- Invalid input returns HTTP 422 and does not alter the stored task.

### US-F1-3: Recognize overdue work

As a team member, I want overdue tasks visibly identified so that I can prioritize incomplete work.

Acceptance criteria:

- A task is overdue only when its date is before the current UTC calendar date and its status is not `Done`.
- Tasks due today, without a date, or completed are not overdue.
- The card displays the original due date alongside the overdue indicator.

### US-F1-4: Filter to overdue tasks

As a team member, I want to filter the board to overdue tasks so that I can focus on work needing attention.

Acceptance criteria:

- `GET /tasks?overdue=true` returns only overdue tasks.
- Overdue, status, and priority filters combine using AND logic.
- All three status columns remain visible while filtering.
- Clearing the filter restores the normal list.

**Corrected AI assumption:** An early AI suggestion treated overdue state as a frontend-only calculation. It was corrected because the API must also filter by overdue state. The backend is the single source of truth.

## Feature 2: Activity log

### US-F2-1: Record creation and ordinary updates

As a team member, I want creation and edits recorded so that I can understand how work changed.

Acceptance criteria:

- Creating a task produces exactly one `created` event.
- A successful non-status edit produces exactly one `updated` event identifying changed fields.
- Events contain an ID, task ID, timestamp, type, and details payload.
- Validation failures and missing-task operations create no event.

### US-F2-2: Record status changes

As a team member, I want status activity to show the previous and new state so that workflow movement is understandable.

Acceptance criteria:

- A permitted transition creates one `status_changed` event with `from` and `to` values.
- It does not also create a generic update event.
- Drag-and-drop and form updates follow the same rule.
- A rejected transition returns HTTP 422 and creates no event.

### US-F2-3: Record task deletion

As a team member, I want deletions recorded so that the activity history explains why a task disappeared.

Acceptance criteria:

- Deleting permanently removes the task from storage and the active columns.
- A successful deletion creates one `deleted` event with a task reference and title snapshot.
- Deleting a missing task returns HTTP 404 and creates no event.

### US-F2-4: View recent activity

As a team member, I want to view recent task activity so that I can review important changes.

Acceptance criteria:

- `GET /activity` returns events newest first.
- The frontend displays a readable, read-only activity panel.
- Each item identifies the action and affected task.

**Corrected scope:** Restorable deletion was removed because it was a separate capability beyond the approved Activity Log feature.

## Scope

Authentication, accounts, notifications, real-time updates, mobile features, production databases, ORMs, and frontend frameworks are out of scope.
