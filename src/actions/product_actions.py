# File: src/actions/product_scraper.py
import random
import time
from datetime import datetime
import pytz
import csv
import os
from src.config import *
from src.ui_actions.human_actions import HumanActions

class ProductScraper:
    def __init__(self, page):
        self.page = page
        self.human = HumanActions(page)
        self.products_collected = []
        self.seen_cards = set()
        self.product_rank = 1

    def get_row_height(self):
        """Get height of one product card (assumes cards are in rows)"""
        first_card = self.page.query_selector(PRODUCT_CARD_SELECTOR)
        if first_card:
            return self.page.evaluate('(el) => el.offsetHeight', first_card)
        return 400  # fallback

    def scroll_one_row(self, card_height):
        """Scroll down by one row height"""
        print("[scroll_one_row] Scrolling down one row")
        self.page.evaluate(f"window.scrollBy(0, {card_height})")
        self.human.random_delay(0.6, 1.2)

    def simulate_add_remove_product(self, card):
        """
        Adds and removes a product to mimic human behavior.
        Returns max quantity reached.
        """
        add_button = card.query_selector(ADD_BUTTON_SELECTOR)
        if not add_button:
            return 0

        print("[simulate_add_remove_product] Adding random product")
        self.human.human_click(add_button)
        self.human.random_delay(0.3, 0.7)

        max_qty = 1
        while True:
            plus_button = card.query_selector(PLUS_BUTTON_SELECTOR)
            qty_elem = card.query_selector('p[data-testid="undefined-cart-qty"]')
            if not plus_button or not qty_elem:
                break

            old_qty = int(qty_elem.inner_text())
            self.human.human_click(plus_button)
            self.human.random_delay(0.2, 0.5)

            try:
                new_qty = int(qty_elem.inner_text())
                if new_qty > old_qty:
                    max_qty = new_qty
                else:
                    break
            except Exception as e:
                print(f"[simulate_add_remove_product] Error reading quantity: {e}")
                break

        minus_button = card.query_selector(MINUS_BUTTON_SELECTOR)
        if minus_button:
            print("[simulate_add_remove_product] Removing product after adding")
            self.human.human_click(minus_button)
            self.human.random_delay(0.3, 0.6)

        return max_qty

    def extract_product_info(self, card, rank=1, subcat_name="Unknown"):
        """Extract product info from card"""
        def safe_inner_text(selector):
            elem = card.query_selector(selector)
            return elem.inner_text().strip() if elem else ""

        def safe_attr(selector, attr):
            elem = card.query_selector(selector)
            return elem.get_attribute(attr).strip() if elem else ""

        name = safe_inner_text('[data-testid="product-card-name"]')
        img_url = safe_attr('[data-testid="product-card-image"]', "src")
        url = safe_attr("a", "href")
        price = safe_inner_text('p[class*="text-"]')
        mrp = safe_inner_text('p[class*="line-through"]')
        discount = safe_inner_text('p[class*="bg-"]')

        # Try to get pack/size robustly
        pack_size = ""
        units = ["ml", "g", "L", "pcs", "pack", "pieces"]
        for unit in units:
            pack_size = safe_inner_text(f'.//p[contains(text(), "{unit}")]')
            if pack_size:
                break
        if not pack_size:
            all_p = card.query_selector_all('p[class*="text-base"]')
            if all_p:
                pack_size = all_p[-1].inner_text().strip()

        # Get delivery time
        delivery_time = ""
        delivery_elem = card.query_selector('.//p[contains(@class, "-ml-1")]')
        if delivery_elem:
            delivery_time = delivery_elem.inner_text().strip()

        timestamp = datetime.now(pytz.timezone("Asia/Kolkata")).strftime("%Y-%m-%d %H:%M:%S")

        return {
            "Timestamp": timestamp,
            "Subcategory": subcat_name,
            "Rank": rank,
            "Product Name": name,
            "Product URL": f"https://www.zeptonow.com {url}" if url else "",
            "Image URL": img_url,
            "Price": price,
            "MRP": mrp,
            "Discount": discount,
            "Delivery Time": delivery_time,
            "Pack/Size": pack_size,
            "Max Quantity": self.simulate_add_remove_product(card),
        }

    def scroll_and_scrape_products(self, subcat_name="Cold Drinks"):
        """
        Scrolls one row at a time, adds a random product,
        and collects product data.
        """
        print(f"[scroll_and_scrape_products] Starting scrape for '{subcat_name}'")

        card_height = self.get_row_height()
        container = self.page.query_selector(PRODUCT_CONTAINER_SELECTOR)
        prev_count = -1
        stuck_count = 0
        MAX_STUCK = 3
        product_data_list = []

        while stuck_count < MAX_STUCK:
            cards = self.page.query_selector_all(PRODUCT_CARD_SELECTOR)
            curr_count = len(cards)

            if curr_count == prev_count:
                stuck_count += 1
                print(f"[scroll_and_scrape_products] No new products. Stuck count: {stuck_count}")
                self.recover_scroll(container, card_height)
                continue
            else:
                stuck_count = 0
                prev_count = curr_count

            # Process only newly visible cards
            for i in range(len(cards)):
                if i in self.seen_cards:
                    continue
                self.seen_cards.add(i)
                card = cards[i]

                print(f"[scroll_and_scrape_products] Processing card {i + 1}/{curr_count}")
                try:
                    product_info = self.extract_product_info(card, self.product_rank, subcat_name)
                    product_data_list.append(product_info)
                    self.product_rank += 1
                except Exception as e:
                    print(f"[scroll_and_scrape_products] Failed to extract info: {e}")

            # Randomly add product from current batch
            if cards:
                rand_idx = random.randint(0, len(cards) - 1)
                card = cards[rand_idx]
                print(f"[scroll_and_scrape_products] Simulating cart interaction on card #{rand_idx + 1}")
                self.simulate_add_remove_product(card)

            # Scroll down one row
            self.scroll_one_row(card_height)

        print(f"[scroll_and_scrape_products] Finished scraping. Collected {len(product_data_list)} products.")
        return product_data_list

    def save_to_csv(self, product_data_list, filename="products.csv"):
        """Save collected product data to CSV"""
        fieldnames = [
            "Timestamp", "Subcategory", "Rank", "Product Name", "Product URL", "Image URL",
            "Price", "MRP", "Discount", "Delivery Time", "Pack/Size", "Max Quantity"
        ]
        file_exists = os.path.isfile(filename)

        with open(filename, "a", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)

            if not file_exists:
                writer.writeheader()

            for product in product_data_list:
                writer.writerow(product)

        print(f"[save_to_csv] Saved {len(product_data_list)} products to {filename}")

    def process_all_subcategories(self, output_dir="output"):
        """Click each subcategory link and scrape its products"""
        print("[process_all_subcategories] Getting subcategory links...")
        links = self.page.query_selector_all(SUBCATEGORY_SELECTOR)

        if not links:
            print("[process_all_subcategories] No subcategories found.")
            return

        os.makedirs(output_dir, exist_ok=True)

        for idx, link in enumerate(links):
            subcat_name = link.inner_text().strip()
            safe_name = "".join([c if c.isalnum() or c in (" ", "_") else "_" for c in subcat_name[:20]])
            csv_path = os.path.join(output_dir, f"{safe_name}.csv")

            print(f"[process_all_subcategories] Processing subcategory: {subcat_name} ({idx + 1}/{len(links)})")
            self.human.human_click(link)
            self.human.random_delay(2, 3)

            try:
                self.page.wait_for_selector(PRODUCT_CARD_SELECTOR, timeout=10000)
                product_data = self.scroll_and_scrape_products(subcat_name)
                self.save_to_csv(product_data, csv_path)
                self.page.reload()
                self.human.random_delay(2, 3)
            except Exception as e:
                print(f"[process_all_subcategories] Failed to load products for '{subcat_name}': {e}")
                continue

        print("[process_all_subcategories] All subcategories processed.")

    def recover_scroll(self, container, card_height):
        """Try to recover lazy loading by scrolling up/down"""
        print("[recover_scroll] Recovering scroll...")
        self.page.evaluate(f"window.scrollBy(0, -{card_height})")
        self.human.random_delay(0.6, 1.2)
        self.page.evaluate(f"window.scrollBy(0, {card_height * 2})")
        self.human.random_delay(0.6, 1.2)

    def scroll_one_row(self, card_height):
        """Scroll one row down"""
        self.page.evaluate(f"window.scrollBy(0, {card_height})")
        self.human.random_delay(0.5, 1.0)

    def scroll_to_load_all_products(self, max_retries=6):
        """
        Scrolls down until no new products appear.
        Uses robust_query_selector to find elements.
        """
        prev_count = -1
        stuck_retries = 0
        up_down_cycles = 0
        MAX_STUCK = 3
        MAX_UP_DOWN_CYCLES = 2

        while stuck_retries < max_retries:
            cards = self.page.query_selector_all(PRODUCT_CARD_SELECTOR)
            curr_count = len(cards)

            if curr_count == prev_count:
                stuck_retries += 1
                print(f"[Scroll] No new products loaded. Stuck count: {stuck_retries}")
                if up_down_cycles < MAX_UP_DOWN_CYCLES:
                    self.recover_scroll(card_height)
                    up_down_cycles += 1
                else:
                    logger.log("[Scroll] Reached max up-down cycles. Refreshing page.")
                    self.page.reload()
                    time.sleep(3)
                    up_down_cycles = 0
            else:
                stuck_retries = 0
                prev_count = curr_count

            # Scroll down one row
            self.page.evaluate(f"window.scrollBy(0, {card_height})")
            self.human.random_delay(0.5, 1.0)

    