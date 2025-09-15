import { chromium } from 'playwright';

async function run(pages = 16, baseUrl = 'https://www.bydfi.com/en/markets'){
  const browser = await chromium.launch({ headless: true });
  const context = await browser.newContext();
  const page = await context.newPage();
  const symbols = new Set();

  for(let n=1;n<=pages;n++){
    const url = `${baseUrl}?page=${n}`;
    try{
      await page.goto(url, { waitUntil: 'networkidle', timeout: 30000 });
    }catch(e){
      // try continue
    }

    // Try click the Perpetual menu item inside div.active.main-menu
    try{
      const perp = page.locator('div.active.main-menu >> text=Perpetual');
      if (await perp.count() > 0) {
        await perp.first().click();
        await page.waitForTimeout(400);
        await page.waitForLoadState('networkidle');
      }
    }catch(e){}

    // Try the dropdown with aria-label="Dropdown select" and choose USDT-M
    try{
      const dd = page.locator('[aria-label="Dropdown select"]');
      if (await dd.count() > 0){
        await dd.first().click();
        await page.waitForTimeout(300);
        const opt = page.locator('text=USDT-M');
        if (await opt.count() > 0){
          await opt.first().click();
          await page.waitForTimeout(600);
          await page.waitForLoadState('networkidle');
        }
      }
    }catch(e){}

    // Extract candidates by scanning visible text for tokens matching USDT patterns
    try{
      const found = await page.evaluate(()=>{
        const text = document.body ? document.body.innerText || '' : '';
        // match tokens like BTC/USDT, BTC_USDT, BTCUSDT, or BASE-USDT
        const re = /\b([A-Z0-9]{1,20}(?:[\/_-]?USDT|USDT))\b/g;
        const out = new Set();
        let m;
        while((m = re.exec(text)) !== null){
          let t = m[1].toUpperCase();
          t = t.replace(/[\/\-_]/g,'');
          if(!t.endsWith('USDT')) t = t + 'USDT';
          out.add(t);
        }
        return Array.from(out);
      });
      for(const s of found) symbols.add(s);
    }catch(e){}

    // small pause to be polite
    await page.waitForTimeout(200);
  }

  await browser.close();
  console.log(JSON.stringify(Array.from(symbols)));
}

const pages = parseInt(process.argv[2] || '16', 10);
const baseUrl = process.argv[3] || 'https://www.bydfi.com/en/markets';
run(pages, baseUrl).catch(e=>{ console.error(e); process.exit(2) });
