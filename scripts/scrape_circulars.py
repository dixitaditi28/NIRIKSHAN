import requests
from bs4 import BeautifulSoup
import pdfplumber
import os
import re
import json
import time

BASE_URL = "https://www.sebi.gov.in/sebiweb/home/HomeAction.do"
PAGINATION_URL = "https://www.sebi.gov.in/sebiweb/ajax/home/getnewslistinfo.jsp"
HEADERS = {"User-Agent": "Mozilla/5.0"}
RAW_DIR = "data/raw/circulars"
OUTPUT_FILE = "data/processed/circulars.json"
TARGET_COUNT = 520

def fetch_listing_page(page_number):
    if page_number == 1:
        params = {"doListing": "yes", "sid": "1", "ssid": "7", "smid": "0"}
        resp = requests.get(BASE_URL, headers=HEADERS, params=params)
        return resp.text
    else:
        payload = {
            "nextValue": str(page_number - 1),
            "next": "n",
            "search": "",
            "fromDate": "",
            "toDate": "",
            "fromYear": "",
            "toYear": "",
            "deptId": "-1",
            "sid": "1",
            "ssid": "7",
            "smid": "0",
            "ssidhidden": "7",
            "intmid": "-1",
            "sText": "Legal",
            "ssText": "Circulars"
        }
        resp = requests.post(PAGINATION_URL, headers=HEADERS, data=payload)
        return resp.text

def parse_circular_list(html):
    soup = BeautifulSoup(html, "html.parser")
    rows = soup.select("tr[role='row']")
    circulars = []
    for row in rows:
        cells = row.find_all("td")
        if len(cells) < 2:
            continue
        date_text = cells[0].get_text(strip=True)
        link_tag = cells[1].find("a")
        if not link_tag:
            continue
        title = link_tag.get_text(strip=True)
        url = link_tag.get("href")
        circulars.append({"date": date_text, "title": title, "page_url": url})
    return circulars

def get_pdf_url(circular_page_url):
    resp = requests.get(circular_page_url, headers=HEADERS)
    match = re.search(r"file=(https://www\.sebi\.gov\.in/sebi_data/attachdocs/[^']+\.pdf)", resp.text)
    if match:
        return match.group(1)
    return None

def download_and_extract(pdf_url, save_path):
    r = requests.get(pdf_url, headers=HEADERS)
    with open(save_path, "wb") as f:
        f.write(r.content)
    with pdfplumber.open(save_path) as pdf:
        text = "\n".join(page.extract_text() or "" for page in pdf.pages)
    return text

def scrape_all(target_count):
    os.makedirs(RAW_DIR, exist_ok=True)
    os.makedirs(os.path.dirname(OUTPUT_FILE), exist_ok=True)

    all_circulars = []
    page = 1

    while len(all_circulars) < target_count:
        html = fetch_listing_page(page)
        page_circulars = parse_circular_list(html)

        if not page_circulars:
            print(f"No more circulars found at page {page}. Stopping.")
            break

        for c in page_circulars:
            try:
                pdf_url = get_pdf_url(c["page_url"])
                if not pdf_url:
                    print(f"Skipping (no PDF): {c['title']}")
                    continue

                filename = pdf_url.split("/")[-1]
                save_path = os.path.join(RAW_DIR, filename)
                text = download_and_extract(pdf_url, save_path)

                c["pdf_url"] = pdf_url
                c["full_text"] = text
                all_circulars.append(c)

                print(f"[{len(all_circulars)}/{target_count}] Scraped: {c['title'][:60]}")
                time.sleep(1)

            except Exception as e:
                print(f"Error on '{c['title']}': {e}")
                continue

            if len(all_circulars) >= target_count:
                break

        page += 1
        time.sleep(1)

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(all_circulars, f, ensure_ascii=False, indent=2)

    print(f"\nDone. Saved {len(all_circulars)} circulars to {OUTPUT_FILE}")

if __name__ == "__main__":
    scrape_all(TARGET_COUNT)