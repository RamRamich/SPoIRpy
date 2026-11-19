# app/models.py
from typing import Optional, Literal
from datetime import datetime
from sqlmodel import SQLModel, Field
from sqlalchemy import Column, DateTime, text, String

# 1. ПОЛЬЗОВАТЕЛИ (users)
GlobalRole = Literal["admin", "user"]
DefaultRole = Literal["programmer", "artist", "sound", "designer", "qa", "lead"]

class UserBase(SQLModel):
    username: str = Field(max_length=50)
    email: str = Field(max_length=255)
    password_hash: str = Field(max_length=255)
    full_name: str = Field(max_length=100)
    avatar_url: Optional[str] = Field(default=None, max_length=500)
    
    global_role: GlobalRole = Field(
        default="user", 
        sa_column=Column(String(20), nullable=False)
    )
    default_role: Optional[DefaultRole] = Field(
        default=None, 
        sa_column=Column(String(30), nullable=True)
    )

class User(UserBase, table=True):
    __tablename__ = "users"
    id: Optional[int] = Field(default=None, primary_key=True)
    created_at: Optional[datetime] = Field(
        default=None, 
        sa_column=Column(DateTime, server_default=text("CURRENT_TIMESTAMP"))
    )

class UserCreate(UserBase):
    pass

class UserUpdate(SQLModel):
    username: Optional[str] = None
    email: Optional[str] = None
    full_name: Optional[str] = None
    avatar_url: Optional[str] = None
    global_role: Optional[GlobalRole] = None
    default_role: Optional[DefaultRole] = None

# 2. ПРОЕКТЫ (projects)
class ProjectBase(SQLModel):
    name: str = Field(max_length=100)
    description: Optional[str] = None
    owner_id: int = Field(foreign_key="users.id")
    deadline: Optional[datetime] = None

class Project(ProjectBase, table=True):
    __tablename__ = "projects"
    id: Optional[int] = Field(default=None, primary_key=True)
    created_at: Optional[datetime] = Field(
        default=None, 
        sa_column=Column(DateTime, server_default=text("CURRENT_TIMESTAMP"))
    )

class ProjectCreate(ProjectBase):
    pass

class ProjectUpdate(SQLModel):
    name: Optional[str] = None
    owner_id: Optional[int] = None
    description: Optional[str] = None
    deadline: Optional[datetime] = None

# 3. ЗАДАЧИ (tasks)
Priority = Literal["low", "medium", "high", "critical"]
Status = Literal["backlog", "todo", "in_progress", "review", "done"]

class TaskBase(SQLModel):
    project_id: int = Field(foreign_key="projects.id")
    description: Optional[str] = None
    title: str = Field(max_length=200)
    technical_spec: Optional[str] = None
    creator_id: int = Field(foreign_key="users.id")
    estimated_hours: Optional[float] = None
    due_date: Optional[datetime] = None
    
    priority: Priority = Field(
        default="medium",
        sa_column=Column(String(10), nullable=False)
    )
    status: Status = Field(
        default="backlog",
        sa_column=Column(String(20), nullable=False)
    )

class Task(TaskBase, table=True):
    __tablename__ = "tasks"
    id: Optional[int] = Field(default=None, primary_key=True)
    created_at: Optional[datetime] = Field(
        default=None, 
        sa_column=Column(DateTime, server_default=text("CURRENT_TIMESTAMP"))
    )

class TaskCreate(TaskBase):
    pass

class TaskUpdate(SQLModel):
    description: Optional[str] = None
    title: Optional[str] = None
    technical_spec: Optional[str] = None
    estimated_hours: Optional[float] = None
    due_date: Optional[datetime] = None
    priority: Optional[Priority] = None
    status: Optional[Status] = None

# 4. УЧАСТНИКИ ПРОЕКТА (project_members)
class ProjectMembers(SQLModel, table=True):
    __tablename__ = "project_members"
    id: Optional[int] = Field(default=None, primary_key=True)
    project_id: int = Field(foreign_key="projects.id")
    user_id: int = Field(foreign_key="users.id")
    role: str = Field(max_length=30)
    joined_at: Optional[datetime] = Field(
        default=None, 
        sa_column=Column(DateTime, server_default=text("CURRENT_TIMESTAMP"))
    )

class ProjectMembersCreate(SQLModel):
    project_id: int
    user_id: int
    role: str

# 5. ИСПОЛНИТЕЛИ ЗАДАЧ (task_assignees)
class TaskAssignees(SQLModel, table=True):
    __tablename__ = "task_assignees"
    id: Optional[int] = Field(default=None, primary_key=True)
    task_id: int = Field(foreign_key="tasks.id")
    user_id: int = Field(foreign_key="users.id")
    role_in_task: Optional[str] = Field(default=None, max_length=30)
    assigned_at: Optional[datetime] = Field(
        default=None, 
        sa_column=Column(DateTime, server_default=text("CURRENT_TIMESTAMP"))
    )

class TaskAssigneesCreate(SQLModel):
    task_id: int
    user_id: int
    role_in_task: Optional[str] = None

# 6. РОЛИ, КОТОРЫЕ ЗАТРАГИВАЕТ ЗАДАЧА (task_roles)
class TaskRoles(SQLModel, table=True):
    __tablename__ = "task_roles"
    id: Optional[int] = Field(default=None, primary_key=True)
    task_id: int = Field(foreign_key="tasks.id")
    role: str = Field(max_length=30)

class TaskRolesCreate(SQLModel):
    task_id: int
    role: str

# 7. СВЯЗИ МЕЖДУ ЗАДАЧАМИ (task_relations)
class TaskRelations(SQLModel, table=True):
    __tablename__ = "task_relations"
    id: Optional[int] = Field(default=None, primary_key=True)
    task_id: int = Field(foreign_key="tasks.id")
    related_task_id: int = Field(foreign_key="tasks.id")
    relation_type: str = Field(default="relates_to", max_length=20)

class TaskRelationsCreate(SQLModel):
    task_id: int
    related_task_id: int
    relation_type: str

# 8. ФАЙЛЫ (files)
class Files(SQLModel, table=True):
    __tablename__ = "files"
    id: Optional[int] = Field(default=None, primary_key=True)
    task_id: int = Field(foreign_key="tasks.id") 
    uploaded_by: int = Field(foreign_key="users.id")
    file_name: str = Field(max_length=255)
    file_path: str = Field(max_length=500)
    mime_type: Optional[str] = Field(default=None, max_length=100)
    file_size: Optional[int] = None
    uploaded_at: Optional[datetime] = Field(
        default=None, 
        sa_column=Column(DateTime, server_default=text("CURRENT_TIMESTAMP"))
    )

class FilesCreate(SQLModel):
    task_id: int
    uploaded_by: int
    file_name: str
    file_path: str
    mime_type: Optional[str] = None
    file_size: Optional[int] = None