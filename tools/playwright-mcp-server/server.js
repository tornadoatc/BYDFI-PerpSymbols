import express from 'express'
import bodyParser from 'body-parser'
import { chromium } from 'playwright'

const app = express()
app.use(bodyParser.json({ limit: '2mb' }))

let browser

app.post('/render', async (req, res) => {
  const { url, timeout = 15000 } = req.body || {}
  if (!url) return res.status(400).json({ error: 'missing url' })

  try {
    if (!browser) browser = await chromium.launch({ headless: true })
    const context = await browser.newContext()
    const page = await context.newPage()
    await page.goto(url, { timeout, waitUntil: 'networkidle' })
    const html = await page.content()
    await page.close()
    await context.close()
    return res.json({ html })
  } catch (err) {
    return res.status(500).json({ error: String(err) })
  }
})

app.post('/close', async (_req, res) => {
  try {
    if (browser) await browser.close()
    browser = null
    res.json({ ok: true })
  } catch (err) {
    res.status(500).json({ error: String(err) })
  }
})

const port = process.env.PORT || 9222
app.listen(port, () => console.log(`playwright-mcp-server listening on ${port}`))
