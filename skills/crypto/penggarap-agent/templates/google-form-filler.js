// Template: Auto-fill and submit multistage Google Forms via Puppeteer (CDP port 9222)
// Run via terminal: node ~/.hermes/scripts/fill_google_form.js
// Description: Automatically finds unselected radio groups, empty text inputs, and 
// clicks "Berikutnya" (Next) or "Kirim" (Submit) iteratively until completion.

const puppeteer = require('puppeteer-core');

(async () => {
    try {
        const browser = await puppeteer.connect({ browserURL: 'http://127.0.0.1:9222' });
        const pages = await browser.pages();
        let targetPage = pages.find(p => p.url().includes('docs.google.com/forms'));

        if (!targetPage) {
            console.log("Error: Target Google Form page not found.");
            process.exit(1);
        }

        let hasNext = true;
        let iterCount = 0;
        const maxIters = 10; // Prevent infinite loops in paginated forms
        
        while (hasNext && iterCount < maxIters) {
             iterCount++;
             await new Promise(r => setTimeout(r, 1000)); // Wait for page transitions/renders
             
             // 1. Fill Empty Text Inputs
             const textInputs = await targetPage.$$('input[type="text"]:not([disabled])');
             for (const input of textInputs) {
                if (!(await targetPage.evaluate(el => el.value, input))) {
                   await input.type("Tentu saja"); // Customize fallback text as needed
                }
             }

             // 2. Fill Empty Text Areas
             const textAreas = await targetPage.$$('textarea:not([disabled])');
             for (const ta of textAreas) {
                if (!(await targetPage.evaluate(el => el.value, ta))) {
                   await ta.type("Sangat setuju dan informatif"); // Customize fallback text as needed
                }
             }

             // 3. Select First Unselected Radio Button per Group
             // Google Forms groups radio buttons in div[role="radiogroup"]
             const radioGroups = await targetPage.$$('div[role="radiogroup"]');
             for (const group of radioGroups) {
                 const isChecked = await group.$('div[aria-checked="true"]');
                 if (!isChecked) {
                      const firstRadio = await group.$('div[role="radio"]');
                      if (firstRadio) {
                          await firstRadio.click();
                          await new Promise(r => setTimeout(r, 200));
                      }
                 }
             }
             
             // 4. Find and Click Next / Submit Button
             const buttons = await targetPage.$$('div[role="button"]');
             let clickedAction = false;
             for (const btn of buttons) {
                 const text = await targetPage.evaluate(el => el.innerText, btn);
                 if (!text) continue;
                 
                 const t = text.toLowerCase();
                 if (t.includes('berikutnya') || t.includes('next')) {
                     await btn.click();
                     clickedAction = true;
                     await new Promise(r => setTimeout(r, 2000));
                     break;
                 } else if (t.includes('kirim') || t.includes('submit')) {
                     await btn.click();
                     clickedAction = true;
                     hasNext = false; // Stop iterating, form submitted
                     await new Promise(r => setTimeout(r, 3000));
                     break;
                 }
             }
             
             if (!clickedAction) {
                 console.log("No Next/Submit found or reached end of form without submit.");
                 break;
             }
        }
        
        // 5. Verify Success Message
        await new Promise(r => setTimeout(r, 2000));
        const bodyText = await targetPage.evaluate(() => document.body.innerText);
        if (bodyText.match(/(telah direkam|terima kasih|recorded|success)/i)) {
            console.log("SUCCESS");
        } else {
            console.log("Could not confirm success from page text.");
        }
        
        // Always close target tab when finished to save memory
        await targetPage.close();
        process.exit(0);

    } catch (error) {
        console.error("Error:", error);
        process.exit(1);
    }
})();
