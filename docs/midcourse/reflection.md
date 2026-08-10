# Reflection

**Author:** Lina Kassis
**Report:** Task Tracker Feature Development Mid-Course Report

I used OpenAI Codex, GitHub Copilot, Claude, and Cursor during the project. Codex supported requirements and tests, Copilot offered inline implementation suggestions, Claude helped compare alternatives, and Cursor supported repository navigation and editing. AI was most useful for turning broad feature descriptions into testable behavior contracts. The due-date request, for example, exposed decisions about date format, the meaning of "overdue," omitted versus null PATCH fields, and filter interactions. This kept the frontend and backend aligned around one rule.

AI helped most when it proposed edge cases that were easy to overlook. One concrete prompt asked for adversarial tests covering yesterday versus today, completed tasks, missing dates, invalid dates, and combined filters. Codex returned a boundary matrix; I retained the due-today and completed-task exclusions and edited the test to combine `overdue=true` with `priority=High`. The activity-log discussion also helped separate ordinary updates from status changes so one operation would not generate duplicate events.

AI also slowed the work when it suggested architecture that was reasonable in general but disproportionate for this project. SQLite with SQLAlchemy would improve concurrency and querying, but adopting it would add models, sessions, migrations, fixtures, and configuration unrelated to the current learning objective. Evaluating and rejecting that suggestion took time. Similarly, a frontend-only overdue calculation looked quick but would have duplicated a rule needed by the API.

My review changed the result in the deletion design. The implementation had expanded Activity Log into a separate restorable-deletion capability with persisted deleted state, a Deleted view, and a restore endpoint. I removed that scope and returned DELETE to permanent removal while retaining one `deleted` activity event after each successful operation. This confirmed that AI suggestions still needed review against the approved feature list, acceptance criteria, project scale, and observed tests.
