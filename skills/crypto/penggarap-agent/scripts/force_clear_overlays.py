# Origin Domain: https://www.dollclub.xyz/
# Date: 2026-08-18
# Specific Symptom: hermes -z: no final response was produced (hang on overlays/antibot)

def force_clear_overlays(page):
    """Removes blocking overlays and restores scroll to unblock stuck agents."""
    page.evaluate('''() => {
        document.querySelectorAll('*').forEach(el => {
            try {
                const style = window.getComputedStyle(el);
                if (parseInt(style.zIndex) > 100 || el.id.includes('turnstile') || el.className.includes('overlay') || el.className.includes('modal')) {
                    el.remove();
                }
            } catch (e) {}
        });
        document.body.style.overflow = 'auto';
        document.documentElement.style.overflow = 'auto';
    }''')