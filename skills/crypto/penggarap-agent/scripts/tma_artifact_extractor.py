# Metadata: Origin Domain: Generic TMA (atfminers.asloni.online), Date: 2026-08-16, Symptom: Worker claimed success but provided NO valid VERIFICATION artifact.

import json

def extract_verification_artifact(page, wait_ms=5000):
    """
    Extracts state from localStorage and sessionStorage to act as a verification artifact
    when the DOM provides no clear success indicators (common in canvas/WebGL TMAs).
    """
    page.wait_for_timeout(wait_ms)
    
    artifact = {'url': page.url}
    try:
        artifact['localStorage'] = page.evaluate('JSON.stringify(window.localStorage)')
        artifact['sessionStorage'] = page.evaluate('JSON.stringify(window.sessionStorage)')
        
        for i, frame in enumerate(page.frames):
            if frame != page.main_frame:
                try:
                    artifact[f'frame_{i}_url'] = frame.url
                    artifact[f'frame_{i}_localStorage'] = frame.evaluate('JSON.stringify(window.localStorage)')
                except Exception:
                    pass
                
    except Exception as e:
        artifact['error'] = str(e)
        
    return artifact
