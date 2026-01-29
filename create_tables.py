import sqlite3
DB_PATH="C:/Users/pamarthi.padmavathi/git/aihackathodemo/ai_rangers.db"
def init_db():
 conn = sqlite3.connect(DB_PATH)
 cursor = conn.cursor()

 # PROJECTS
 cursor.execute("""
 CREATE TABLE IF NOT EXISTS projects (
    project_id INTEGER PRIMARY KEY AUTOINCREMENT,
    project_name TEXT NOT NULL,
    start_date TEXT,
    end_date TEXT,
    status TEXT
 )
 """)

 # TEAM MEMBERS
 cursor.execute("""
 CREATE TABLE IF NOT EXISTS team_members (
    member_id INTEGER PRIMARY KEY AUTOINCREMENT,
    member_name TEXT,
    role TEXT,
    project_id INTEGER,
    FOREIGN KEY (project_id) REFERENCES projects(project_id)
 )
 """)

 # SPRINTS
 cursor.execute("""
 CREATE TABLE IF NOT EXISTS sprints (
    sprint_id INTEGER PRIMARY KEY AUTOINCREMENT,
    sprint_name TEXT,
    start_date TEXT,
    end_date TEXT,
    project_id INTEGER,
    FOREIGN KEY (project_id) REFERENCES projects(project_id)
 )
 """)

# TASKS
 cursor.execute("""
 CREATE TABLE IF NOT EXISTS tasks (
    task_id INTEGER PRIMARY KEY AUTOINCREMENT,
    task_title TEXT,
    status TEXT,
    priority TEXT,
    assigned_to INTEGER,
    sprint_id INTEGER,
    FOREIGN KEY (assigned_to) REFERENCES team_members(member_id),
    FOREIGN KEY (sprint_id) REFERENCES sprints(sprint_id)
 )
 """)

 # DEFECTS
 cursor.execute("""
 CREATE TABLE IF NOT EXISTS defects (
    defect_id INTEGER PRIMARY KEY AUTOINCREMENT,
    defect_title TEXT,
    severity TEXT,
    status TEXT,
    task_id INTEGER,
    FOREIGN KEY (task_id) REFERENCES tasks(task_id)
 )
 """)

 conn.commit()
 conn.close()

print("✅ Database and tables created successfully")
