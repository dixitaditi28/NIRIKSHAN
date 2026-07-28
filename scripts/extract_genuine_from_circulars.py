import psycopg2
import os
import re
import csv
from dotenv import load_dotenv

load_dotenv()

DB_CONFIG = {
    "dbname": "nirikshan",
    "user": "postgres",
    "password": os.environ.get("DB_PASSWORD"),
    "host": "localhost",
    "port": "5432"
}

OUTPUT_FILE = "data/synthetic/text/genuine_real_excerpts.csv"
TARGET_COUNT = 250
MIN_EXCERPT_LENGTH = 200
MAX_EXCERPT_LENGTH = 450
SKIP_HEADER_CHARS = 150

def clean_text(raw_text):
    text = re.sub(r'\s+', ' ', raw_text).strip()
    return text

def extract_excerpt(full_text, circular_id, subject):
    cleaned = clean_text(full_text)
    if len(cleaned) < SKIP_HEADER_CHARS + MIN_EXCERPT_LENGTH:
        return None

    search_start = SKIP_HEADER_CHARS
    sentence_end_pattern = re.compile(r'[.!?]\s+[A-Z]')
    match = sentence_end_pattern.search(cleaned, search_start)

    start_pos = match.start() + 2 if match else search_start
    excerpt = cleaned[start_pos:start_pos + MAX_EXCERPT_LENGTH]

    last_period = excerpt.rfind('.')
    if last_period > MIN_EXCERPT_LENGTH:
        excerpt = excerpt[:last_period + 1]

    if len(excerpt) < MIN_EXCERPT_LENGTH:
        return None

    return excerpt

def extract_genuine_excerpts():
    os.makedirs(os.path.dirname(OUTPUT_FILE), exist_ok=True)

    conn = psycopg2.connect(**DB_CONFIG)
    cur = conn.cursor()
    cur.execute("SELECT circular_id, date, subject, full_text FROM sebi_circulars WHERE full_text IS NOT NULL")
    rows = cur.fetchall()
    cur.close()
    conn.close()

    print(f"Fetched {len(rows)} circulars from database")

    excerpts = []
    for idx, (circular_id, date, subject, full_text) in enumerate(rows):
        excerpt = extract_excerpt(full_text, circular_id or f"row_{idx}", subject)
        if excerpt:
            excerpts.append({
                "text": excerpt,
                "label": "genuine",
                "language": "English",
                "source": "real_circular",
                "template_id": f"real_circular_{idx}"
            })
        if len(excerpts) >= TARGET_COUNT:
            break

    print(f"Extracted {len(excerpts)} valid excerpts")

    with open(OUTPUT_FILE, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["text", "label", "language", "source", "template_id"])
        writer.writeheader()
        writer.writerows(excerpts)

    print(f"Saved to {OUTPUT_FILE}")

if __name__ == "__main__":
    extract_genuine_excerpts()