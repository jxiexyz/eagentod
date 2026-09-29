# Metadata: app.zen-o.xyz, 2026-08-23, Fails to upload required video for mission tasks.
import os

async def handle_media_upload(page, selector: str, filepath: str = "/tmp/dummy.mp4"):
    if not os.path.exists(filepath):
        with open(filepath, "wb") as f:
            f.write(b"\x00\x00\x00\x1cftypisom\x00\x00\x02\x00isomiso2avc1mp41\x00\x00\x00\x08free")
    
    await page.evaluate("(sel) => { const el = document.querySelector(sel); if(el) { el.style.display = 'block'; el.style.opacity = 1; el.style.visibility = 'visible'; } }", selector)
    await page.set_input_files(selector, filepath)
