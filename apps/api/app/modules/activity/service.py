from datetime import datetime, timezone
from prisma import Prisma
from app.core.audit import record_audit
from app.core.enums import TaskStatus
from app.middleware.error_handler import NotFoundError
from app.modules.activity.schemas import ActivityCreate, ReminderCreate, TaskCreate, TaskUpdate


async def log_activity(db: Prisma, body: ActivityCreate, user_id: str) -> object:
    data = body.model_dump(exclude_none=True)
    data["userId"] = user_id
    activity = await db.activity.create(data=data)
    await record_audit(db, user_id, "CREATE", "activities", record_id=activity.id)
    return activity


async def list_activities(db: Prisma, related_type: str | None, related_id: str | None,
                          page: int, page_size: int) -> tuple[list, int]:
    where: dict = {}
    if related_type:
        where["relatedType"] = related_type
    if related_id:
        where["relatedId"] = related_id
    skip = (page - 1) * page_size
    activities = await db.activity.find_many(where=where, skip=skip, take=page_size,
                                             order={"happenedAt": "desc"})
    total = await db.activity.count(where=where)
    return activities, total


async def create_task(db: Prisma, body: TaskCreate, creator_id: str) -> object:
    data = body.model_dump(exclude_none=True)
    data["createdById"] = creator_id
    if "assigneeId" not in data:
        data["assigneeId"] = creator_id
    task = await db.task.create(data=data)
    await record_audit(db, creator_id, "CREATE", "tasks", record_id=task.id)
    return task


async def get_task(db: Prisma, task_id: str) -> object:
    task = await db.task.find_first(where={"id": task_id, "deletedAt": None})
    if not task:
        raise NotFoundError(f"Task {task_id} not found")
    return task


async def list_tasks(db: Prisma, assignee_id: str | None, status: str | None,
                     page: int, page_size: int) -> tuple[list, int]:
    where: dict = {"deletedAt": None}
    if assignee_id:
        where["assigneeId"] = assignee_id
    if status:
        where["status"] = status
    skip = (page - 1) * page_size
    tasks = await db.task.find_many(where=where, skip=skip, take=page_size,
                                    order={"dueAt": "asc"})
    total = await db.task.count(where=where)
    return tasks, total


async def update_task(db: Prisma, task_id: str, body: TaskUpdate, actor_id: str) -> object:
    task = await db.task.find_first(where={"id": task_id, "deletedAt": None})
    if not task:
        raise NotFoundError(f"Task {task_id} not found")
    data = body.model_dump(exclude_none=True)
    updated = await db.task.update(where={"id": task_id}, data=data)
    await record_audit(db, actor_id, "UPDATE", "tasks", record_id=task_id, new_values=data)
    return updated


async def delete_task(db: Prisma, task_id: str, actor_id: str) -> None:
    task = await db.task.find_first(where={"id": task_id, "deletedAt": None})
    if not task:
        raise NotFoundError(f"Task {task_id} not found")
    await db.task.update(where={"id": task_id},
                         data={"deletedAt": datetime.now(timezone.utc)})
    await record_audit(db, actor_id, "DELETE", "tasks", record_id=task_id)


async def create_reminder(db: Prisma, body: ReminderCreate) -> object:
    return await db.reminder.create(data={
        "taskId": body.taskId,
        "remindAt": body.remindAt,
    })


async def get_overdue_tasks(db: Prisma, assignee_id: str | None) -> list:
    where: dict = {
        "deletedAt": None,
        "status": {"not": TaskStatus.COMPLETED},
        "dueAt": {"lt": datetime.now(timezone.utc)},
    }
    if assignee_id:
        where["assigneeId"] = assignee_id
    return await db.task.find_many(where=where, order={"dueAt": "asc"})
