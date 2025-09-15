import { chromium } from 'playwright';

async function run(pages = 16, baseUrl = 'https://www.bydfi.com/en/markets'){
  const browser = await chromium.launch({ headless: true });
  const context = await browser.newContext();
  const page = await context.newPage();
  const all = [];

  for(let n=1;n<=pages;n++){
    const url = `${baseUrl}?page=${n}`;
    console.log(`--- page ${n} -> ${url}`);
    try{
      await page.goto(url, { waitUntil: 'networkidle', timeout: 30000 });
    }catch(e){ console.error('goto error', e.message); }

    // Try click Perpetual
    try{
      const perp = page.locator('div.active.main-menu >> text=Perpetual');
      const c = await perp.count();
      console.log('perp count', c);
      if (c>0){
        await perp.first().click();
        await page.waitForTimeout(400);
      }
    }catch(e){ console.error('perp click error', e.message); }

    // dropdown
    try{
      const dd = page.locator('[aria-label="Dropdown select"]');
      const c = await dd.count();
      console.log('dropdown count', c);
      if (c>0){
        await dd.first().click();
        await page.waitForTimeout(300);
        const opt = page.locator('text=USDT-M');
        const oc = await opt.count();
        console.log('opt count', oc);
        if (oc>0){
          await opt.first().click();
          await page.waitForTimeout(600);
        }
      }
    }catch(e){ console.error('dropdown error', e.message); }

    // extract
    try{
      const found = await page.evaluate(()=>{
        const text = document.body ? document.body.innerText || '' : '';
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
      console.log('found count', found.length, 'sample', found.slice(0,8));
      all.push({page:n, count: found.length, sample: found.slice(0,8)});
    }catch(e){ console.error('extract error', e.message); all.push({page:n, count:0, sample:[]}); }

    await page.waitForTimeout(200);
  }

  await browser.close();
  console.log('RESULTS_JSON_START');
  console.log(JSON.stringify(all));
  console.log('RESULTS_JSON_END');
}

const pages = parseInt(process.argv[2] || '16', 10);
run(pages).catch(e=>{ console.error(e); process.exit(2) });
