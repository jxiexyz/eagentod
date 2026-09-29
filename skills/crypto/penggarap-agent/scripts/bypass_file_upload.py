# Metadata: Origin Domain: app.zen-o.xyz, Date: 2026-08-23, Specific Symptom: Mission #13 video upload failure.

async def bypass_file_upload(page, trigger_selector: str, file_path: str):
    """
    Handles hidden or complex file input uploads by intercepting the file chooser.
    """
    import os
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"File not found: {file_path}")

    try:
        # Fast path: try direct input file setting if an input[type=file] is available
        input_element = await page.query_selector("input[type='file']")
        if input_element:
            await input_element.set_input_files(file_path)
            return True
    except Exception:
        pass

    # Fallback: click the visual trigger and intercept the file chooser event
    async with page.expect_file_chooser() as fc_info:
        await page.click(trigger_selector)
    file_chooser = await fc_info.value
    await file_chooser.set_files(file_path)
    return True
