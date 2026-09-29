const puppeteer = require('puppeteer-core');

(async () => {
    // 1. Dynamically fetch the WebSocket URL from the running CDP browser
    const response = await fetch('http://localhost:9222/json/version');
    const data = await response.json();
    const wsUrl = data.webSocketDebuggerUrl;

    // 2. Connect to the existing session (Crucial to preserve Google/X/Discord logins)
    const browser = await puppeteer.connect({ browserWSEndpoint: wsUrl, defaultViewport: null });
    
    // 3. Open a new page for this specific task
    const page = await browser.newPage();
    
    try {
        console.log("Navigating...");
        await page.goto('TARGET_URL_HERE', { waitUntil: 'networkidle2', timeout: 30000 });
        
        // Wait for dynamic React/VDOM rendering
        await new Promise(r => setTimeout(r, 5000));
        
        // --- INJECT CUSTOM LOGIC HERE ---
        // Example:
        // await page.evaluate(() => {
        //     const el = document.querySelector('input');
        //     if (el) {
        //         el.value = 'data';
        //         el.dispatchEvent(new Event('input', {bubbles: true}));
        //         el.dispatchEvent(new Event('change', {bubbles: true}));
        //     }
        // });
        
    } catch (err) {
        console.error("Script execution failed:", err);
    } finally {
        // 4. CLEANUP (CRITICAL PITFALL PREVENTION)
        // MUST close the specific page to prevent RAM leaks.
        await page.close();
        // MUST ONLY disconnect from the browser. 
        // NEVER call browser.close() or the entire 9222 CDP session dies!
        browser.disconnect();
    }
})();
