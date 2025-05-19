import requests
from bs4 import BeautifulSoup
import json
import time
import logging
from datetime import datetime

# --- Configuration ---
ARCHIVE_URL = "https://pastebin.com/archive"
RAW_URL_TEMPLATE = "https://pastebin.com/raw/{}"
OUTPUT_FILE = "keyword_matches.jsonl"
KEYWORDS = [
    "crypto", "bitcoin", "ethereum", "blockchain", "t.me", "cryptocurrency", "bitget", "tether", "cardano", "solana", "xrp", "dogecoin", "tron", "polygon", "polkadot", "avalanche", "litecoin", "binance", "shiba inu" , "dai"
]
REQUEST_DELAY = 2  # seconds between requests

# --- Logging Setup ---
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler("crawler.log"),
        logging.StreamHandler()
    ]
)

def get_latest_paste_ids():
    """Scrape the archive page and extract the latest 30 Paste IDs."""
    try:
        resp = requests.get(ARCHIVE_URL, timeout=10)
        resp.raise_for_status()
    except Exception as e:
        logging.error(f"Failed to fetch archive page: {e}")
        return []

    soup = BeautifulSoup(resp.text, "html.parser")
    paste_ids = []
    for link in soup.select("table.maintable a"):
        href = link.get("href", "")
        if href.startswith("/") and len(href.strip("/")) == 8:  # Pastebin IDs are 8 chars
            paste_id = href.strip("/")
            if paste_id not in paste_ids:
                paste_ids.append(paste_id)
        if len(paste_ids) >= 30:
            break
    logging.info(f"Extracted {len(paste_ids)} paste IDs from archive.")
    return paste_ids

def fetch_paste_content(paste_id):
    """Fetch the raw content of a paste by its ID."""
    url = RAW_URL_TEMPLATE.format(paste_id)
    try:
        resp = requests.get(url, timeout=10)
        if resp.status_code == 404:
            logging.warning(f"Paste {paste_id} not found (404).")
            return None
        resp.raise_for_status()
        return resp.text
    except Exception as e:
        logging.error(f"Failed to fetch paste {paste_id}: {e}")
        return None

def find_keywords(text, keywords):
    """Return a list of keywords found in the text (case-insensitive)."""
    found = []
    text_lower = text.lower()
    for kw in keywords:
        if kw.lower() in text_lower:
            found.append(kw)
    return found

def main():
    paste_ids = get_latest_paste_ids()
    if not paste_ids:
        logging.error("No paste IDs found. Exiting.")
        return

    matches = 0
    with open(OUTPUT_FILE, "w", encoding="utf-8") as outfile:
        for idx, paste_id in enumerate(paste_ids, 1):
            logging.info(f"[{idx}/{len(paste_ids)}] Checking paste ID: {paste_id}")
            content = fetch_paste_content(paste_id)
            if content is None:
                logging.info(f"Skipped paste {paste_id} (could not fetch content).")
                time.sleep(REQUEST_DELAY)
                continue

            keywords_found = find_keywords(content, KEYWORDS)
            if keywords_found:
                discovered_at = datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ")
                result = {
                    "source": "pastebin",
                    "context": f"Found crypto-related content in Pastebin paste ID {paste_id}",
                    "paste_id": paste_id,
                    "url": RAW_URL_TEMPLATE.format(paste_id),
                    "discovered_at": discovered_at,
                    "keywords_found": keywords_found,
                    "status": "pending"
                }
                outfile.write(json.dumps(result) + "\n")
                matches += 1
                logging.info(f"Keywords found in paste {paste_id}: {keywords_found}")
            else:
                logging.info(f"No keywords found in paste {paste_id}. Skipped.")

            time.sleep(REQUEST_DELAY)  # Rate limiting

    logging.info(f"Done. {matches} matching pastes written to {OUTPUT_FILE}.")

if __name__ == "__main__":
    main()