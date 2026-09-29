# Metadata: Domain: nft.retium.org, Date: 2026-08-22, Symptom: Form submission failure without specific DOM context

def bypass_evm_form(page, address_value, address_selector="input[placeholder*='0x'], input[name*='wallet'], input[name*='address']", submit_selector="button:has-text('Submit'), button:has-text('Join')"):
    page.wait_for_selector(address_selector, state="visible", timeout=15000)
    page.fill(address_selector, address_value)
    page.click(submit_selector)
    # ponytail: naive CSS selector cascade. add shadow-DOM traversal or iframe resolution when inputs are cross-origin.
