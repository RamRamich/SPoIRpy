# app/routers/tasks.py
from fastapi import APIRouter
from pydantic import BaseModel
from app.db import get_pool_conn

class UpdateTask(BaseModel):
    title: str = ""
    description: str = ""
    priority: str ="medium"
    status: str = "backlog"

class CreateTask(BaseModel):
    creator_id: int
    project_id: int
    title: str
    description: str = ""
    priority: str ="medium"
    status: str = "backlog"

# Создаем экземпляр роутера.
# prefix="/task" — это пространство имен. Все маршруты в этом файле 
# автоматически получат этот префикс.
# tags=["task"] — нужно для группировки в автоматической документации (Swagger UI).
router = APIRouter(
    prefix="/api/tasks",
    tags=["Tasks"]
)

@router.get("") 
def get_tasks():
    conn = get_pool_conn()
    try:
        cur = conn.cursor()
        cur.execute("SELECT * FROM tasks")
        tasks = cur.fetchall()
    except Exception as e:
        conn.rollback()   # ← ОТКАТ при ошибке
        return {"error": str(e)}
    finally:
        conn.close()
    return tasks 

@router.post("") 
def post_tasks(
    task : CreateTask
):
    conn = get_pool_conn()
    try:
        cur = conn.cursor()
        cur.execute(
            "INSERT INTO tasks (creator_id, project_id, title, description, priority, status) "
            "VALUES (%s, %s, %s,%s,%s,%s)",
            (task.creator_id, task.project_id, task.title, task.description,task.priority, task.status)
        )
        conn.commit()
    except Exception as e:
        conn.rollback()   # ← ОТКАТ при ошибке
        return {"error": str(e)}
    finally:
        conn.close()
    return {"status": "ok"}

@router.put("/{task_id}") 
def update_task(
    task_id: int, task : UpdateTask
):
    conn = get_pool_conn()
    try:
        cur = conn.cursor()
        cur.execute(
            "UPDATE tasks "
            "SET title = %s, description = %s, status = %s, priority = %s "
            "WHERE id = %s",
            (task.title, task.description, task.priority, task.status, task_id)
        )
        conn.commit()
    except Exception as e:
        conn.rollback()   # ← ОТКАТ при ошибке
        return {"error": str(e)}
    finally:
        conn.close()
    return {"status": "ok"}

@router.delete("/{task_id}") 
def delete_task(task_id: int):
    conn = get_pool_conn()
    try:
        cur = conn.cursor()
        cur.execute("DELETE FROM tasks WHERE id = %s", (task_id,))
        conn.commit()
    except Exception as e:
        conn.rollback()   # ← ОТКАТ при ошибке
        return {"error": str(e)}
    finally:
        conn.close()
    return {"status": "ok"}