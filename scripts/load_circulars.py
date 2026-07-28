import json
import os
import psycopg2
from dotenv import load_dotenv

load_dotenv()

DB_CONFIG = {
    "dbname": "nirikshan",
    "user": "postgres",
    "password": os.environ.get("DB_PASSWORD"),
    "host": "localhost",
    "port": "5432"
}

INPUT_FILE = "data/processed/circulars.json"

def load_circulars():
    with open(INPUT_FILE, "r", encoding="utf-8") as f:
        circulars = json.load(f)

    conn = psycopg2.connect(**DB_CONFIG)
    cur = conn.cursor()

    inserted = 0
    for c in circulars:
        cur.execute(
            """
            INSERT INTO sebi_circulars (date, subject, full_text, source_url, pdf_url)
            VALUES (%s, %s, %s, %s, %s)
            """,
            (c.get("date"), c.get("title"), c.get("full_text"), c.get("page_url"), c.get("pdf_url"))
        )
        inserted += 1

    conn.commit()
    cur.close()
    conn.close()
    print(f"Inserted {inserted} circulars into sebi_circulars table.")

if __name__ == "__main__":
    load_circulars()