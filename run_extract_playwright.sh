#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$ROOT"

# Rotate existing CSV if present
if [ -f out_symbols_live.csv ]; then
  ts=$(date +%Y%m%dT%H%M%S)
  mv out_symbols_live.csv "out_symbols_live.${ts}.csv"
  echo "rotated existing out_symbols_live.csv -> out_symbols_live.${ts}.csv"
fi

# Start Playwright MCP server
echo "Starting Playwright MCP server..."
cd tools/playwright-mcp-server
npm install --no-audit --no-fund >/dev/null 2>&1 || true
# ensure Chromium present
npx playwright install chromium >/dev/null 2>&1 || true
nohup node server.js > server.log 2>&1 &
PID=$!
echo $PID > "$ROOT/playwright_server.pid"
echo "server pid $PID"
cd "$ROOT"

echo "Running interactive extraction (DOM) to assist discovery..."
node tools/playwright-mcp-server/extract_perpetual_usdtm.js 16 | jq -r '.[]' > out_symbols_live.dom.csv || true

echo "Running authoritative perpetual contract fetch..."
source .venv/bin/activate || true
python tools/scraper/fetch_perpetual_contracts.py

echo "Stopping Playwright MCP server..."
if [ -f playwright_server.pid ]; then
  kill "$(cat playwright_server.pid)" || true
  rm -f playwright_server.pid
fi

echo "Done. new out_symbols_live.csv created at: $ROOT/out_symbols_live.csv"
