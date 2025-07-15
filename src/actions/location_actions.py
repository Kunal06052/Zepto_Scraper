import time
from src.config import *

class Action:
    def __init__(self, page):
        self.page = page

    def set_location(self, location):
        # Click location button in top bar
        print("Clicking 'Select Location' button...")
        self.page.wait_for_selector(LOCATION_BUTTON_SELECTOR, timeout=15000)
        self.page.click(LOCATION_BUTTON_SELECTOR)
        # Wait for input field in popup
        print("Waiting for location input field...")
        self.page.wait_for_selector(LOCATION_INPUT_SELECTOR, timeout=15000)
        # Type city (character by character, slower for realism)
        print(f"Typing city: {location}")
        self.page.fill(LOCATION_INPUT_SELECTOR, "")  # Clear
        for ch in location:
            self.page.type(LOCATION_INPUT_SELECTOR, ch)
            time.sleep(0.1)
        # Wait and click first dropdown result
        print("Waiting for first dropdown result...")
        self.page.wait_for_selector(LOCATION_RESULT_SELECTOR, timeout=10000)
        self.page.click(LOCATION_RESULT_SELECTOR)
        # Click "Confirm & Continue"
        print("Waiting for Confirm button...")
        self.page.wait_for_selector(LOCATION_CONFIRM_SELECTOR, timeout=10000)
        self.page.click(LOCATION_CONFIRM_SELECTOR)
        print("Location set!")




