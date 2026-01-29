import sqlite3

DB_PATH="C:/Users/pamarthi.padmavathi/git/aihackathodemo/ai_rangers.db"
def seed_data():
 conn = sqlite3.connect(DB_PATH)
 cursor = conn.cursor()

#preent duplicates inserts
 cursor.execute("SELECT COUNT(*) FROM projects")
 if cursor.fetchone()[0] > 0:
    conn.close()
    return

 # -------------------------
 # INSERT PROJECTS
 # -------------------------
 cursor.executemany("""
 INSERT INTO projects (project_name, start_date, end_date, status)
 VALUES (?, ?, ?, ?)
 """, [
   ("AI Project Tracker", "2024-10-01", "2025-03-31", "In Progress"),
   ("Automation Dashboard", "2024-08-15", "2025-01-15", "Completed"),
   ("Mobile Banking App", "2025-01-10", "2025-09-30", "In Progress"),
   ("ChatOps Integration", "2024-11-05", "2025-04-30", "In Progress"),
   ("Data Quality Framework", "2024-07-01", "2024-12-20", "Completed"),
   ("Observability Platform", "2025-02-01", "2025-10-31", "Not Started"),

 ])

 # -------------------------
 # INSERT TEAM MEMBERS
 # -------------------------
 cursor.executemany("""
 INSERT INTO team_members (member_name, role, project_id)
 VALUES (?, ?, ?)
 """, [
   # Project 1 - AI Project Tracker
   ("Ponnada Lavanya", "Technical Lead", 1),
   ("Anil Kumar", "Backend Developer", 1),
   ("Sneha Reddy", "Frontend Developer", 1),     
   ("Rahul Verma", "QA Engineer", 1),

   # Project 2 - Automation Dashboard
   ("Isha Gupta", "Product Manager", 2),
   ("Vikram Singh", "DevOps Engineer", 2),

   # Project 3 - Mobile Banking App
   ("Neha Sharma", "iOS Engineer", 3),
   ("Karan Mehta", "Android Engineer", 3),
   ("Arjun Rao", "Backend Developer", 3),
   ("Divya Nair", "QA Engineer", 3),

   # Project 4 - ChatOps Integration
   ("Meera Iyer", "Platform Engineer", 4),
   ("Sahil Jain", "SRE", 4),

   # Project 5 - Data Quality Framework
   ("Rohit Patil", "Data Engineer", 5),
   ("Aditi Kulkarni", "Data Analyst", 5),

   # Project 6 - Observability Platform
   ("Harsh Vardhan", "Site Reliability Engineer", 6),
   ("Priya Menon", "Full Stack Engineer", 6),

 ])

 # -------------------------
 # INSERT SPRINTS
 # -------------------------
 cursor.executemany("""
 INSERT INTO sprints (sprint_name, start_date, end_date, project_id)
 VALUES (?, ?, ?, ?)
 """, [
   # Project 1
   ("Sprint 1 - Planning", "2024-10-01", "2024-10-15", 1),
   ("Sprint 2 - Development", "2024-10-16", "2024-10-31", 1),
   ("Sprint 3 - ML Pipeline", "2024-11-01", "2024-11-15", 1),

   # Project 2
   ("Sprint 1 - Automation Setup", "2024-08-15", "2024-08-31", 2),
   ("Sprint 2 - CI/CD", "2024-09-01", "2024-09-15", 2),

   # Project 3
   ("Sprint 1 - Auth Flows", "2025-01-10", "2025-01-24", 3),
   ("Sprint 2 - Payments", "2025-01-25", "2025-02-08", 3),

   # Project 4
   ("Sprint 1 - Bot Basics", "2024-11-05", "2024-11-20", 4),

   # Project 5
   ("Sprint 1 - DQ Rules", "2024-07-01", "2024-07-15", 5),

   # Project 6
   ("Sprint 1 - Metrics", "2025-02-01", "2025-02-14", 6),

 ])

 # -------------------------
 # INSERT TASKS
 # -------------------------
 cursor.executemany("""
 INSERT INTO tasks (task_title, status, priority, assigned_to, sprint_id)
 VALUES (?, ?, ?, ?, ?)
 """, [
   ("Design database schema", "completed", "High", 1, 1),
   ("API development", "in progress", "High", 2, 2),
   ("UI dashboard creation", "in progress", "Medium", 3, 2),
   ("Test case preparation", "not started", "Low", 4, 3),

   # ⭐ More tasks added below
   ("Optimize SQL queries", "completed", "Medium", 1, 1),
   ("Set up CI/CD pipeline", "in progress", "High", 2, 2),
   ("Build frontend components", "in progress", "Medium", 3, 2),
   ("Write unit tests", "not started", "Medium", 4, 3),
   ("Prepare sprint report", "completed", "Low", 1, 1),
    
   ("Implement authentication", "in progress", "High", 2, 2),
   ("Fix UI bugs", "in progress", "Low", 3, 2),
   ("Improve logging framework", "completed", "Medium", 4, 3),
   ("Add pagination support", "not started", "Low", 1, 1),
    
   ("Enhance API error handling", "completed", "High", 2, 2),
   ("Integrate charts dashboard", "in progress", "Medium", 3, 2),
   ("Write integration tests", "not started", "High", 4, 3),
   ("Refactor codebase", "completed", "Medium", 1, 1),

   ("Email notification module", "not started", "Low", 2, 2),
   ("Implement search feature", "in progress", "High", 3, 2),
   ("Sprint retro preparation", "completed", "Low", 4, 3),
   ("Task assignment enhancements", "in progress", "Medium", 1, 1)

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
   ("Test data mismatch", "Medium", "In Progress", 4),

   # ⭐ Additional defects
   ("Slow database query", "High", "Open", 1),
   ("Incorrect API error code", "Medium", "Open", 2),
   ("Button click not responsive", "Low", "Closed", 3),
   ("Form validation failure", "High", "In Progress", 1),
   ("Unexpected logout issue", "Critical", "Open", 2),
   ("Dropdown not loading", "Medium", "Open", 3),
   ("Timezone mismatch in logs", "Low", "Closed", 4),
   ("CSS not applied in dark mode", "Low", "Open", 3),
   ("Memory leak in API service", "High", "In Progress", 2),
   ("Incorrect pagination count", "Medium", "Closed", 1),
   ("Broken image in UI", "Low", "Closed", 3),
   ("Duplicate records in report", "High", "Open", 4),
   ("Search results inconsistent", "Medium", "In Progress", 2),
   ("API timeout under load", "Critical", "Open", 2),
   ("Tooltip overlapping text", "Low", "Open", 3),
   ("Mobile layout breaks", "Medium", "Open", 3),
   ("Incorrect priority mapping", "Low", "Closed", 4)

 ])

 conn.commit()
 conn.close()

print("✅ Sample data inserted successfully")
