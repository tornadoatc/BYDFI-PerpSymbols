# Feature Specification: Build a BYDFI Perpetual USDT-M symbols scraper

**Feature Branch**: `001-build-an-application`  
**Created**: 2025-09-15  
**Status**: Draft  
**Input**: User description: "Build an application that will scrape data from the http://www.BYDFI.com/markets page for the Perpetual USDT-M symbols across 16 pages and output a CSV of <symbol>USDT."

## Execution Flow (main)
```
1. Parse user description from Input
	→ If empty: ERROR "No feature description provided"
2. Identify target pages (16 pages of markets) and Perpetual USDT-M symbol rows
3. For each page (1..16):
	→ Fetch HTML page
	→ Parse rows identifying Perpetual USDT-M listings
	→ Extract base symbol and normalize to `<symbol>USDT`
4. Aggregate unique symbols across all pages
5. Write CSV file with one symbol per line in format `<symbol>USDT`
6. Return: SUCCESS with path to CSV and count of symbols
```

---

## ⚡ Quick Guidelines
- ✅ Focus on WHAT and WHY: extract Perpetual USDT-M symbols and produce a CSV for downstream use
- ❌ Avoid implementation platform lock-in in this spec; the implementation below will propose a concrete, low-risk approach

### Section Requirements
- **Mandatory sections**: Completed below

---

## User Scenarios & Testing *(mandatory)*

### Primary User Story
As a data engineer, I need a small tool that scrapes BYDFI market pages to collect all Perpetual USDT-M trading symbols so I can import them into downstream pipelines as a CSV list.

### Acceptance Scenarios
1. Given the site is reachable, when the scraper runs, then it fetches 16 pages, extracts all Perpetual USDT-M symbols, and writes a CSV file with one normalized symbol per line (e.g., `BTCUSDT`).
2. Given duplicate symbol appearances across pages, when aggregation completes, then the CSV contains no duplicates.
3. Given a network error on a page fetch, when retries are exhausted, then the run fails with a non-zero exit code and an error log indicating which page(s) failed.

### Edge Cases
- If site layout changes (HTML structure), the parser should fail fast and emit a helpful message indicating parsing failure and an example snippet.
- If fewer than expected pages exist, the tool should still process available pages and report the pages processed.
- Rate-limiting or temporary 429 responses: implement exponential backoff with jitter and a small number of retries.

## Requirements *(mandatory)*

### Functional Requirements
- **FR-001**: System MUST fetch market pages 1 through 16 (configurable) from `http://www.BYDFI.com/markets?page=<n>`.
- **FR-002**: System MUST identify and extract only Perpetual USDT-M symbols.
- **FR-003**: System MUST normalize extracted symbols to the format `<symbol>USDT` (uppercase, no separators).
- **FR-004**: System MUST deduplicate symbols across pages.
- **FR-005**: System MUST write the final CSV to a configurable output path and return the absolute path on success.
- **FR-006**: System MUST exit with non-zero status on unrecoverable errors (network, parsing) and provide logs.
- **FR-007**: System SHOULD retry transient HTTP errors with exponential backoff (configurable attempts).

### Key Entities
- **Symbol**: Represents a base trading symbol extracted from a Perpetual USDT-M listing (e.g., `BTC`) with normalized output `BTCUSDT`.

---

## Review & Acceptance Checklist

### Content Quality
- [x] No implementation details that lock the project into a single platform (implementation notes below are suggestions)
- [x] Focused on user value and business needs
- [x] All mandatory sections completed

### Requirement Completeness
- [ ] No [NEEDS CLARIFICATION] markers remain
- [x] Requirements are testable and unambiguous
- [x] Success criteria are measurable (CSV path, symbol count)

---

## Execution Status
- [x] User description parsed
- [x] Key concepts extracted
- [x] Ambiguities marked: none required (assumed site structure stable)
- [x] User scenarios defined
- [x] Requirements generated
- [x] Entities identified
- [ ] Review checklist passed

---

## Implementation notes (suggested, not prescriptive)
- Language: Python 3.10+ (single-file CLI) or Node.js script are acceptable.
- Use `requests` or `httpx` for HTTP and `beautifulsoup4` or `lxml` for HTML parsing (if Python).
- Add a small unit test for the parser using a saved sample page HTML.
- Output CSV format: one symbol per line, no header.

## Next steps
1. Implement scraper as a small Python CLI in `tools/scraper/bydfi_scraper.py`.
2. Add a unit test in `tests/test_parser.py` and a sample HTML under `tests/fixtures/`.
3. Run scraper and commit code to branch `001-build-an-application`.
4. Create a short README with usage and install instructions.

