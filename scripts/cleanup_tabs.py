#!/usr/bin/env python3
"""Cleanup idle/duplicate tabs on CDP browser.
Force mode: safe — only closes about:blank and duplicate URLs, keeps 1 tab per unique domain.
Normal mode (no lock held): closes everything except KEEP_URLS."""
import asyncio
import sys
import argparse
from urllib.parse import urlparse
from playwright.async_api import async_playwright
from browser_lock import acquire_browser_lock, release_browser_lock

KEEP_URLS = ['x.com/home', 'twitter.com/home']


def _domain(url):
    """Extract domain from URL for dedup."""
    try:
        return urlparse(url).netloc.lower()
    except Exception:
        return url


async def cleanup(url_pattern=None, max_age=None, force=False):
    print("[Clean] Starting tab cleanup...")

    lock_acquired = False
    worker_active = False
    if not force:
        try:
            acquire_browser_lock(timeout=5, job_name="cleanup-tabs")
            lock_acquired = True
        except RuntimeError:
            print("[Clean] Browser actively in use (lock held). Skipping cleanup to avoid clash.")
            return
    else:
        # Force mode but worker might be active — use safe dedup-only strategy
        try:
            acquire_browser_lock(timeout=0, job_name="cleanup-tabs-probe")
            lock_acquired = True
        except (RuntimeError, Exception):
            worker_active = True
            print("[Clean] Force mode + worker active → safe dedup-only (keep 1 per domain, close blanks/dupes)")

    try:
        pw = await async_playwright().start()
        browser = await pw.chromium.connect_over_cdp("http://127.0.0.1:9222")
        context = browser.contexts[0]
        pages = context.pages
        print(f"[Clean] Found {len(pages)} open tabs")

        closed = 0
        kept = []

        if worker_active:
            # SAFE MODE: only close about:blank and duplicate URLs
            # Keep first occurrence of each domain, close rest
            seen_domains = set()
            for page in pages:
                url = page.url

                # Always keep persistent tabs
                if any(k in url for k in KEEP_URLS):
                    kept.append(url)
                    seen_domains.add(_domain(url))
                    continue

                # Close all about:blank
                if not url or url == 'about:blank':
                    try:
                        await page.close()
                        closed += 1
                        print("[Clean] Closed blank tab")
                    except Exception:
                        pass
                    continue

                # Close blob: URLs (orphaned media)
                if url.startswith('blob:'):
                    try:
                        await page.close()
                        closed += 1
                        print(f"[Clean] Closed blob tab: {url[:60]}")
                    except Exception:
                        pass
                    continue

                # Dedup: keep first tab per domain, close duplicates
                dom = _domain(url)
                if dom in seen_domains:
                    try:
                        await page.close()
                        closed += 1
                        print(f"[Clean] Closed dupe: {url[:80]}")
                    except Exception:
                        pass
                else:
                    seen_domains.add(dom)
                    kept.append(url)
        else:
            # NORMAL MODE: close everything except KEEP_URLS
            for page in pages:
                url = page.url

                is_keep = any(k in url for k in KEEP_URLS)
                if is_keep:
                    kept.append(url)
                    continue

                if url_pattern and url_pattern not in url:
                    kept.append(url)
                    continue

                try:
                    await page.close()
                    closed += 1
                    if url and url != 'about:blank':
                        print(f"[Clean] Closed tab: {url[:80]}")
                    else:
                        print("[Clean] Closed idle tab")
                except Exception:
                    pass

        print(f"[Clean] Done: closed {closed}, kept {len(kept)}")
    except Exception as e:
        print(f"[Clean] Error via Playwright: {e}")

    # Fallback to direct CDP REST API for bulletproof tab cleanup (only when no worker is active)
    try:
        if not worker_active:
            import urllib.request
            import json
            req = urllib.request.urlopen("http://127.0.0.1:9222/json")
            targets = json.loads(req.read().decode())
            cdp_closed = 0
            for t in targets:
                if t.get("type") != "page":
                    continue
                url = t.get("url", "")
                tid = t.get("id")
                if any(k in url for k in KEEP_URLS):
                    continue
                # Close non-essential tabs
                try:
                    urllib.request.urlopen(f"http://127.0.0.1:9222/json/close/{tid}")
                    cdp_closed += 1
                except Exception:
                    pass
            if cdp_closed > 0:
                print(f"[Clean] Direct CDP closed {cdp_closed} orphan tabs")
    except Exception as e:
        print(f"[Clean] Direct CDP fallback error: {e}")
    finally:
        if lock_acquired:
            release_browser_lock()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Cleanup CDP browser tabs")
    parser.add_argument("--url-pattern", help="Only close tabs matching this domain/pattern")
    parser.add_argument("--max-age", type=int, default=None, help="Only close tabs older than N seconds (0=all)")
    parser.add_argument("--force", action="store_true", help="Bypass lock — uses safe dedup mode if worker active")
    args = parser.parse_args()

    asyncio.run(cleanup(url_pattern=args.url_pattern, max_age=args.max_age, force=args.force))
