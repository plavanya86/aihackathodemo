import json
import sqlite3
from openai import AzureOpenAI

# --------------------
# CONFIG
# --------------------
DB_PATH = "ai_rangers.db"
SCHEMA_PATH = "metadata/schema.json"


# --------------------
# LOAD SCHEMA
# --------------------
with open(SCHEMA_PATH, "r") as f:
    schema = json.load(f)

def schema_to_prompt(schema: dict) -> str:
    lines = []
    for table, info in schema["tables"].items():
        lines.append(f"Table: {table}")
        for col in info["columns"]:
            lines.append(f" - {col}")
        lines.append("")
    return "\n".join(lines)

SCHEMA_PROMPT = schema_to_prompt(schema)

# --------------------
# DATABASE
# --------------------
def execute_sql(sql: str):
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()
    cur.execute(sql)
    rows = cur.fetchall()
    conn.close()
    return [dict(row) for row in rows]

# --------------------
# LLM → SQL
# --------------------
def get_sql_from_llm(question: str) -> str:
    system_prompt = f"""
You are an expert SQLite SQL generator.

Rules:
- Use ONLY the tables and columns listed
- SQLite syntax only
- Respect case-sensitive values (example: 'In Progress')
- Do NOT use UNION unless required
- Return ONLY SQL (no markdown, no explanation)

Schema:
{SCHEMA_PROMPT}
"""

    response = client.chat.completions.create(
        model=DEPLOYMENT_NAME,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": question}
        ],
        temperature=0
    )

    raw_sql = response.choices[0].message.content.strip()

    # Remove markdown fences if present
    if raw_sql.startswith("```"):
        raw_sql = raw_sql.replace("```sql", "").replace("```", "").strip()

    return raw_sql
    system_prompt = f"""
You are an expert SQLite SQL generator.

Rules:
- Use ONLY the tables and columns listed
- SQLite syntax only
- Respect case-sensitive values (example: 'In Progress')
- Do NOT use UNION unless required
- Return ONLY SQL

Schema:
{SCHEMA_PROMPT}
"""

    response = client.chat.completions.create(
        model=DEPLOYMENT_NAME,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": question}
        ],
        temperature=0
    )

    return response.choices[0].message.content.strip()

# --------------------
# LLM → SCHEMA EXPLANATION
# --------------------
def explain_schema_with_llm():
    prompt = f"""
Explain this database schema in simple language.
Audience: new developers / freshers.

Explain:
- What each table represents
- How tables are related
- Real-world meaning

Schema:
{json.dumps(schema, indent=2)}
"""

    response = client.chat.completions.create(
        model=DEPLOYMENT_NAME,
        messages=[
            {"role": "system", "content": "You are a helpful database expert."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.2
    )

    return response.choices[0].message.content.strip()

# --------------------
# MAIN PROGRAM
# --------------------
def main():
    print("\n🤖 AI SQL Assistant (No UI)")
    print("1. Ask SQL question")
    print("2. Explain database schema")
    print("3. Exit")

    while True:
        choice = input("\nEnter choice (1/2/3): ")

        if choice == "1":
            question = input("\nAsk your question: ")
            try:
                sql = get_sql_from_llm(question)
                print("\n🧠 Generated SQL:")
                print(sql)

                results = execute_sql(sql)
                print("\n📊 Results:")
                if results:
                    for row in results:
                        print(row)
                else:
                    print("No data found.")

            except Exception as e:
                print("❌ Error:", e)

        elif choice == "2":
            explanation = explain_schema_with_llm()
            print("\n📘 Schema Explanation:\n")
            print(explanation)

        elif choice == "3":
            print("👋 Exiting...")
            break

        else:
            print("❌ Invalid choice")

# --------------------
# RUN
# --------------------
if __name__ == "__main__":
    main()
