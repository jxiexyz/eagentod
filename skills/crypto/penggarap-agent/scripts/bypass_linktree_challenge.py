# Metadata: Origin Domain: linktr.ee, Date: 2026-08-26, Symptom: Challenge page or dynamic JS blocking link extraction
import time
from playwright.sync_api import Page

def bypass_challenge_and_extract(page: Page, target_selector: str = "a[href]") -> list:
    page.wait_for_timeout(5000)
    try:
        page.wait_for_load_state("networkidle", timeout=10000)
    except Exception:
        pass
    page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
    page.wait_for_timeout(2000)
    links = []
    elements = page.query_selector_all(target_selector)
    for el in elements:
        href = el.get_attribute("href")
        if href and href.startswith("http"):
            links.append(href)
    return list(set(links))