from src.config import CATEGORY_CARD_SELECTOR, CATEGORY_SCROLL_RIGHT_SELECTOR, SUBCATEGORY_LINK_SELECTOR
import random 
import time

class NavigationActions:
    def __init__(self, page):
        self.page = page

    # def scroll_right_n_times(self, n=1):
    #     for i in range(n):
    #         self.page.wait_for_selector(CATEGORY_SCROLL_RIGHT_SELECTOR, timeout=5000)
    #         self.page.click(CATEGORY_SCROLL_RIGHT_SELECTOR)
    #         self.page.wait_for_timeout(500)  # Small pause for animation

    def click_category_by_href(self, partial_href):
        self.page.wait_for_selector(CATEGORY_CARD_SELECTOR, timeout=10000)
        links = self.page.query_selector_all(CATEGORY_CARD_SELECTOR)
        for link in links:
            href = link.get_attribute('href')
            if href and partial_href in href:
                link.scroll_into_view_if_needed()
                link.hover()                              # Human-like behavior
                self.page.wait_for_timeout(random.randint(150, 350))
                link.click()
                # print(f"Clicked category with href: {href}")
                return True
        # print(f"Category with href containing '{partial_href}' not found.")
        return False
    


    def click_subcategory_by_name(self, name="Top Picks"):
        self.page.wait_for_selector(SUBCATEGORY_LINK_SELECTOR, timeout=10000)
        links = self.page.query_selector_all(SUBCATEGORY_LINK_SELECTOR)
        for link in links:
            p_tag = link.query_selector('p')
            if p_tag and name.lower() in p_tag.inner_text().strip().lower():
                link.scroll_into_view_if_needed()
                link.hover()
                self.page.wait_for_timeout(random.randint(150, 350))
                link.click()
                print(f"Clicked subcategory: {name}")
                return True
        print(f"Subcategory '{name}' not found.")
        return False

    def iterate_all_subcategories(self, callback=None):
        self.page.wait_for_selector(SUBCATEGORY_LINK_SELECTOR, timeout=10000)
        links = self.page.query_selector_all(SUBCATEGORY_LINK_SELECTOR)
        for link in links:
            p_tag = link.query_selector('p')
            name = p_tag.inner_text().strip() if p_tag else "Unknown"
            link.scroll_into_view_if_needed()
            link.hover()
            self.page.wait_for_timeout(random.randint(100, 350))
            link.click()
            print(f"Clicked subcategory: {name}")
            # Optional: do something on each subcategory (scrape data, etc)
            if callback:
                callback(name)
            # Optionally, re-query links if page reloads or changes
            self.page.wait_for_timeout(1000)
    def list_subcategories(self):
        """Returns a list of (index, name, element) for all subcategories."""
        self.page.wait_for_selector(SUBCATEGORY_LINK_SELECTOR, timeout=10000)
        links = self.page.query_selector_all(SUBCATEGORY_LINK_SELECTOR)
        subcategories = []
        for i, link in enumerate(links):
            p_tag = link.query_selector('p')
            name = p_tag.inner_text().strip() if p_tag else f"Subcategory {i+1}"
            subcategories.append((i, name, link))
        return subcategories

    def choose_subcategory_by_index(self, index):
        subcategories = self.list_subcategories()
        if 0 <= index < len(subcategories):
            _, name, link = subcategories[index]
            link.scroll_into_view_if_needed()
            link.hover()
            self.page.wait_for_timeout(200)
            link.click()
            print(f"Clicked subcategory: {name}")
        else:
            print("Invalid index!")
    def scroll_right_n_times(self, n=2, timeout=15000):
        """
        Scroll the right-arrow button 'n' times, waiting for its presence each time.
        """
        for i in range(n):
            try:
                self.page.wait_for_selector(CATEGORY_SCROLL_RIGHT_SELECTOR, timeout=timeout)
                scroll_btn = self.page.query_selector(CATEGORY_SCROLL_RIGHT_SELECTOR)
                if scroll_btn:
                    print(f"Attempting to click right scroll button ({i+1}/{n})")
                    scroll_btn.click()
                    time.sleep(random.uniform(0.3, 0.7))  # human-like delay
                else:
                    print("Scroll right button not found.")
                    break
            except Exception as e:
                print(f"Error clicking scroll right button: {e}")
                break

