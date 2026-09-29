# Metadata: bafoontown.wtf, 2026-08-23, Physical video upload requirement bypass
import os

async def execute(page, selector="input[type='file']", file_path="/tmp/mock_video.mp4"):
    if not os.path.exists(file_path):
        with open(file_path, "wb") as f:
            f.write(b'\x00\x00\x00\x20ftypisom\x00\x00\x02\x00isomiso2avc1mp41')
            f.write(os.urandom(1024))
    input_element = await page.wait_for_selector(selector, state="attached")
    await input_element.set_input_files(file_path)
    return True