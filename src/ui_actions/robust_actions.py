# src/ui_actions/robust_actions.py

import time

def robust_query_selector(page, selector, retries=3, refresh_func=None, logger=None, desc="element", post_refresh_delay=3):
    """
    Try to find an element with retries, with optional page refresh and logging.
    Returns element handle or None.
    """
    for attempt in range(retries):
        elem = page.query_selector(selector)
        if elem:
            return elem
        msg = f"[{desc}] Attempt {attempt+1}/{retries} - not found: {selector}"
        print(msg)
        if logger:
            logger.log(msg)
        time.sleep(1.2)
    if refresh_func:
        msg = f"[{desc}] Not found after {retries} retries, refreshing page."
        print(msg)
        if logger:
            logger.log(msg)
        refresh_func()
        time.sleep(post_refresh_delay)
        elem = page.query_selector(selector)
        if elem:
            return elem
    return None
