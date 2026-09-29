# Metadata: Generic (from jacon.codes), 2026-08-27, Symptom: Max tool iterations hit due to multi-step UI
import time
import logging

# Helper to execute many UI interactions in a single tool call,
# preventing the agent from exhausting its max iteration limit on step-by-step UI tasks.
def run_ui_sequence(page, sequence, delay_between_steps=1.5):
    """
    Executes a sequence of actions (clicks, fills) in one Playwright execution.
    
    :param page: Playwright Page object.
    :param sequence: List of dictionaries defining actions.
        Example:
        [
            {'action': 'click', 'text': 'ENTER JACON LAB'},
            {'action': 'click', 'selector': '.some-class button'},
            {'action': 'fill', 'selector': 'input[name="wallet"]', 'value': '0x123...'}
        ]
    :param delay_between_steps: Sleep time between actions to allow UI transitions.
    """
    execution_log = []
    for step in sequence:
        action = step.get('action', 'click')
        try:
            if action == 'click':
                if 'text' in step:
                    target = page.locator(f"text=\"{step['text']}\"").first
                    # Fallback to button containing text if exact text node isn't clickable
                    if not target.is_visible(timeout=2000):
                        target = page.locator(f"button:has-text(\"{step['text']}\")").first
                else:
                    target = page.locator(step['selector']).first
                
                target.wait_for(state="visible", timeout=5000)
                target.click()
                execution_log.append(f"Success: Clicked {step.get('text') or step.get('selector')}")
                
            elif action == 'fill':
                target = page.locator(step['selector']).first
                target.wait_for(state="visible", timeout=5000)
                target.fill(step['value'])
                execution_log.append(f"Success: Filled {step['selector']}")
                
            time.sleep(delay_between_steps)
            
        except Exception as e:
            err_msg = f"Failed step {step}: {str(e)}"
            execution_log.append(err_msg)
            logging.warning(err_msg)
            # Yield partial success state rather than full crash
            break
            
    return {
        "status": "completed_sequence", 
        "steps_executed": len(execution_log),
        "log": execution_log,
        "current_url": page.url
    }
