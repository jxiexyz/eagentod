# Metadata: Origin Domain: teogiwa.com (Generic), Date: 2026-08-23, Symptom: Failure to extract PFP from source and update X profile/post

import time
import os

def bypass_cross_domain_pfp_post(page, x_page, image_selector, tweet_text, save_path="/tmp/pfp.png"):
    """
    Downloads an image from a target page, sets it as the X (Twitter) profile picture, and posts a tweet.
    Assumes x_page is an authenticated CDP session on x.com.
    """
    # 1. Download/Screenshot PFP from source page
    page.bring_to_front()
    page.wait_for_selector(image_selector, state="visible", timeout=10000)
    element = page.locator(image_selector).first
    element.scroll_into_view_if_needed()
    element.screenshot(path=save_path)

    # 2. Update X Profile
    x_page.bring_to_front()
    x_page.goto("https://x.com/settings/profile")
    x_page.wait_for_selector('input[type="file"]', state="attached", timeout=10000)
    
    # Upload avatar (usually the first file input)
    file_inputs = x_page.locator('input[type="file"]')
    file_inputs.nth(0).set_input_files(save_path)
    
    # Handle crop/apply modal
    apply_btn = x_page.locator('[data-testid="applyButton"]')
    try:
        apply_btn.wait_for(state="visible", timeout=5000)
        apply_btn.click()
    except Exception:
        pass
        
    # Save profile
    save_btn = x_page.locator('[data-testid="Profile_Save_Button"]')
    save_btn.click()
    time.sleep(3) # Wait for backend sync

    # 3. Post Tweet
    x_page.goto("https://x.com/compose/tweet")
    x_page.wait_for_selector('[data-testid="tweetTextarea_0"]', state="visible", timeout=10000)
    x_page.fill('[data-testid="tweetTextarea_0"]', tweet_text)
    x_page.click('[data-testid="tweetButton"]')
    time.sleep(3)
    
    # Cleanup
    if os.path.exists(save_path):
        os.remove(save_path)
        
    return True
