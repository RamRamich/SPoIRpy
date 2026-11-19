# app/api/tasks.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session
from typing import List, Optional

from app.db import get_session
from app import crud
from app.models import Task, TaskCreate, TaskUpdate

router = APIRouter(prefix="/tasks", tags=["Tasks"])

@router.post("/", response_model=Task, status_code=status.HTTP_201_CREATED)
def create_task(
    task_in: TaskCreate, 
    session: Session = Depends(get_session)
):
    """
    Создать новую задачу.
    """
    return crud.create_task(session=session, task_in=task_in)

@router.get("/", response_model=List[Task])
def read_tasks(
    project_id: Optional[int] = None,
    status: Optional[str] = None,
    skip: int = 0,
    limit: int = 100,
    session: Session = Depends(get_session)
):
    """
    Получить список задач.
    Можно фильтровать по `project_id` и `status`, а также использовать пагинацию (`skip`, `limit`).
    """
    return crud.get_tasks(
        session=session, 
        project_id=project_id, 
        status=status, 
        skip=skip, 
        limit=limit
    )

@router.get("/{task_id}", response_model=Task)
def read_task(
    task_id: int, 
    session: Session = Depends(get_session)
):
    """
    Получить задачу по её ID.
    """
    db_task = crud.get_task(session=session, task_id=task_id)
    if db_task is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="Задача не найдена"
        )
    return db_task

@router.patch("/{task_id}", response_model=Task)
def update_task(
    task_id: int, 
    task_in: TaskUpdate, 
    session: Session = Depends(get_session)
):
    """
    Обновить задачу (частично).
    Используем PATCH, так как клиент может прислать только измененные поля (например, только статус).
    """
    db_task = crud.update_task(session=session, task_id=task_id, task_in=task_in)
    if db_task is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="Задача не найдена"
        )
    return db_task

@router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_task(
    task_id: int, 
    session: Session = Depends(get_session)
):
    """
    Удалить задачу по ID.
    """
    success = crud.delete_task(session=session, task_id=task_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="Задача не найдена"
        )
    return None