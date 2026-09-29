# Metadata: rewards.svpstars.com, 2026-09-20, ZEC Noir string match validation failure
import os
import importlib.util

def fill_zec_noir_address(page, input_selector: str):
    path = os.path.expanduser("~/airdrop_identity.py")
    spec = importlib.util.spec_from_file_location("airdrop_identity", path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    
    addr = getattr(mod, "zec_wallet", "")
    if not addr.startswith("u1"):
        raise ValueError("Require u1... ZEC UA (Noir/Vizor)")
        
    page.wait_for_selector(input_selector)
    page.fill(input_selector, addr)
    return addr
