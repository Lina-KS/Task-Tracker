import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Optional
from uuid import uuid4

from app.models import (
    ActivityEventType,
    ActivityResponse,
    TaskCreate,
    TaskPriority,
    TaskResponse,
    TaskStatus,
    TaskUpdate,
)

_DATA_DIRECTORY = Path(__file__).resolve().parent / "data"
_TASKS_FILE = _DATA_DIRECTORY / "tasks.json"
_ACTIVITY_FILE = _DATA_DIRECTORY / "activity.json"

_tasks: dict[str, TaskResponse] = {}
_activity: list[ActivityResponse] = []


def _read_records(path: Path) -> list[dict[str, Any]]:
    if not path.exists():
        return []

    try:
        contents = path.read_text(encoding="utf-8")
        records = json.loads(contents) if contents.strip() else []
    except json.JSONDecodeError:
        return []

    return records if isinstance(records, list) else []


def _write_records(path: Path, records: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary_path = path.with_suffix(f"{path.suffix}.tmp")
    temporary_path.write_text(json.dumps(records, indent=2), encoding="utf-8")
    temporary_path.replace(path)


def _save_tasks() -> None:
    _write_records(
        _TASKS_FILE,
        [task.model_dump(mode="json", exclude={"is_overdue"}) for task in _tasks.values()],
    )


def _save_activity() -> None:
    _write_records(
        _ACTIVITY_FILE,
        [event.model_dump(mode="json") for event in _activity],
    )


def _load_storage() -> None:
    global _activity, _tasks

    task_records = _read_records(_TASKS_FILE)
    active_task_records = []
    for record in task_records:
        # Migrate data written by the removed soft-delete feature. Previously
        # deleted tasks stay deleted; active tasks lose the obsolete marker.
        if record.get("is_deleted") is True:
            continue
        active_task_records.append(
            {key: value for key, value in record.items() if key != "is_deleted"}
        )

    _tasks = {
        task.id: task
        for task in (TaskResponse.model_validate(record) for record in active_task_records)
    }
    _activity = [
        ActivityResponse.model_validate(record)
        for record in _read_records(_ACTIVITY_FILE)
        if record.get("event_type") != "restored"
    ]


def _record_event(
    event_type: ActivityEventType,
    task: TaskResponse,
    details: dict[str, Any],
) -> None:
    _activity.append(
        ActivityResponse(
            id=str(uuid4()),
            task_id=task.id,
            event_type=event_type,
            timestamp=datetime.now(timezone.utc),
            details=details,
        )
    )
    _save_activity()


def add_task(payload: TaskCreate) -> TaskResponse:
    now = datetime.now(timezone.utc)
    task = TaskResponse(
        id=str(uuid4()),
        title=payload.title,
        description=payload.description or "",
        status=payload.status,
        priority=payload.priority,
        assignee=payload.assignee,
        due_date=payload.due_date,
        created_at=now,
        updated_at=now,
    )
    _tasks[task.id] = task
    _save_tasks()
    _record_event(ActivityEventType.CREATED, task, {"title": task.title})
    return task


def get_all_tasks(
    status: TaskStatus | None = None,
    priority: TaskPriority | None = None,
    overdue: bool | None = None,
) -> list[TaskResponse]:
    tasks = list(_tasks.values())

    if status is not None:
        tasks = [task for task in tasks if task.status == status]

    if priority is not None:
        tasks = [task for task in tasks if task.priority == priority]

    if overdue is not None:
        tasks = [task for task in tasks if task.is_overdue is overdue]

    return tasks


def get_task_by_id(task_id: str) -> Optional[TaskResponse]:
    return _tasks.get(task_id)


def update_task(task_id: str, payload: TaskUpdate) -> Optional[TaskResponse]:
    task = get_task_by_id(task_id)

    if task is None:
        return None

    updates = payload.model_dump(exclude_unset=True)

    if not updates:
        return task

    if "description" in updates and updates["description"] is None:
        updates["description"] = ""

    updated_task = task.model_copy(
        update={
            **updates,
            "updated_at": datetime.now(timezone.utc),
        }
    )
    _tasks[task_id] = updated_task
    _save_tasks()

    if "status" in updates:
        _record_event(
            ActivityEventType.STATUS_CHANGED,
            updated_task,
            {
                "from_status": task.status.value,
                "to_status": updated_task.status.value,
            },
        )
    else:
        _record_event(
            ActivityEventType.UPDATED,
            updated_task,
            {"changed_fields": sorted(updates)},
        )

    return updated_task


def delete_task(task_id: str) -> bool:
    task = _tasks.pop(task_id, None)

    if task is None:
        return False

    _save_tasks()
    _record_event(ActivityEventType.DELETED, task, {"title": task.title})
    return True


def get_activity() -> list[ActivityResponse]:
    return sorted(_activity, key=lambda event: event.timestamp, reverse=True)


def _configure_storage(tasks_file: Path, activity_file: Path) -> tuple[Path, Path]:
    global _ACTIVITY_FILE, _TASKS_FILE

    previous_paths = (_TASKS_FILE, _ACTIVITY_FILE)
    _TASKS_FILE = tasks_file
    _ACTIVITY_FILE = activity_file
    _load_storage()
    return previous_paths


def _restore_storage(paths: tuple[Path, Path]) -> None:
    global _ACTIVITY_FILE, _TASKS_FILE

    _TASKS_FILE, _ACTIVITY_FILE = paths
    _load_storage()


def _reload_for_tests() -> None:
    _load_storage()


def _reset() -> None:
    _tasks.clear()
    _activity.clear()
    _save_tasks()
    _save_activity()


_load_storage()
