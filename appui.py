import streamlit as st
import sqlite3
import json
from create_tables import init_db
from insert_data import seed_data
from dotenv import load_dotenv
import os
load_dotenv()
from openai import AzureOpenAI


# -----------------------------
# Azure OpenAI Client
# -----------------------------




class SQLValidationError(Exception):
    def __init__(self, message, fix_hint):
        self.message = message
        self.fix_hint = fix_hint
        super().__init__(message)

class InvalidTableError(Exception):
    pass

class ForbiddenCommandError(Exception):
    pass


if "db_initialized" not in st.session_state:
    init_db()
    seed_data()
    st.session_state.db_initialized = True

# -----------------------------
# Load Schema
# -----------------------------
with open("metadata/schema.json", "r") as f:
    SCHEMA = json.load(f)

def format_schema(schema):
    text = f"Database: {schema['database']}\n\n"
    for table, details in schema["tables"].items():
        text += f"Table: {table}\n"
        text += f"Description: {details['description']}\n"
        for col, meta in details["columns"].items():
            text += f"- {col}: {meta['description']}\n"
        text += "\n"
    return text

SCHEMA_CONTEXT = format_schema(SCHEMA)

# -----------------------------
# SQL Generation
# -----------------------------
def generate_sql(question):
    prompt = f"""
You are an expert SQL assistant.

Use the schema below to generate SQLite-compatible SQL.
Do NOT use markdown or
When generating SQL:
- Always use LOWER() for string comparisons
- Assume SQLite is case-sensitive
-Rules:
- Use ONLY tables present in the schema
- If a requested table does not exist, DO NOT guess a replacement
- DO NOT substitute table names

 ```.

Schema:
{SCHEMA_CONTEXT}

User Question:
{question}

Return only SQL.
"""
    response = client.chat.completions.create(
        model=DEPLOYMENT_NAME,
        messages=[{"role": "user", "content": prompt}],
        temperature=0
    )
    return response.choices[0].message.content.strip()


#-----------------------------
#Rewriting prompt
#---------------------------
def rewrite_prompt(original_question, bad_sql, error: SQLValidationError):
    return f"""
You generated an incorrect SQL query.

User Question:
{original_question}

Incorrect SQL:
{bad_sql}

Problem:
{error.message}

Fix Instructions:
{error.fix_hint}

Rules:
- Use correct JOINs based on foreign keys
- Do NOT return IDs when names exist
- Use only tables and columns from the schema
- Return ONLY valid SQLite SQL
- NEVER change table names
- If a table does not exist, return the SQL unchanged

Return ONLY the corrected SQL query.
"""

# -----------------------------
# Execute SQL
# -----------------------------
def execute_sql(sql):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute(sql)
    rows = cursor.fetchall()
    columns = [desc[0] for desc in cursor.description] if cursor.description else []
    conn.close()
    return columns, rows

# -----------------------------
# Schema Explanation
# -----------------------------
def explain_schema(question):
    # 🔐 1️⃣ Hard validation FIRST (no LLM)
    forbidden = contains_forbidden_prompt(question)

    if forbidden:
        return (
            "❌ Invalid prompt due to database constraints.\n"
            f"The operation `{forbidden.upper()}` is not supported.\n"
            "This database is read-only and does not allow data modification."
        )

    # 🧠 2️⃣ Only valid prompts reach the LLM
    prompt = f"""
You are explaining the database schema to a new developer.

Schema:
{SCHEMA_CONTEXT}

Question:
{question}

Rules:
- Give a clear and concise explanation
- Explain only relevant tables and columns
- Do NOT generate SQL
- Do NOT suggest alternative queries
- If the schema does not support the question, clearly say so
- Keep the explanation short and factual
"""

    response = client.chat.completions.create(
        model=DEPLOYMENT_NAME,
        messages=[{"role": "user", "content": prompt}],
        temperature=0.2
    )

    return response.choices[0].message.content.strip()

# -----------------------------
# STREAMLIT UI
# -----------------------------
import os
st.set_page_config(page_title="NL → SQL AI Assistant", layout="wide")

#st.image("hcltech-new-logo.svg", width=180)
st.markdown(
   """
    <div style="background-color:#f0f0f0; width:200px; padding:10px; display:inline-block; text-align:center;">
    """,
   unsafe_allow_html=True
)

st.image("hcltech-new-logo.svg", width=180)

st.markdown("</div>", unsafe_allow_html=True)



st.title("🧠 SQL Database Assistant")
question = st.text_input("Ask your question 👇", placeholder="Enter your Question")

col1, col2 = st.columns(2)

with col1:
    run_sql = st.button("🔍 Run SQL")

with col2:
    explain = st.button("📘 Explain Schema")


#--------------------------
#VALIDATION
#-----------------------------
import re


FORBIDDEN_KEYWORDS = {
    "insert", "update", "delete", "drop", "alter",
    "create", "truncate", "attach", "pragma"
}


ALLOWED_TABLES = set(SCHEMA["tables"].keys())

def contains_forbidden_prompt(question: str):
    q = f" {question.lower()} "
    for kw in FORBIDDEN_KEYWORDS:
        if f" {kw} " in q:
            return kw
    return None

def validate_user_intent(question: str):
    q = question.lower()

    # 1️⃣ Multiple statements intent
    if ";" in q:
        raise ValueError(
            "❌ Multiple statements detected.\n"
            "Only ONE SELECT query is allowed."
        )

    # 2️⃣ Forbidden commands intent
    for kw in FORBIDDEN_KEYWORDS:
        if re.search(rf"\b{kw}\b", q):
            raise ForbiddenCommandError(
                f"❌ `{kw.upper()}` operation is not allowed.\n"
                "This database is read-only."
            )
        
def validate_sql(sql: str):
    if not sql or not sql.strip():
        raise ValueError("❌ Empty SQL query")

    sql_clean = sql.strip()
    sql_lower = sql_clean.lower()

    # 1️⃣ MULTIPLE STATEMENTS (highest priority)
    if sql_clean.count(";") > 1:
        raise ValueError(
            "❌ Multiple SQL statements detected.\n"
            "Only ONE SELECT statement is allowed."
        )

    # 2️⃣ FORBIDDEN COMMANDS
    for keyword in FORBIDDEN_KEYWORDS:
        if re.search(rf"\b{keyword}\b", sql_lower):
            raise ForbiddenCommandError(
                f"❌ `{keyword.upper()}` operations are not allowed.\n"
                "The database is read-only."
            )

    # 3️⃣ ONLY SELECT ALLOWED
    if not sql_lower.startswith("select"):
        raise ValueError("❌ Only SELECT queries are allowed")

    # 4️⃣ COMMENTS
    if "--" in sql_lower or "/*" in sql_lower:
        raise ValueError("❌ SQL comments are not allowed")

    # 5️⃣ SUBQUERIES
    if re.search(r"\(\s*select\b", sql_lower):
        raise ValueError("❌ Subqueries are not allowed")

    # 6️⃣ TABLE VALIDATION
    tables = re.findall(r"\bfrom\s+(\w+)|\bjoin\s+(\w+)", sql_lower)
    for t1, t2 in tables:
        table = t1 or t2
        if table not in ALLOWED_TABLES:
            raise InvalidTableError(
                f"❌ Invalid table `{table}`.\n"
                "This table does not exist in the schema."
            )

    # 7️⃣ SAFE AUTO-FIX ONLY (FK / JOIN)
    if "from tasks" in sql_lower and "assigned_to" in sql_lower and "join" not in sql_lower:
        raise SQLValidationError(
            message="assigned_to is a foreign key, not a name",
            fix_hint="Join team_members on tasks.assigned_to = team_members.member_id"
        )

    return True



# -----------------------------
# SQL Flow
# -----------------------------
import pandas as pd
if run_sql and question:
    try:
        # 🔐 HARD INTENT VALIDATION (BEFORE LLM)
        validate_user_intent(question)

        # 🧠 Generate SQL ONLY after intent is safe
        sql = generate_sql(question)

        try:
            validate_sql(sql)

        except (InvalidTableError,
                ForbiddenCommandError,
                ValueError) as e:
            st.error(str(e))
            st.stop()   # ⛔ NO AUTO FIX

        except SQLValidationError as ve:
            st.warning("⚠️ Fixing query structure...")
            fixed_prompt = rewrite_prompt(question, sql, ve)
            sql = generate_sql(fixed_prompt)
            validate_sql(sql)

        st.subheader("🧠 Generated SQL")
        st.code(sql, language="sql")

        cols, rows = execute_sql(sql)
        st.success("✅ Query executed successfully")

        if rows:
            st.subheader("📊 Results")
            df = pd.DataFrame(rows, columns=cols)
            styled_df = df.style.set_table_styles([
                {'selector': 'th', 'props': [('background-color', '#4CAF50'), ('color', 'white')]},
                ]).highlight_max(axis=0, color='lightblue')


            st.dataframe(df, use_container_width=True)
        else:
            st.warning("No data found.")


    except Exception as e:
        st.error(f"❌ Error: {e}")


# -----------------------------
# Schema Explanation Flow
# -----------------------------
if explain and question:
    explanation = explain_schema(question)
    st.subheader("📘 Schema Explanation")
    st.write(explanation)
