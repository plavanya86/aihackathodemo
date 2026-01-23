import sqlite3

conn = sqlite3.connect("ai_rangers.db")
cursor = conn.cursor()

# -------------------------
# INSERT PROJECTS
# -------------------------
cursor.executemany("""
INSERT INTO projects (project_name, start_date, end_date, status)
VALUES (?, ?, ?, ?)
""", [
    ("AI Project Tracker", "2024-10-01", "2025-03-31", "In Progress"),
    ("Automation Dashboard", "2024-08-15", "2025-01-15", "Completed")
])

# -------------------------
# INSERT TEAM MEMBERS
# -------------------------
cursor.executemany("""
INSERT INTO team_members (member_name, role, project_id)
VALUES (?, ?, ?)
""", [
    ("Ponnada Lavanya", "Technical Lead", 1),
    ("Anil Kumar", "Backend Developer", 1),
    ("Sneha Reddy", "Frontend Developer", 1),
    ("Rahul Verma", "QA Engineer", 2)
])

# -------------------------
# INSERT SPRINTS
# -------------------------
cursor.executemany("""
INSERT INTO sprints (sprint_name, start_date, end_date, project_id)
VALUES (?, ?, ?, ?)
""", [
    ("Sprint 1 - Planning", "2024-10-01", "2024-10-15", 1),
    ("Sprint 2 - Development", "2024-10-16", "2024-10-31", 1),
    ("Sprint 1 - Automation Setup", "2024-08-15", "2024-08-31", 2)
])

# -------------------------
# INSERT TASKS
# -------------------------
cursor.executemany("""
INSERT INTO tasks (task_title, status, priority, assigned_to, sprint_id)
VALUES (?, ?, ?, ?, ?)
""", [
    ("Design database schema", "Completed", "High", 1, 1),
    ("API development", "In Progress", "High", 2, 2),
    ("UI dashboard creation", "In Progress", "Medium", 3, 2),
    ("Test case preparation", "Not Started", "Low", 4, 3)
])

# -------------------------
# INSERT DEFECTS
# -------------------------
cursor.executemany("""
INSERT INTO defects (defect_title, severity, status, task_id)
VALUES (?, ?, ?, ?)
""", [
    ("API response delay", "High", "Open", 2),
    ("UI alignment issue", "Low", "Closed", 3),
    ("Test data mismatch", "Medium", "In Progress", 4)
])

conn.commit()
conn.close()

print("✅ Sample data inserted successfully")
