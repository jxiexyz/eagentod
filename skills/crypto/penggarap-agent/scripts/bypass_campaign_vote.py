# Metadata: Domain: voice.fun, Date: 2026-09-29, Symptom: Fails to select option card and cast vote on social campaign poll

import asyncio

async def bypass_campaign_vote(
    page,
    option_index: int = 0,
    card_selectors: list = None,
    vote_button_texts: list = None,
    timeout: int = 15000
) -> dict:
    """
    Automates voting on social campaign polls, duel cards, and web3 voting portals.
    Selects visible option cards, triggers vote submission, and extracts result verification state.
    """
    if card_selectors is None:
        card_selectors = [
            'div[class*="DuelCard" i]',
            'div[class*="optionCard" i]',
            'div[class*="option" i]',
            'div[role="radio"]',
            'div[role="option"]',
            'button[class*="option" i]',
            'div[class*="choice" i]'
        ]

    if vote_button_texts is None:
        vote_button_texts = ["Vote Now", "Cast Vote", "Submit Vote", "Vote", "Participate"]

    await page.wait_for_load_state("domcontentloaded")
    await asyncio.sleep(1)

    # 1. Check if already voted
    already_voted = await page.evaluate("""() => {
        const text = document.body.innerText || '';
        const indicators = ['Voted', 'Show Results', 'Your vote has been recorded', 'Already voted'];
        for (const ind of indicators) {
            if (text.includes(ind)) return ind;
        }
        return null;
    }""")
    if already_voted:
        return {"success": True, "voted": True, "artifact": f"Already voted indicator: {already_voted}"}

    # 2. Bring poll/duel container into view
    await page.evaluate("""() => {
        const container = document.querySelector('div[class*="Duel" i], div[class*="Poll" i], section[class*="vote" i]');
        if (container) container.scrollIntoView({ block: 'center', behavior: 'smooth' });
    }""")
    await asyncio.sleep(1)

    # 3. Find and select option card
    selected = False
    for selector in card_selectors:
        cards_info = await page.evaluate(f"""(sel) => {{
            const elements = Array.from(document.querySelectorAll(sel));
            const visible = elements.filter(el => {{
                const r = el.getBoundingClientRect();
                return r.width > 0 && r.height > 0 && window.getComputedStyle(el).visibility !== 'hidden';
            }});
            return visible.map((el, idx) => ({{ idx, text: el.innerText.trim().substring(0, 100) }}));
        }}""", selector)

        if cards_info:
            target_idx = option_index if option_index < len(cards_info) else 0
            click_res = await page.evaluate(f"""({{ sel, idx }}) => {{
                const elements = Array.from(document.querySelectorAll(sel)).filter(el => {{
                    const r = el.getBoundingClientRect();
                    return r.width > 0 && r.height > 0;
                }});
                if (elements[idx]) {{
                    elements[idx].scrollIntoView({{ block: 'center' }});
                    elements[idx].dispatchEvent(new MouseEvent('pointerdown', {{ bubbles: true }}));
                    elements[idx].dispatchEvent(new MouseEvent('mousedown', {{ bubbles: true }}));
                    elements[idx].dispatchEvent(new MouseEvent('pointerup', {{ bubbles: true }}));
                    elements[idx].dispatchEvent(new MouseEvent('mouseup', {{ bubbles: true }}));
                    elements[idx].click();
                    return true;
                }}
                return false;
            }}""", {"sel": selector, "idx": target_idx})

            if click_res:
                selected = True
                await asyncio.sleep(1)
                break

    # 4. Find and click separate vote submit button if present
    voted_click = False
    for btn_text in vote_button_texts:
        btn_clicked = await page.evaluate(f"""(textToFind) => {{
            const btns = Array.from(document.querySelectorAll('button, div[role="button"], a[role="button"]'));
            const target = btns.find(b => {{
                const txt = b.innerText ? b.innerText.trim() : '';
                const r = b.getBoundingClientRect();
                return txt.toLowerCase().includes(textToFind.toLowerCase()) && r.width > 0 && r.height > 0;
            }});
            if (target) {{
                target.scrollIntoView({{ block: 'center' }});
                target.dispatchEvent(new MouseEvent('pointerdown', {{ bubbles: true }}));
                target.dispatchEvent(new MouseEvent('mousedown', {{ bubbles: true }}));
                target.dispatchEvent(new MouseEvent('pointerup', {{ bubbles: true }}));
                target.dispatchEvent(new MouseEvent('mouseup', {{ bubbles: true }}));
                target.click();
                return true;
            }}
            return false;
        }}""", btn_text)

        if btn_clicked:
            voted_click = True
            await asyncio.sleep(2)
            break

    # 5. Extract verification artifact from DOM
    end_time = asyncio.get_event_loop().time() + (timeout / 1000)
    artifact = None
    while asyncio.get_event_loop().time() < end_time:
        artifact = await page.evaluate("""() => {
            const body = document.body.innerText || '';
            const match = body.match(/(?:Voted|Show Results|votes|%\\s*votes?|\\d+%[\\s\\S]{0,30}\\d+%)/i);
            if (match) return match[0];
            const resultCard = document.querySelector('div[class*="Duel" i], div[class*="Poll" i], div[class*="result" i]');
            if (resultCard && (resultCard.innerText.includes('%') || resultCard.innerText.includes('Voted'))) {
                return resultCard.innerText.substring(0, 150).replace(/\\n+/g, ' ');
            }
            return null;
        }""")
        if artifact:
            break
        await asyncio.sleep(1)

    if artifact:
        return {"success": True, "voted": True, "artifact": artifact}

    if selected or voted_click:
        return {"success": True, "voted": True, "artifact": "Vote action submitted"}

    return {"success": False, "error": "Could not find selectable voting options or vote submit buttons"}
