from fastapi import APIRouter, Depends, Query, status
from prisma import Prisma
from typing import Optional

from app.core.dependencies import get_current_user
from app.core.envelope import ok
from app.db.client import get_db
from app.modules.activity import service
from app.modules.activity.schemas import ActivityCreate, ReminderCreate, TaskCreate, TaskUpdate

router = APIRouter(tags=["activities"])


@router.post("/activities", status_code=status.HTTP_201_CREATED)
async def log_activity(body: ActivityCreate, db: Prisma = Depends(get_db),
                       current_user=Depends(get_current_user)) -> dict:
    return ok((await service.log_activity(db, body, current_user.id)).__dict__)


@router.get("/activities")
async def list_activities(related_type: Optional[str] = None, related_id: Optional[str] = None,
                           page: int = Query(1, ge=1), page_size: int = Query(20, ge=1, le=100),
                           db: Prisma = Depends(get_db), current_user=Depends(get_current_user)) -> dict:
    activities, total = await service.list_activities(db, related_type, related_id, page, page_size)
    return ok([a.__dict__ for a in activities], meta={"total": total})


@router.post("/tasks", status_code=status.HTTP_201_CREATED)
async def create_task(body: TaskCreate, db: Prisma = Depends(get_db),
                      current_user=Depends(get_current_user)) -> dict:
    return ok((await service.create_task(db, body, current_user.id)).__dict__)


@router.get("/tasks")
async def list_tasks(assignee_id: Optional[str] = None, status: Optional[str] = None,
                     page: int = Query(1, ge=1), page_size: int = Query(20, ge=1, le=100),
                     db: Prisma = Depends(get_db), current_user=Depends(get_current_user)) -> dict:
    tasks, total = await service.list_tasks(db, assignee_id, status, page, page_size)
    return ok([t.__dict__ for t in tasks], meta={"total": total})


@router.get("/tasks/overdue")
async def overdue_tasks(assignee_id: Optional[str] = None, db: Prisma = Depends(get_db),
                        current_user=Depends(get_current_user)) -> dict:
    tasks = await service.get_overdue_tasks(db, assignee_id)
    return ok([t.__dict__ for t in tasks])


@router.get("/tasks/{task_id}")
async def get_task(task_id: str, db: Prisma = Depends(get_db),
                   current_user=Depends(get_current_user)) -> dict:
    return ok((await service.get_task(db, task_id)).__dict__)


@router.patch("/tasks/{task_id}")
async def update_task(task_id: str, body: TaskUpdate, db: Prisma = Depends(get_db),
                      current_user=Depends(get_current_user)) -> dict:
    return ok((await service.update_task(db, task_id, body, current_user.id)).__dict__)


@router.delete("/tasks/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_task(task_id: str, db: Prisma = Depends(get_db),
                      current_user=Depends(get_current_user)) -> None:
    await service.delete_task(db, task_id, current_user.id)


@router.post("/reminders", status_code=status.HTTP_201_CREATED)
async def create_reminder(body: ReminderCreate, db: Prisma = Depends(get_db),
                          current_user=Depends(get_current_user)) -> dict:
    return ok((await service.create_reminder(db, body)).__dict__)
