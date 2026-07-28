import pandas as pd
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

INPUT_FILE = "data/processed/intermediaries.csv"

def load_intermediaries():
    df = pd.read_csv(INPUT_FILE)

    df = df.dropna(subset=["name"])
    df = df[~df["registration_no"].isin([":", "", None])]
    df = df.where(pd.notnull(df), None)

    conn = psycopg2.connect(**DB_CONFIG)
    cur = conn.cursor()

    inserted = 0
    for _, row in df.iterrows():
        cur.execute(
            """
            INSERT INTO registered_intermediaries
            (registration_no, category, name, trade_name, email, telephone, address, validity, exchange_name)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
            """,
            (row.get("registration_no"), row.get("category"), row.get("name"),
             row.get("trade_name"), row.get("email"), row.get("telephone"),
             row.get("address"), row.get("validity"), row.get("exchange_name"))
        )
        inserted += 1

    conn.commit()
    cur.close()
    conn.close()
    print(f"Inserted {inserted} intermediaries into registered_intermediaries table.")

if __name__ == "__main__":
    load_intermediaries()