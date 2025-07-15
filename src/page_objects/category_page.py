# from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeoutError
# import random
# import time
# from src.ui_actions.human_actions import HumanActions

# # CSS/XPath Selectors for scrolling buttons
# FULL_RIGHT_SCROLL_SELECTOR = (
#     '//div[contains(@class, "absolute") and contains(@class, "right-5") and '
#     'contains(@class, "top-1/2") and contains(@class, "z-10") and contains(@class, "-translate-y-1/2")]'
#     '/button[contains(@class, "-rotate-180")]'
# )

# FULL_LEFT_SCROLL_SELECTOR = (
#     "div.absolute.left-5.top-1\\/2.-translate-y-1\\/2 > button"
# )


# class CategoryPage:
#     def __init__(self, page):
#         self.page = page

#     def robust_click(self, selector, label="button", timeout_sec=7):
#         """
#         Try to click an element robustly with retries and error handling.
#         Returns True if successful, False otherwise.
#         """
#         start_time = time.time()
#         while time.time() - start_time < timeout_sec:
#             try:
#                 # Wait for the element to be visible
#                 self.page.wait_for_selector(selector, timeout=timeout_sec * 1000, state="visible")
#                 element = self.page.query_selector(selector)
#                 if element:
#                     print(f"[robust_click] {label} found. Attempting to click.")
#                     element.scroll_into_view_if_needed()
#                     element.hover()
#                     element.click()
#                     print(f"[robust_click] Successfully clicked '{label}'")
#                     return True
#                 else:
#                     print(f"[robust_click] {label} NOT found after waiting.")
#             except PlaywrightTimeoutError:
#                 print(f"[robust_click] Timeout waiting for selector '{selector}'")
#             except Exception as e:
#                 print(f"[robust_click] Error clicking '{label}': {e}")

#             time.sleep(1)  # Small delay before retry

#         print(f"[robust_click] Failed to click '{label}' within {timeout_sec} seconds.")
#         return False

#     def humanized_carousel_scroll(self, net_right=2, max_extra=4):
#         """
#         Scrolls right exactly `net_right` times in total.
#         - First, always scrolls right `net_right` times.
#         - Then performs a mix of random left/right scrolls,
#           but ensures the final net right scroll is exactly `net_right`.
#         """
#         print(f"[humanized_carousel_scroll] Starting with net_right={net_right}, max_extra={max_extra}")

#         # Step 1: Initial Right Scrolls
#         for i in range(net_right):
#             print(f"[humanized_carousel_scroll] Initial right scroll {i + 1}/{net_right}")
#             success = self.robust_click(FULL_RIGHT_SCROLL_SELECTOR, "Right Scroll Button")
#             if not success:
#                 print("[humanized_carousel_scroll] Failed initial right scroll.")
#                 raise RuntimeError("Failed to perform required initial right scroll.")

#         # Step 2: Random Left/Right Mix (Net Scroll Must Stay at net_right)
#         extra_moves = random.randint(1, max_extra)
#         right_moves = random.randint(0, extra_moves)
#         left_moves = extra_moves - right_moves
#         moves = ["right"] * right_moves + ["left"] * left_moves
#         random.shuffle(moves)
#         print(f"[humanized_carousel_scroll] Extra moves: {moves}")

#         for move in moves:
#             direction = move.lower()
#             selector = FULL_RIGHT_SCROLL_SELECTOR if direction == "right" else FULL_LEFT_SCROLL_SELECTOR
#             print(f"[humanized_carousel_scroll] Performing {direction} scroll")
#             success = self.robust_click(selector, f"{direction.capitalize()} Scroll Button")
#             if not success:
#                 print(f"[humanized_carousel_scroll] Warning: {direction.capitalize()} scroll failed, continuing...")

#         print("[humanized_carousel_scroll] Scroll sequence complete.")
    
#     # File: src/page_objects/category_page.py

#     def select_category_by_href(self, href, timeout_sec=15):
#         """
#         Find and click a category <a> tag with humanized mouse actions.
#         """
#         print(f"[select_category_by_href] Looking for category with href='{href}'")

#         try:
#             # Wait for carousel container to load
#             self.page.wait_for_selector("section.embla .embla__container", timeout=timeout_sec * 1000)

#             # Build selector for anchor with exact href
#             selector = f"a[href='{href}']"

#             # Wait for the link to be visible
#             self.page.wait_for_selector(selector, timeout=timeout_sec * 1000, state="visible")

#             print(f"[select_category_by_href] Found category with href='{href}'. Clicking...")
#             element = self.page.query_selector(selector)

#             if not element:
#                 raise RuntimeError(f"Element not found for href='{href}'")

#             # Create HumanActions instance and click
#             human_actions = HumanActions(self.page)
#             human_actions.human_fidget_mouse(chance=0.3)
#             human_actions.human_click(element)

#             print(f"[select_category_by_href] Successfully clicked category with href='{href}'")
#         except PlaywrightTimeoutError as e:
#             print(f"[select_category_by_href] Timeout: Could not find category with href='{href}' - {e}")
#             raise
#         except Exception as e:
#             print(f"[select_category_by_href] Unexpected error: {e}")
#             raise

#     def click_category_image_by_src(self, img_src_keyword, timeout_sec=15):
#         """
#         Scrolls carousel, finds <img> tag containing the given src keyword,
#         and clicks it using human-like actions.
#         """
#         print(f"[click_category_image_by_src] Looking for image with src containing='{img_src_keyword}'")

#         try:
#             # Wait for carousel container
#             self.page.wait_for_selector("section.embla .embla__container", timeout=timeout_sec * 1000)

#             # Get all images inside carousel slides
#             images = self.page.query_selector_all("section.embla .embla__slide img")

#             if not images:
#                 raise RuntimeError("No images found in carousel")

#             print(f"[click_category_image_by_src] Found {len(images)} images. Matching src...")

#             for img in images:
#                 src = img.get_attribute("src")
#                 if src and img_src_keyword in src:
#                     print(f"[click_category_image_by_src] Found matching image: '{src}'. Clicking...")
#                     human_actions = HumanActions(self.page)
#                     human_actions.human_click(img)
#                     return True

#             raise RuntimeError(f"No image found with src containing '{img_src_keyword}'")

#         except PlaywrightTimeoutError as e:
#             print(f"[click_category_image_by_src] Timeout: {e}")
#             raise
#         except Exception as e:
#             print(f"[click_category_image_by_src] Error: {e}")
#             raise

# File: src/page_objects/category_page.py

import time
import random
from playwright.sync_api import TimeoutError as PlaywrightTimeoutError
from src.ui_actions.human_actions import HumanActions
CATEGORY_SCROLL_RIGHT_SELECTOR = "div.absolute.right-5.top-1\\/2.-translate-y-1\\/2 > button.-rotate-180"
CATEGORY_SCROLL_LEFT_SELECTOR = "div.absolute.left-5.top-1\\/2.-translate-y-1\\/2 > button"


class CategoryPage:
    def __init__(self, page):
        self.page = page

    @staticmethod
    def robust_click(page, selector, label="button", timeout_sec=10, reload_on_fail=False):
        """
        Try to click a button robustly. Only reload if requested (and only once).
        """
        start = time.time()
        tried_reload = False

        while time.time() - start < timeout_sec:
            try:
                # Wait for the selector to be visible
                page.wait_for_selector(selector, timeout=timeout_sec * 1000, state="visible")
                btn = page.query_selector(selector)

                if btn:
                    print(f"[robust_click] {label} found for selector '{selector}'")
                    try:
                        btn.scroll_into_view_if_needed()
                        btn.hover()
                        btn.click()
                        print(f"[robust_click] Clicked {label}")
                        return True
                    except PlaywrightTimeoutError as e:
                        print(f"[robust_click] Timeout during click action: {e}")
                        if reload_on_fail and not tried_reload:
                            print("[robust_click] Reloading due to timeout during click...")
                            page.reload()
                            time.sleep(2)
                            tried_reload = True
                            continue
                    except Exception as e:
                        print(f"[robust_click] Exception during click: {e}")
                        if reload_on_fail and not tried_reload:
                            print("[robust_click] Trying page reload due to click exception...")
                            page.reload()
                            time.sleep(2)
                            tried_reload = True
                            continue
                else:
                    print(f"[robust_click] {label} NOT found for selector '{selector}'")

            except PlaywrightTimeoutError:
                print(f"[robust_click] Timeout waiting for selector '{selector}'")
                if reload_on_fail and not tried_reload:
                    print("[robust_click] Trying page reload due to wait timeout...")
                    page.reload()
                    time.sleep(2)
                    tried_reload = True
                    continue
            except Exception as e:
                print(f"[robust_click] Unexpected exception: {e}")
                if reload_on_fail and not tried_reload:
                    print("[robust_click] Trying page reload due to unknown exception...")
                    page.reload()
                    time.sleep(2)
                    tried_reload = True
                    continue

            time.sleep(0.5)

        print(f"[robust_click] Timeout: Failed to click {label} within {timeout_sec} seconds.")
        return False

    def humanized_carousel_scroll(self, net_right=2):
        """
        Scrolls right `net_right` times, then scrolls left `(net_right - 2)` times.
        Ensures final net scroll is always exactly 2 to the right.
        """
        print(f"[humanized_carousel_scroll] Starting with net_right={net_right}")

        # Step 1: Scroll right `net_right` times
        for i in range(net_right):
            print(f"[humanized_carousel_scroll] Right scroll {i + 1}/{net_right}")
            success = self.robust_click(
                self.page,
                CATEGORY_SCROLL_RIGHT_SELECTOR,
                label="Right Scroll Button",
                reload_on_fail=True
            )
            if not success:
                raise RuntimeError("Failed to complete required right scrolls.")

            time.sleep(random.uniform(0.7, 1.5))  # Human-like delay

        # Step 2: Scroll left `(net_right - 2)` times
        left_scrolls_needed = max(0, net_right - 2)
        print(f"[humanized_carousel_scroll] Now performing {left_scrolls_needed} left scroll(s)")

        for i in range(left_scrolls_needed):
            print(f"[humanized_carousel_scroll] Left scroll {i + 1}/{left_scrolls_needed}")
            success = self.robust_click(
                self.page,
                CATEGORY_SCROLL_LEFT_SELECTOR,
                label="Left Scroll Button",
                reload_on_fail=True
            )
            if not success:
                print("[humanized_carousel_scroll] Warning: Left scroll failed, continuing...")

            time.sleep(random.uniform(0.5, 1.2))  # Human-like delay

        print("[humanized_carousel_scroll] Scroll sequence complete.")

    def select_category_by_href(self, href, timeout_sec=15):
        """
        Find and click a category <a> tag with humanized mouse actions.
        """
        print(f"[select_category_by_href] Looking for category with href='{href}'")

        try:
            # Wait for carousel container to load
            self.page.wait_for_selector("section.embla .embla__container", timeout=timeout_sec * 1000)

            # Build selector for anchor with exact href
            selector = f"a[href='{href}']"

            # Wait for the link to be visible
            self.page.wait_for_selector(selector, timeout=timeout_sec * 1000, state="visible")

            print(f"[select_category_by_href] Found category with href='{href}'. Clicking...")
            element = self.page.query_selector(selector)

            if not element:
                raise RuntimeError(f"Element not found for href='{href}'")

            # Create HumanActions instance and click
            human_actions = HumanActions(self.page)
            human_actions.human_fidget_mouse(chance=0.3)
            human_actions.human_click(element)

            print(f"[select_category_by_href] Successfully clicked category with href='{href}'")
        except PlaywrightTimeoutError as e:
            print(f"[select_category_by_href] Timeout: Could not find category with href='{href}' - {e}")
            raise
        except Exception as e:
            print(f"[select_category_by_href] Unexpected error: {e}")
            raise

    # File: src/page_objects/category_page.py

    # File: src/page_objects/category_page.py

    def click_link_by_exact_href(self, target_href, timeout_sec=15):
        """
        Searches all <a> tags for an exact href match and clicks the element.
        Uses robust_click for retry logic and optional reloads.
        """
        print(f"[click_link_by_exact_href] Looking for link with href='{target_href}'")

        try:
            # Wait for page to load enough to find links
            self.page.wait_for_timeout(timeout_sec * 1000)

            # Get all anchor tags
            anchors = self.page.query_selector_all("a")

            if not anchors:
                raise RuntimeError("No <a> tags found on the page.")

            print(f"[click_link_by_exact_href] Found {len(anchors)} <a> tags. Searching for href match...")

            for anchor in anchors:
                href = anchor.get_attribute("href")
                if href == target_href:
                    print(f"[click_link_by_exact_href] Matched href: '{href}'. Clicking...")
                    
                    # Use robust_click properly: pass page + selector string
                    selector = f"a[href='{href}']"
                    return self.robust_click(self.page, selector, label=f"Link '{href}'", reload_on_fail=True)

            raise RuntimeError(f"No link found with exact href='{target_href}'")

        except Exception as e:
            print(f"[click_link_by_exact_href] Error: {e}")
            raise