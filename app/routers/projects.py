# app/routers/projects.py
from fastapi import APIRouter
from pydantic import BaseModel
from app.db import get_pool_conn


class CreateProject(BaseModel):
    name: str
    description: str = ""
    owner_id: int


class UpdateProject(BaseModel):
    name: str = ""
    description: str = ""
    owner_id: int = 0


router = APIRouter(
    prefix="/api/projects",
    tags=["Projects"]
)


@router.get("")
def get_projects():
    conn = get_pool_conn()
    try:
        cur = conn.cursor()
        cur.execute("SELECT * FROM projects")
        projects = cur.fetchall()
    except Exception as e:
        conn.rollback()
        return {"error": str(e)}
    finally:
        conn.close()
    return projects


@router.post("")
def post_projects(project: CreateProject):
    conn = get_pool_conn()
    try:
        cur = conn.cursor()
        cur.execute(
            "INSERT INTO projects (name, description, owner_id) "
            "VALUES (%s, %s, %s)",
            (project.name, project.description, project.owner_id)
        )
        conn.commit()
    except Exception as e:
        conn.rollback()
        return {"error": str(e)}
    finally:
        conn.close()
    return {"status": "ok"}


@router.put("/{project_id}")
def update_project(project_id: int, project: UpdateProject):
    conn = get_pool_conn()
    try:
        cur = conn.cursor()
        cur.execute(
            "UPDATE projects "
            "SET name = %s, description = %s, owner_id = %s "
            "WHERE id = %s",
            (project.name, project.description, project.owner_id, project_id)
        )
        conn.commit()
    except Exception as e:
        conn.rollback()
        return {"error": str(e)}
    finally:
        conn.close()
    return {"status": "ok"}


@router.delete("/{project_id}")
def delete_project(project_id: int):
    conn = get_pool_conn()
    try:
        cur = conn.cursor()
        cur.execute("DELETE FROM projects WHERE id = %s", (project_id,))
        conn.commit()
    except Exception as e:
        conn.rollback()
        return {"error": str(e)}
    finally:
        conn.close()
    return {"status": "ok"}