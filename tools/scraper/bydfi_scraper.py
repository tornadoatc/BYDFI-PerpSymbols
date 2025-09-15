#!/usr/bin/env python3
"""Simple BYDFI Perpetual USDT-M symbols scraper.

Usage: python tools/scraper/bydfi_scraper.py --pages 16 --output ./symbols.csv
"""
import argparse
import csv
import sys
from pathlib import Path
import time
import requests
from bs4 import BeautifulSoup


def fetch_page(url, session, retries=3, backoff=1.0):
    for attempt in range(1, retries + 1):
        try:
            r = session.get(url, timeout=10)
            r.raise_for_status()
            return r.text
        except requests.RequestException as e:
            if attempt == retries:
                raise
            time.sleep(backoff * attempt)


def parse_symbols_from_html(html):
    """Return a set of base symbols found in Perpetual USDT-M listings.

    This function looks for table rows or listing elements that include 'Perpetual' and 'USDT-M'
    and extracts the base symbol text. It's intentionally permissive but tested in unit tests.
    """
    soup = BeautifulSoup(html, "lxml")
    symbols = set()

    # Try common table/list patterns
    for row in soup.select("tr, .market-row, li"):
        text = row.get_text(" ", strip=True)
        if not text:
            continue
        if "Perpetual" in text and ("USDT-M" in text or "USDT" in text):
            # crude extraction: find token that looks like SYMBOL/USDT or SYMBOLUSDT
            for token in text.replace("|", " ").split():
                if "/USDT" in token.upper():
                    base = token.split("/")[0].upper()
                    symbols.add(f"{base}USDT")
                elif token.upper().endswith("USDT") and len(token) > 4:
                    base = token[:-4].upper()
                    symbols.add(f"{base}USDT")

    return symbols


def main(argv=None):
    p = argparse.ArgumentParser()
    p.add_argument("--pages", type=int, default=16, help="Number of pages to fetch")
    p.add_argument("--output", type=Path, default=Path.cwd() / "symbols.csv")
    p.add_argument("--base-url", default="http://www.BYDFI.com/markets")
    args = p.parse_args(argv)

    session = requests.Session()
    all_symbols = set()

    for n in range(1, args.pages + 1):
        url = f"{args.base_url}?page={n}"
        try:
            html = fetch_page(url, session)
        except Exception as e:
            print(f"ERROR: failed to fetch page {n}: {e}", file=sys.stderr)
            return 2

        page_symbols = parse_symbols_from_html(html)
        all_symbols.update(page_symbols)

    out_path = args.output.expanduser().absolute()
    out_path.parent.mkdir(parents=True, exist_ok=True)
    with out_path.open("w", newline="") as f:
        writer = csv.writer(f)
        for s in sorted(all_symbols):
            writer.writerow([s])

    print(str(out_path))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
