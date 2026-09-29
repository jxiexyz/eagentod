# Metadata: Domain: thefallennft.com, Date: 2026-08-27, Symptom: t.me links blocked in precheck
import re
import urllib.parse

def bypass(page, url=""):
    match = re.search(r'(?:t\.me/|tg://resolve\?domain=)([^/?&#]+)', url)
    if match:
        qs = urllib.parse.parse_qs(urllib.parse.urlparse(url).query)
        return {"bot": match.group(1), "start": qs.get('start', qs.get('startapp', ['']))[0]}
    
    for link in page.locator("a[href*='t.me/'], a[href*='tg://']").all():
        href = link.get_attribute("href")
        if href and (m := re.search(r'(?:t\.me/|tg://resolve\?domain=)([^/?&#]+)', href)):
            qs = urllib.parse.parse_qs(urllib.parse.urlparse(href).query)
            return {"bot": m.group(1), "start": qs.get('start', qs.get('startapp', ['']))[0]}
    return None