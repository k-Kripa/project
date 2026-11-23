"""Step 3 - Load the cleaned CSV into PostgreSQL (credentials come from .env)."""
import os
from pathlib import Path

import pandas as pd
from dotenv import load_dotenv
from sqlalchemy import create_engine, text

ROOT = Path(__file__).resolve().parent.parent
load_dotenv(ROOT / ".env")

url = (
    f"postgresql+psycopg2://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}"
    f"@{os.getenv('DB_HOST')}:{os.getenv('DB_PORT', '5432')}/{os.getenv('DB_NAME')}?sslmode=require"
)
engine = create_engine(url)

df = pd.read_csv(ROOT / "data" / "cleaned" / "properties_cleaned.csv")

with engine.begin() as conn:
    conn.execute(text("create schema if not exists student_project"))

df.to_sql("properties_cleaned", engine, schema="student_project",
          if_exists="replace", index=False)
print(f"Loaded {len(df)} rows into student_project.properties_cleaned")
