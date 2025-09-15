Playwright MCP Server

Small Express server that uses Playwright to render pages and return the fully rendered HTML.

Install and run:

```bash
cd tools/playwright-mcp-server
npm install
node server.js
```

Example request (curl):

```bash
curl -sS -X POST http://localhost:9222/render -H 'Content-Type: application/json' \
  -d '{"url":"https://www.bydfi.com/en/markets?page=1"}' | jq -r .html | head -n 50
```
