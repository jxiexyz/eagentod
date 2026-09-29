# Metadata: Domain: Generic (origin teogiwa.com), Date: 2026-08-23, Symptom: Failure to download PFP and update X profile
import os
import base64

async def download_image(page, selector, save_path="/tmp/pfp.jpg"):
    element = await page.wait_for_selector(selector, state="visible", timeout=10000)
    src = await element.evaluate("el => el.src || ''")
    if src.startswith("http"):
        b64 = await page.evaluate("""async (url) => {
            const res = await fetch(url);
            const blob = await res.blob();
            return new Promise((resolve) => {
                const reader = new FileReader();
                reader.onloadend = () => resolve(reader.result);
                reader.readAsDataURL(blob);
            });
        }""", src)
        encoded = b64.split(",", 1)[1]
        with open(save_path, "wb") as f:
            f.write(base64.b64decode(encoded))
    else:
        await element.screenshot(path=save_path)
    return save_path

async def update_x_profile_and_post(x_page, image_path, post_text):
    await x_page.goto("https://x.com/settings/profile")
    async with x_page.expect_file_chooser() as fc_info:
        await x_page.click('div[aria-label*="photo" i]')
    await fc_info.value.set_files(image_path)
    await x_page.click('[data-testid="applyButton"]')
    await x_page.click('[data-testid="Profile_Save_Button"]')
    await x_page.wait_for_timeout(3000)
    
    await x_page.goto("https://x.com/compose/tweet")
    await x_page.fill('[data-testid="tweetTextarea_0"]', post_text)
    await x_page.click('[data-testid="tweetButton"]')
