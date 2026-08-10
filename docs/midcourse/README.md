# Midcourse documentation

This directory contains the required documentation for the two selected
features: due dates with overdue filtering and Activity Log.

- `user-stories.md`: independently testable stories and acceptance criteria.
- `mini-adr.md`: the implementation decision and rejected alternatives.
- `prompt-log.md`: AI prompts, returned suggestions, and human dispositions.
- `verification.md`: baseline, full-suite, manual, and deliberate Break Test evidence.
- `reflection.md`: reflection on AI assistance and human review.

Restorable deletion is intentionally excluded. DELETE permanently removes a
task while Activity Log retains a `deleted` event containing its ID and title
snapshot.
