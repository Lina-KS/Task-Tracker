# User stories and acceptance criteria

## Feature 1: Due dates and overdue filtering

### US-F1-1: Create a task with a due date
As a team member, I want to set an optional due date while creating a task so that I can plan work against a calendar date.

Acceptance criteria:
- Accept no date or a valid `YYYY-MM-DD` date.
- Return the saved date in the created task.
- Reject invalid dates with HTTP 422.
- Include an optional date input in the New Task form.

### US-F1-2: Change or clear a due date
As a team member, I want to change or clear a task's due date so that its schedule stays accurate.

Acceptance criteria:
- Show the current date in Edit.
- Persist a valid replacement.
- Treat explicit `null` as clear and omission as unchanged.
- Reject invalid input without altering the task.

### US-F1-3: Recognize overdue work
As a team member, I want overdue tasks visibly identified so that I can prioritize incomplete work.

Acceptance criteria:
- Overdue means before the current UTC calendar date and not `Done`.
- Due-today, no-date, and completed tasks are not overdue.
- Display the due date beside the overdue indicator.

### US-F1-4: Filter to overdue tasks
As a team member, I want to filter the board to overdue tasks so that I can focus on work needing attention.

Acceptance criteria:
- `GET /tasks?overdue=true` returns only overdue tasks.
- Filters combine with AND logic.
- All status columns remain visible.
- Clearing the filter restores the normal list.

**Corrected AI assumption:** Frontend-only overdue calculation was replaced with a backend source of truth because the API must also filter by overdue state.

## Feature 2: Activity log and restorable deletion

### US-F2-1: Record creation and ordinary updates
As a team member, I want creation and edits recorded so that I can understand how work changed.

Acceptance criteria:
- Create exactly one `created` event per task creation.
- Create exactly one `updated` event per successful non-status edit.
- Include event ID, task ID, timestamp, type, and details.
- Failed operations create no event.

### US-F2-2: Record status changes
As a team member, I want status activity to show the previous and new state.

Acceptance criteria:
- Create one `status_changed` event with previous/new values.
- Do not create a duplicate generic event.
- Apply the same rule to drag-and-drop and form updates.
- Rejected transitions create no event.

### US-F2-3: Soft-delete a task
As a team member, I want deleted tasks removed from active work without losing them permanently.

Acceptance criteria:
- Remove deleted tasks from normal results and active columns.
- Keep them accessible through a Deleted view.
- Create one `deleted` event after success.
- A missing task returns HTTP 404 and creates no event.

### US-F2-4: Restore a deleted task
As a team member, I want to restore a deleted task so it can return to active work.

Acceptance criteria:
- Restore existing task data to normal results.
- Reject missing or active tasks clearly.
- Create one `restored` event.
- Persist deleted/restored state across storage reloads.

### US-F2-5: View recent activity
As a team member, I want to view recent activity so I can review important changes.

Acceptance criteria:
- Return events newest first from `GET /activity`.
- Display a readable, read-only activity panel.
- Identify the action and affected task.

**Corrected AI assumption:** Permanent deletion was replaced with persistent soft deletion because restoration is required.

## Scope
Authentication, accounts, notifications, real-time updates, production databases, ORMs, and frontend frameworks are out of scope.
