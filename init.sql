-- База данных: appDB (создаётся автоматически через MYSQL_DATABASE)
-- СУБД: MySQL 8.0+
-- Кодировка: utf8mb4

-- 1. ПОЛЬЗОВАТЕЛИ
CREATE TABLE IF NOT EXISTS users (
    id              BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
    username        VARCHAR(50)     NOT NULL,
    email           VARCHAR(255)    NOT NULL,
    password_hash   VARCHAR(255)    NOT NULL,
    full_name       VARCHAR(100)    NOT NULL,
    avatar_url      VARCHAR(500)    DEFAULT NULL,
    global_role     VARCHAR(20)     NOT NULL DEFAULT 'user',
    default_role    VARCHAR(30)     DEFAULT NULL,
    created_at      TIMESTAMP       NOT NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (id),
    UNIQUE KEY uq_users_username (username),
    UNIQUE KEY uq_users_email (email),
    CONSTRAINT chk_users_global_role
        CHECK (global_role IN ('admin', 'user')),
    CONSTRAINT chk_users_default_role
        CHECK (default_role IS NULL OR default_role IN
            ('programmer', 'artist', 'sound', 'designer', 'qa', 'lead'))
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- 2. ПРОЕКТЫ
CREATE TABLE IF NOT EXISTS projects (
    id              BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
    name            VARCHAR(100)    NOT NULL,
    description     TEXT            DEFAULT NULL,
    owner_id        BIGINT UNSIGNED NOT NULL,
    deadline        DATETIME        DEFAULT NULL,
    created_at      TIMESTAMP       NOT NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (id),
    KEY idx_projects_owner (owner_id),
    CONSTRAINT fk_projects_owner
        FOREIGN KEY (owner_id) REFERENCES users(id)
        ON DELETE RESTRICT ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- 3. УЧАСТНИКИ ПРОЕКТА
CREATE TABLE IF NOT EXISTS project_members (
    id              BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
    project_id      BIGINT UNSIGNED NOT NULL,
    user_id         BIGINT UNSIGNED NOT NULL,
    role            VARCHAR(30)     NOT NULL,
    joined_at       TIMESTAMP       NOT NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (id),
    UNIQUE KEY uq_project_members (project_id, user_id),
    KEY idx_project_members_user (user_id),
    CONSTRAINT fk_project_members_project
        FOREIGN KEY (project_id) REFERENCES projects(id)
        ON DELETE CASCADE ON UPDATE CASCADE,
    CONSTRAINT fk_project_members_user
        FOREIGN KEY (user_id) REFERENCES users(id)
        ON DELETE CASCADE ON UPDATE CASCADE,
    CONSTRAINT chk_project_members_role
        CHECK (role IN ('programmer', 'artist', 'sound', 'designer', 'qa', 'lead'))
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- 4. ЗАДАЧИ
CREATE TABLE IF NOT EXISTS tasks (
    id              BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
    project_id      BIGINT UNSIGNED NOT NULL,
    title           VARCHAR(200)    NOT NULL,
    description     TEXT            DEFAULT NULL,
    technical_spec  TEXT            DEFAULT NULL,
    priority        VARCHAR(10)     NOT NULL DEFAULT 'medium',
    status          VARCHAR(20)     NOT NULL DEFAULT 'backlog',
    creator_id      BIGINT UNSIGNED NOT NULL,
    estimated_hours DECIMAL(5,2)    DEFAULT NULL,
    due_date        DATETIME        DEFAULT NULL,
    created_at      TIMESTAMP       NOT NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (id),
    KEY idx_tasks_project (project_id),
    KEY idx_tasks_creator (creator_id),
    KEY idx_tasks_status (status),
    KEY idx_tasks_due_date (due_date),
    CONSTRAINT fk_tasks_project
        FOREIGN KEY (project_id) REFERENCES projects(id)
        ON DELETE CASCADE ON UPDATE CASCADE,
    CONSTRAINT fk_tasks_creator
        FOREIGN KEY (creator_id) REFERENCES users(id)
        ON DELETE RESTRICT ON UPDATE CASCADE,
    CONSTRAINT chk_tasks_priority
        CHECK (priority IN ('low', 'medium', 'high', 'critical')),
    CONSTRAINT chk_tasks_status
        CHECK (status IN ('backlog', 'todo', 'in_progress', 'review', 'done')),
    CONSTRAINT chk_tasks_estimated_hours
        CHECK (estimated_hours IS NULL OR estimated_hours >= 0)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- 5. ИСПОЛНИТЕЛИ ЗАДАЧ
CREATE TABLE IF NOT EXISTS task_assignees (
    id              BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
    task_id         BIGINT UNSIGNED NOT NULL,
    user_id         BIGINT UNSIGNED NOT NULL,
    role_in_task    VARCHAR(30)     DEFAULT NULL,
    assigned_at     TIMESTAMP       NOT NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (id),
    UNIQUE KEY uq_task_assignees (task_id, user_id),
    KEY idx_task_assignees_user (user_id),
    CONSTRAINT fk_task_assignees_task
        FOREIGN KEY (task_id) REFERENCES tasks(id)
        ON DELETE CASCADE ON UPDATE CASCADE,
    CONSTRAINT fk_task_assignees_user
        FOREIGN KEY (user_id) REFERENCES users(id)
        ON DELETE CASCADE ON UPDATE CASCADE,
    CONSTRAINT chk_task_assignees_role
        CHECK (role_in_task IS NULL OR role_in_task IN
            ('programmer', 'artist', 'sound', 'designer', 'qa', 'lead', 'reviewer'))
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- 6. РОЛИ, КОТОРЫЕ ЗАТРАГИВАЕТ ЗАДАЧА
CREATE TABLE IF NOT EXISTS task_roles (
    id              BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
    task_id         BIGINT UNSIGNED NOT NULL,
    role            VARCHAR(30)     NOT NULL,
    PRIMARY KEY (id),
    UNIQUE KEY uq_task_roles (task_id, role),
    KEY idx_task_roles_role (role),
    CONSTRAINT fk_task_roles_task
        FOREIGN KEY (task_id) REFERENCES tasks(id)
        ON DELETE CASCADE ON UPDATE CASCADE,
    CONSTRAINT chk_task_roles_role
        CHECK (role IN ('programmer', 'artist', 'sound', 'designer', 'qa', 'lead'))
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- 7. СВЯЗИ МЕЖДУ ЗАДАЧАМИ
-- ВНИМАНИЕ: CHECK (task_id <> related_task_id) убран,
-- т.к. MySQL не разрешает CHECK на колонке с ON DELETE CASCADE.
-- Проверку "задача не ссылается на себя" делаем в коде.
CREATE TABLE IF NOT EXISTS task_relations (
    id                  BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
    task_id             BIGINT UNSIGNED NOT NULL,
    related_task_id     BIGINT UNSIGNED NOT NULL,
    relation_type       VARCHAR(20)     NOT NULL,
    PRIMARY KEY (id),
    UNIQUE KEY uq_task_relations (task_id, related_task_id, relation_type),
    KEY idx_task_relations_related (related_task_id),
    CONSTRAINT fk_task_relations_task
        FOREIGN KEY (task_id) REFERENCES tasks(id)
        ON DELETE CASCADE ON UPDATE CASCADE,
    CONSTRAINT fk_task_relations_related
        FOREIGN KEY (related_task_id) REFERENCES tasks(id)
        ON DELETE CASCADE ON UPDATE CASCADE,
    CONSTRAINT chk_task_relations_type
        CHECK (relation_type IN ('blocks', 'depends_on', 'duplicates', 'relates_to'))
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- 8. ФАЙЛЫ, ПРИКРЕПЛЁННЫЕ К ЗАДАЧАМ
CREATE TABLE IF NOT EXISTS files (
    id              BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
    task_id         BIGINT UNSIGNED NOT NULL,
    uploaded_by     BIGINT UNSIGNED NOT NULL,
    file_name       VARCHAR(255)    NOT NULL,
    file_path       VARCHAR(500)    NOT NULL,
    mime_type       VARCHAR(100)    DEFAULT NULL,
    file_size       BIGINT UNSIGNED DEFAULT NULL,
    uploaded_at     TIMESTAMP       NOT NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (id),
    KEY idx_files_task (task_id),
    KEY idx_files_uploaded_by (uploaded_by),
    CONSTRAINT fk_files_task
        FOREIGN KEY (task_id) REFERENCES tasks(id)
        ON DELETE CASCADE ON UPDATE CASCADE,
    CONSTRAINT fk_files_uploaded_by
        FOREIGN KEY (uploaded_by) REFERENCES users(id)
        ON DELETE RESTRICT ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ============================================================
-- ДАННЫЕ
-- ============================================================

-- 1. ПОЛЬЗОВАТЕЛИ
INSERT INTO users (username, email, password_hash, full_name, global_role, default_role)
SELECT 'ivan', 'ivan@example.com', 'hash1', 'Иван Иванов', 'admin', 'lead'
WHERE NOT EXISTS (SELECT 1 FROM users WHERE username = 'ivan');

-- 2. ПРОЕКТЫ
INSERT INTO projects (name, description, owner_id, deadline)
SELECT 'Мой первый проект', 'Учебный проект',
       (SELECT id FROM users WHERE username = 'ivan' LIMIT 1),
       '2026-12-31 23:59:59'
WHERE NOT EXISTS (SELECT 1 FROM projects WHERE name = 'Мой первый проект');

-- 3. УЧАСТНИКИ ПРОЕКТА
INSERT INTO project_members (project_id, user_id, role)
SELECT
    (SELECT id FROM projects WHERE name = 'Мой первый проект' LIMIT 1),
    (SELECT id FROM users WHERE username = 'ivan' LIMIT 1),
    'lead'
WHERE NOT EXISTS (
    SELECT 1 FROM project_members
    WHERE project_id = (SELECT id FROM projects WHERE name = 'Мой первый проект' LIMIT 1)
      AND user_id = (SELECT id FROM users WHERE username = 'ivan' LIMIT 1)
);

-- 4. ЗАДАЧИ (первая)
INSERT INTO tasks (project_id, title, description, priority, status, creator_id)
SELECT
    (SELECT id FROM projects WHERE name = 'Мой первый проект' LIMIT 1),
    'Сверстать страницу',
    'Сделать главную страницу проекта',
    'high',
    'todo',
    (SELECT id FROM users WHERE username = 'ivan' LIMIT 1)
WHERE NOT EXISTS (SELECT 1 FROM tasks WHERE title = 'Сверстать страницу');

-- 5. ИСПОЛНИТЕЛИ ЗАДАЧ
INSERT INTO task_assignees (task_id, user_id, role_in_task)
SELECT
    (SELECT id FROM tasks WHERE title = 'Сверстать страницу' LIMIT 1),
    (SELECT id FROM users WHERE username = 'ivan' LIMIT 1),
    'programmer'
WHERE NOT EXISTS (
    SELECT 1 FROM task_assignees
    WHERE task_id = (SELECT id FROM tasks WHERE title = 'Сверстать страницу' LIMIT 1)
      AND user_id = (SELECT id FROM users WHERE username = 'ivan' LIMIT 1)
);

-- 6. РОЛИ, КОТОРЫЕ ЗАТРАГИВАЕТ ЗАДАЧА
INSERT INTO task_roles (task_id, role)
SELECT
    (SELECT id FROM tasks WHERE title = 'Сверстать страницу' LIMIT 1),
    'programmer'
WHERE NOT EXISTS (
    SELECT 1 FROM task_roles
    WHERE task_id = (SELECT id FROM tasks WHERE title = 'Сверстать страницу' LIMIT 1)
      AND role = 'programmer'
);

-- 7. СВЯЗИ МЕЖДУ ЗАДАЧАМИ
-- Сначала вторая задача
INSERT INTO tasks (project_id, title, description, priority, status, creator_id)
SELECT
    (SELECT id FROM projects WHERE name = 'Мой первый проект' LIMIT 1),
    'Написать API',
    'Сделать REST API',
    'medium',
    'backlog',
    (SELECT id FROM users WHERE username = 'ivan' LIMIT 1)
WHERE NOT EXISTS (SELECT 1 FROM tasks WHERE title = 'Написать API');

INSERT INTO task_relations (task_id, related_task_id, relation_type)
SELECT
    (SELECT id FROM tasks WHERE title = 'Написать API' LIMIT 1),
    (SELECT id FROM tasks WHERE title = 'Сверстать страницу' LIMIT 1),
    'depends_on'
WHERE NOT EXISTS (
    SELECT 1 FROM task_relations
    WHERE task_id = (SELECT id FROM tasks WHERE title = 'Написать API' LIMIT 1)
      AND related_task_id = (SELECT id FROM tasks WHERE title = 'Сверстать страницу' LIMIT 1)
);

-- 8. ФАЙЛЫ, ПРИКРЕПЛЁННЫЕ К ЗАДАЧАМ
INSERT INTO files (task_id, uploaded_by, file_name, file_path, mime_type, file_size)
SELECT
    (SELECT id FROM tasks WHERE title = 'Сверстать страницу' LIMIT 1),
    (SELECT id FROM users WHERE username = 'ivan' LIMIT 1),
    'layout.png',
    '/uploads/layout.png',
    'image/png',
    102400
WHERE NOT EXISTS (SELECT 1 FROM files WHERE file_name = 'layout.png');