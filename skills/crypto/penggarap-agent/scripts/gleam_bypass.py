#!/usr/bin/env python3
"""
Gleam.io Universal Automator for Penggarap Agent
Handles Contestant Details modal, X actions, Questions/UIDs, and Angular event confirmation.
"""
import asyncio
import sys
from playwright.async_api import async_playwright

async def garap_gleam(target_url=None, uid="947222755", handle="chiquast"):
    async with async_playwright() as p:
        browser = await p.chromium.connect_over_cdp("http://localhost:9222")
        context = browser.contexts[0]
        
        gleam_page = None
        for page in context.pages:
            if "gleam.io" in page.url:
                gleam_page = page
                break
                
        if not gleam_page:
            if target_url:
                gleam_page = await context.new_page()
                await gleam_page.goto(target_url, timeout=45000)
            else:
                print("No Gleam page found")
                return False
                
        await asyncio.sleep(3)
        
        # 1. Check & Handle X OAuth Popups if open
        oauth_page = next((p for p in context.pages if "oauth2/authorize" in p.url or "api.x.com" in p.url), None)
        if oauth_page:
            await oauth_page.evaluate('''() => {
                const btn = document.querySelector('[data-testid="OAuth_Consent_Button"]') || 
                            Array.from(document.querySelectorAll('button, div[role="button"]')).find(b => b.innerText.includes('Authorize') || b.innerText.includes('Izinkan'));
                if (btn) btn.click();
            }''')
            await asyncio.sleep(4)
            
        # 2. Check and fill Contestant Form if visible
        await gleam_page.evaluate('''({uid, handle}) => {
            const inputs = document.querySelectorAll('input, textarea');
            for (const input of inputs) {
                const name = (input.name || '').toLowerCase();
                const placeholder = (input.placeholder || '').toLowerCase();
                const label = input.closest('label, .form-group, .form-compact__part') ? input.closest('label, .form-group, .form-compact__part').innerText.toLowerCase() : '';
                
                if (name.includes('field_') || label.includes('uid') || placeholder.includes('uid')) {
                    input.value = uid;
                    input.dispatchEvent(new Event('input', { bubbles: true }));
                    input.dispatchEvent(new Event('change', { bubbles: true }));
                } else if (label.includes('handle') || label.includes('twitter') || label.includes('x handle')) {
                    input.value = handle;
                    input.dispatchEvent(new Event('input', { bubbles: true }));
                    input.dispatchEvent(new Event('change', { bubbles: true }));
                }
            }
            
            // Angular sync
            const scope = angular.element(document.body).scope();
            if (scope && scope.contestantState && scope.contestantState.form && scope.contestantState.form_additional_fields) {
                for (const key in scope.contestantState.form_additional_fields) {
                    const f = scope.contestantState.form_additional_fields[key];
                    if (f.label && f.label.toLowerCase().includes('uid')) scope.contestantState.form[key] = uid;
                    if (f.label && (f.label.toLowerCase().includes('handle') || f.label.toLowerCase().includes('x'))) scope.contestantState.form[key] = handle;
                }
                scope.$apply();
            }
            
            const saveBtn = Array.from(document.querySelectorAll('button, a, input[type="submit"]')).find(b => b.innerText.trim() === 'Save' && b.offsetParent !== null);
            if (saveBtn) saveBtn.click();
        }''', {'uid': uid, 'handle': handle})
        
        await asyncio.sleep(3)
        
        # 3. Process each entry method
        methods_count = await gleam_page.locator(".entry-method").count()
        for i in range(methods_count):
            await gleam_page.evaluate('''(idx) => {
                const m = document.querySelectorAll(".entry-method")[idx];
                if (!m) return;
                const scope = angular.element(m).scope();
                if (scope && scope.entry_method) {
                    if (scope.isEntered && scope.isEntered(scope.entry_method)) return;
                    if (scope.triggerVisit) scope.triggerVisit(scope.entry_method);
                    if (scope.confirmAction) scope.confirmAction(scope.entry_method, scope.entryState.formData[scope.entry_method.id] || {});
                    scope.$apply();
                }
            }''', i)
            await asyncio.sleep(2)
            
        await gleam_page.evaluate("() => window.scrollTo(0, 0)")
        entries = await gleam_page.evaluate('''() => {
            const el = document.querySelector('.incentive-metric, .user-entry-count');
            return document.body.innerText.substring(0, 200);
        }''')
        print("Final Status:", entries)
        return True

if __name__ == "__main__":
    url = sys.argv[1] if len(sys.argv) > 1 else None
    asyncio.run(garap_gleam(url))
