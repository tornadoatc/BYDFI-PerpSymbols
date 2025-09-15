BYDFI Perpetual USDT-M Symbols

This repository contains tools to extract Perpetual USDT-M symbols from BYDFI (https://www.bydfi.com).

Contents
- `tools/scraper/` - Python scripts to fetch symbols (API and HTML parsers).
- `tools/playwright-mcp-server/` - Node.js Playwright server used to render pages and capture XHR for debugging.
- `run_extract_playwright.sh` - Convenience script to start the server, run extractors, rotate CSV output, and stop the server.
- `out_symbols_live.csv` - Latest extracted list of Perpetual USDT-M symbols.

Usage
1. Install Python dependencies (use a virtualenv).
   - Recommended: `pip install -r tools/scraper/requirements.txt` (if provided) or install `requests` and `beautifulsoup4`.
2. To run the authoritative extractor (uses BYDFI swap API):
   - `python3 tools/scraper/fetch_perpetual_contracts.py`
3. To run the Playwright render server (optional, for debugging):
   - `cd tools/playwright-mcp-server` then `npm install` then `node server.js`
4. To run the full automated flow (starts server, runs extractors, rotates CSV):
   - `./run_extract_playwright.sh`

Notes
- The scraper prefers the site's API (`/swap/public/common/exchangeInfo`) for authoritative contract metadata. DOM scraping is brittle and used only for debugging.
- This repository includes some Playwright browser artifacts; consider running `npm ci` inside `tools/playwright-mcp-server` only when needed.

License
- This project follows the license of the primary author (none specified here). Use responsibly.
# BYDFI Perpetual USDT-M symbols scraper

Small tool to scrape http://www.BYDFI.com/markets pages for Perpetual USDT-M symbols and write a CSV of `<symbol>USDT`.

Requirements: Python 3.10+, pip install requests beautifulsoup4 lxml

Run the scraper:

```bash
python tools/scraper/bydfi_scraper.py --pages 16 --output ./symbols.csv
```

Run tests (pytest):

```bash
pip install pytest
pytest -q
```
