import { chromium } from 'playwright';
(async ()=>{
  const browser = await chromium.launch();
  const context = await browser.newContext();
  const page = await context.newPage();
  page.on('response', async r => {
    try{
      const req = r.request();
      const t = req.resourceType();
      if(t==='xhr' || t==='fetch'){
        const url = r.url();
        let body = '';
        try{ body = await r.text(); }catch(e){}
        console.log('XHR', url);
        if(body.length>0){
          console.log(body.slice(0,1000));
        }
      }
    }catch(e){console.error('resp error',e)}
  });
  await page.goto('https://www.bydfi.com/en/markets?page=1', {waitUntil:'networkidle'});
  await page.waitForTimeout(2000);
  await browser.close();
})();
