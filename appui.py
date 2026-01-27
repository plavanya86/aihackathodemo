import streamlit as st
import sqlite3
import json
from openai import AzureOpenAI

# -----------------------------
# Azure OpenAI Client
# -----------------------------


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
Do NOT use markdown or ```.

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

# -----------------------------
# Execute SQL
# -----------------------------
def execute_sql(sql):
    conn = sqlite3.connect("ai_rangers.db")
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
    prompt = f"""
You are explaining database schema to a new developer.

Schema:
{SCHEMA_CONTEXT}

Question:
{question}

Give a clear, simple explanation.
"""
    response = client.chat.completions.create(
        model=DEPLOYMENT_NAME,
        messages=[{"role": "user", "content": prompt}],
        temperature=0.3
    )
    return response.choices[0].message.content

# -----------------------------
# STREAMLIT UI
# -----------------------------
st.set_page_config(page_title="NL → SQL AI Assistant", layout="wide")

st.title("🧠 AI Project Database Assistant")
st.caption("Natural Language → SQL + Schema Explanation")

question = st.text_input("Ask your question 👇", placeholder="Show tasks for projects in progress")

col1, col2 = st.columns(2)

with col1:
    run_sql = st.button("🔍 Run SQL")

with col2:
    explain = st.button("📘 Explain Schema")

# -----------------------------
# SQL Flow
# -----------------------------
if run_sql and question:
    try:
        sql = generate_sql(question)
        st.subheader("🧠 Generated SQL")
        st.code(sql, language="sql")

        cols, rows = execute_sql(sql)
        if rows:
            st.subheader("📊 Results")
            st.dataframe(rows, use_container_width=True)
        else:
            st.warning("No data found.")
    except Exception as e:
        st.error(f"Error: {e}")

# -----------------------------
# Schema Explanation Flow
# -----------------------------
if explain and question:
    explanation = explain_schema(question)
    st.subheader("📘 Schema Explanation")
    st.write(explanation)
