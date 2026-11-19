# app/crud.py
from typing import Optional, List
from sqlmodel import Session, select
from app.models import (
    User, UserCreate, UserUpdate,
    Task, TaskCreate, TaskUpdate,
    Project, ProjectCreate, ProjectUpdate,
    ProjectMembers, ProjectMembersCreate,
    TaskAssignees, TaskAssigneesCreate,
    TaskRoles, TaskRolesCreate,
    TaskRelations, TaskRelationsCreate,
    Files, FilesCreate
)

# ПОЛЬЗОВАТЕЛИ

def create_user(session: Session, user_in: UserCreate) -> User:
    db_user = User.model_validate(user_in)
    session.add(db_user)
    session.commit()
    session.refresh(db_user)
    return db_user

def get_user(session: Session, user_id: int) -> Optional[User]:
    return session.get(User, user_id)

def get_users(session: Session, project_id: Optional[int] = None, skip: int = 0, limit: int = 100) -> List[User]:
    statement = select(User)
    if project_id is not None:
        # ИСПРАВЛЕНО: используем JOIN, чтобы связать User и ProjectMembers
        statement = statement.join(ProjectMembers, User.id == ProjectMembers.user_id).where(ProjectMembers.project_id == project_id)
    
    statement = statement.offset(skip).limit(limit)
    return session.exec(statement).all()

def update_user(session: Session, user_id: int, user_in: UserUpdate) -> Optional[User]:
    db_user = session.get(User, user_id)
    if not db_user:
        return None
    update_data = user_in.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_user, key, value)
    session.add(db_user)
    session.commit()
    session.refresh(db_user)
    return db_user

def delete_user(session: Session, user_id: int) -> bool:
    db_user = session.get(User, user_id)
    if not db_user:
        return False
    session.delete(db_user)
    session.commit()
    return True

# ЗАДАЧИ

def create_task(session: Session, task_in: TaskCreate) -> Task:
    db_task = Task.model_validate(task_in)
    session.add(db_task)
    session.commit()
    session.refresh(db_task)
    return db_task

def get_task(session: Session, task_id: int) -> Optional[Task]:
    return session.get(Task, task_id)

def get_tasks(session: Session, project_id: Optional[int] = None, status: Optional[str] = None, skip: int = 0, limit: int = 100) -> List[Task]:
    statement = select(Task)
    if project_id is not None:
        statement = statement.where(Task.project_id == project_id)
    if status is not None:
        statement = statement.where(Task.status == status)
    
    statement = statement.offset(skip).limit(limit)
    return session.exec(statement).all()

def update_task(session: Session, task_id: int, task_in: TaskUpdate) -> Optional[Task]:
    db_task = session.get(Task, task_id)
    if not db_task:
        return None
    update_data = task_in.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_task, key, value)
    session.add(db_task)
    session.commit()
    session.refresh(db_task)
    return db_task

def delete_task(session: Session, task_id: int) -> bool:
    db_task = session.get(Task, task_id)
    if not db_task:
        return False
    session.delete(db_task)
    session.commit()
    return True

# ПРОЕКТЫ

def project_create(session: Session, project_in: ProjectCreate) -> Project:
    db_project = Project.model_validate(project_in)
    session.add(db_project)
    session.commit()
    session.refresh(db_project)
    return db_project

def get_project(session: Session, project_id: int) -> Optional[Project]:
    return session.get(Project, project_id)

def get_projects(session: Session, skip: int = 0, limit: int = 100) -> List[Project]:
    statement = select(Project).offset(skip).limit(limit)
    return session.exec(statement).all()

def update_project(session: Session, project_id: int, project_in: ProjectUpdate) -> Optional[Project]:
    # ИСПРАВЛЕНО: session с маленькой буквы, exclude_unset, правильный тип возврата
    db_project = session.get(Project, project_id)
    if not db_project:
        return None
    update_data = project_in.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_project, key, value)
    session.add(db_project)
    session.commit()
    session.refresh(db_project)
    return db_project

def delete_project(session: Session, project_id: int) -> bool:
    db_project = session.get(Project, project_id)
    if not db_project:
        return False
    session.delete(db_project)
    session.commit()
    return True

# УЧАСТНИКИ ПРОЕКТА

def create_project_members(session: Session, project_members_in: ProjectMembersCreate) -> ProjectMembers:
    db_ProjectMembers = ProjectMembers.model_validate(project_members_in)
    session.add(db_ProjectMembers)
    session.commit()
    session.refresh(db_ProjectMembers)
    return db_ProjectMembers

def get_project_members(session: Session, project_id: Optional[int] = None) -> List[ProjectMembers]:
    statement = select(ProjectMembers)
    if project_id is not None:
        statement = statement.where(ProjectMembers.project_id == project_id)
    return session.exec(statement).all()

# ИСПОЛНИТЕЛИ ЗАДАЧ

def create_task_assignes(session: Session, task_assignes_in: TaskAssigneesCreate) -> TaskAssignees:
    db_TaskAssignees = TaskAssignees.model_validate(task_assignes_in)
    session.add(db_TaskAssignees)
    session.commit()
    session.refresh(db_TaskAssignees)
    return db_TaskAssignees

def get_task_assignes(session: Session, task_id: Optional[int] = None) -> List[TaskAssignees]:
    statement = select(TaskAssignees)
    if task_id is not None:
        statement = statement.where(TaskAssignees.task_id == task_id)
    return session.exec(statement).all()

# РОЛИ, КОТОРЫЕ ЗАТРАГИВАЕТ ЗАДАЧА

def create_task_roles(session: Session, task_role_in: TaskRolesCreate) -> TaskRoles:
    db_TaskRoles = TaskRoles.model_validate(task_role_in)
    session.add(db_TaskRoles)
    session.commit()
    session.refresh(db_TaskRoles)
    return db_TaskRoles

def get_task_roles(session: Session, task_id: Optional[int] = None) -> List[TaskRoles]:
    statement = select(TaskRoles)
    if task_id is not None:
        # ИСПРАВЛЕНО: TaskRoles.task_id, а не TaskRoles.task
        statement = statement.where(TaskRoles.task_id == task_id)
    return session.exec(statement).all()

# СВЯЗИ МЕЖДУ ЗАДАЧАМИ

def create_task_relations(session: Session, task_relations_in: TaskRelationsCreate) -> TaskRelations:
    # ИСПРАВЛЕНО: TaskRelations.model_validate, а не TaskRoles
    db_TaskRelations = TaskRelations.model_validate(task_relations_in)
    session.add(db_TaskRelations)
    session.commit()
    session.refresh(db_TaskRelations)
    return db_TaskRelations

def get_task_relations(session: Session, task_id: Optional[int] = None) -> List[TaskRelations]:
    statement = select(TaskRelations)
    if task_id is not None:
        statement = statement.where(TaskRelations.task_id == task_id)
    return session.exec(statement).all()

# ФАЙЛЫ

def create_files(session: Session, files_in: FilesCreate) -> Files:
    db_Files = Files.model_validate(files_in)
    session.add(db_Files)
    session.commit()
    session.refresh(db_Files)
    return db_Files

def get_task_files(session: Session, task_id: Optional[int] = None) -> List[Files]:
    statement = select(Files)
    if task_id is not None:
        statement = statement.where(Files.task_id == task_id)
    return session.exec(statement).all()