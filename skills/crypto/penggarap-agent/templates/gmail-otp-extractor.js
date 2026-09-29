const puppeteer = require('puppeteer-core');

(async () => {
    try {
        const browser = await puppeteer.connect({ browserURL: 'http://localhost:9222' });
        const pages = await browser.pages();
        let targetPage;
        for (const page of pages) {
            if (page.url().includes('mail.google.com')) {
                targetPage = page;
                break;
            }
        }
        
        if (targetPage) {
            // 1. Click the first relevant email row (Bypass Puppeteer click on unclickable nodes)
            await targetPage.evaluate(() => {
                const rows = Array.from(document.querySelectorAll('tr[role="row"]'));
                for (let i = 0; i < 5; i++) {
                    if (rows[i]) {
                        const text = rows[i].innerText;
                        // Change keyword based on project
                        if (text.includes('Code') || text.includes('verification') || text.includes('OTP')) {
                            rows[i].click();
                            return;
                        }
                    }
                }
                if(rows[0]) rows[0].click(); // fallback
            });
            
            // 2. Wait for email body to load
            await new Promise(r => setTimeout(r, 2000));
            
            // 3. Extract full text
            const text = await targetPage.evaluate(() => document.body.innerText);
            
            // 4. Regex for 6-digit code (adjust regex if alphanumeric or 4-digit)
            const codeMatch = text.match(/\b\d{6}\b/);
            if (codeMatch) {
                console.log('CODE_FOUND:' + codeMatch[0]);
            } else {
                console.log('CODE_NOT_FOUND');
            }
        } else {
            console.log('Gmail tab not found');
        }
        browser.disconnect();
    } catch (e) {
        console.error(e);
    }
})();
