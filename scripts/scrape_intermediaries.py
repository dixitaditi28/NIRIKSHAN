import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
import os

BASE_URL = "https://www.sebi.gov.in/sebiweb/other/OtherAction.do"
PAGINATION_URL = "https://www.sebi.gov.in/sebiweb/ajax/other/getintmfpiinfo.jsp"
HEADERS = {"User-Agent": "Mozilla/5.0"}
OUTPUT_FILE = "data/processed/intermediaries.csv"

CATEGORIES = {
    5: "Banker to an Issue",
    6: "Debentures Trustee",
    7: "Credit Rating Agency (CRA)",
    8: "KYC Registration Agency",
    9: "Merchant Bankers",
    10: "Registrars to an Issue and Share Transfer Agents",
    11: "Underwriters",
    16: "Registered Alternative Investment Funds",
    21: "Registered Venture Capital Funds",
    23: "Registered Mutual Funds",
    25: "Registered Foreign Venture Capital Investors",
    27: "Registered Custodians",
    30: "Registered Stock Brokers (Equity Segment)",
    31: "Registered Stock Brokers (Equity Derivative Segment)"
}

PAGES_PER_CATEGORY = 3

def fetch_page(intm_id, page_number):
    if page_number == 1:
        params = {"doRecognisedFpi": "yes", "intmId": str(intm_id)}
        resp = requests.get(BASE_URL, headers=HEADERS, params=params)
        return resp.text
    else:
        payload = {
            "nextValue": str(page_number - 1),
            "next": "n",
            "intmId": str(intm_id),
            "contPer": "",
            "name": "",
            "regNo": "",
            "email": "",
            "location": "",
            "exchange": "",
            "affiliate": "",
            "alp": "",
            "language": "2",
            "model": "",
            "esgCategory": ""
        }
        resp = requests.post(PAGINATION_URL, headers=HEADERS, data=payload)
        return resp.text
def parse_entities(html, category_name):
    soup = BeautifulSoup(html, "html.parser")

    text_blocks = soup.get_text("\n").split("\n")
    text_blocks = [t.strip() for t in text_blocks if t.strip()]

    field_map = {
        "Name": "name",
        "Trade Name": "trade_name",
        "Registration No.": "registration_no",
        "E-mail": "email",
        "Telephone": "telephone",
        "Address": "address",
        "Validity": "validity",
        "Exchange Name": "exchange_name"
    }

    entities = []
    current = {}
    i = 0
    while i < len(text_blocks):
        label = text_blocks[i]
        if label in field_map:
            key = field_map[label]
            value = text_blocks[i + 1] if i + 1 < len(text_blocks) else ""

            if key == "name" and current:
                current["category"] = category_name
                entities.append(current)
                current = {}

            current[key] = value
            i += 2
        else:
            i += 1

    if current:
        current["category"] = category_name
        entities.append(current)

    return entities


def scrape_all():
    os.makedirs(os.path.dirname(OUTPUT_FILE), exist_ok=True)
    all_entities = []

    for intm_id, category_name in CATEGORIES.items():
        print(f"\nScraping category: {category_name} (intmId={intm_id})")
        for page in range(1, PAGES_PER_CATEGORY + 1):
            html = fetch_page(intm_id, page)
            entities = parse_entities(html, category_name)
            if not entities:
                print(f"  Page {page}: no entities found, stopping category.")
                break
            all_entities.extend(entities)
            print(f"  Page {page}: {len(entities)} entities")
            time.sleep(1)

    df = pd.DataFrame(all_entities)
    df = df.drop_duplicates(subset=["registration_no", "category"])
    df.to_csv(OUTPUT_FILE, index=False)
    print(f"\nSaved {len(df)} unique entities to {OUTPUT_FILE}")

if __name__ == "__main__":
    scrape_all()