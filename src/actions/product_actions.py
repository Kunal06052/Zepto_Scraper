# # # # import csv
# # # # import os
# # # # from src.config import PRODUCT_CARD_SELECTOR
# # # # from src.ui_actions.human_actions import HumanActions
# # # # from datetime import datetime
# # # # import pytz
# # # # import time 
# # # # from src.ui_actions.robust_actions import robust_query_selector
# # # # from src.utils.error_logger import ErrorLogger

# # # # logger = ErrorLogger("src/data/errors.log")

# # # # class ProductActions:
# # # #     def __init__(self, page):
# # # #         self.page = page
# # # #         self.human = HumanActions(page)
    
# # # #     def scroll_to_load_all_products(self, max_retries=6):
# # # #         """
# # # #         Scrolls down by the height of a product card, attempting to load all products.
# # # #         If products stop loading, scrolls up and down a few times to "unstick" lazy loading.
# # # #         Uses robust element lookup and logs errors.
# # # #         """
# # # #         prev_count = -1
# # # #         stuck_retries = 0
# # # #         up_down_cycles = 0

# # # #         # Use robust_query_selector for first card
# # # #         try:
# # # #             first_card = robust_query_selector(
# # # #                 self.page,
# # # #                 PRODUCT_CARD_SELECTOR,
# # # #                 retries=3,
# # # #                 refresh_func=lambda: self.page.reload(),
# # # #                 logger=logger,
# # # #                 desc="Product card"
# # # #             )
# # # #             card_height = self.page.evaluate("(el) => el.offsetHeight", first_card) if first_card else 400
# # # #         except Exception:
# # # #             card_height = 400

# # # #         while stuck_retries < max_retries:
# # # #             cards = self.page.query_selector_all(PRODUCT_CARD_SELECTOR)
# # # #             curr_count = len(cards)
# # # #             if curr_count == prev_count:
# # # #                 stuck_retries += 1

# # # #                 # Try scrolling up, then down, then refresh if really stuck
# # # #                 if up_down_cycles < 2:
# # # #                     logger.log(f"[Scroll] No new products, scrolling up and down. Attempt {up_down_cycles+1}")
# # # #                     self.page.evaluate(f"window.scrollBy(0, -{card_height * 8});")
# # # #                     self.human.human_sleep(0.7, 1.2)
# # # #                     self.page.evaluate(f"window.scrollBy(0, {card_height * 8});")
# # # #                     self.human.human_sleep(0.7, 1.2)
# # # #                     up_down_cycles += 1
# # # #                 else:
# # # #                     logger.log("[Scroll] No new products loaded after retries, stopping.")
# # # #                     break
# # # #             else:
# # # #                 stuck_retries = 0
# # # #                 up_down_cycles = 0  # Reset up/down cycle
# # # #                 prev_count = curr_count
# # # #                 self.page.evaluate(f"window.scrollBy(0, {card_height});")
# # # #                 self.human.human_sleep(0.5, 1.1)

# # # #         logger.log(f"Total loaded product cards: {prev_count}")
# # # #         return self.page.query_selector_all(PRODUCT_CARD_SELECTOR)

# # # #     def extract_product_info(self, card, rank):
# # # #         def safe_inner_text_css(selector):
# # # #             elem = card.query_selector(selector)
# # # #             return elem.inner_text().strip() if elem else ""

# # # #         def safe_inner_text_xpath(xpath):
# # # #             elem = card.query_selector(f'xpath={xpath}')
# # # #             return elem.inner_text().strip() if elem else ""

# # # #         def safe_attr(selector, attr):
# # # #             elem = card.query_selector(selector)
# # # #             return elem.get_attribute(attr) if elem else ""

# # # #         url = card.get_attribute('href') or ""
# # # #         name = safe_inner_text_css('[data-testid="product-card-name"]')
# # # #         img_url = safe_attr('[data-testid="product-card-image"]', 'src')
# # # #         price = safe_inner_text_css('p[class*="text-"]')
# # # #         mrp = safe_inner_text_css('p[class*="line-through"]')
# # # #         discount = safe_inner_text_css('p[class*="bg-"]')
# # # #         rating = safe_inner_text_xpath('.//p[contains(@class, "font-[500]")]')
# # # #         rating_count = safe_inner_text_xpath('.//p[contains(@class, "font-[400]")]')
# # # #         delivery_time = safe_inner_text_xpath('.//p[contains(@class, "-ml-1")]')

# # # #         # Pack/Size robust search
# # # #         units = ["ml", "g", "L", "pcs", "pack", "pieces", "Pack", "Pieces"]
# # # #         packsize = ""
# # # #         for unit in units:
# # # #             packsize = safe_inner_text_xpath(f'.//p[contains(@class, "text-base") and contains(text(), "{unit}")]')
# # # #             if packsize:
# # # #                 break
# # # #         if not packsize:
# # # #             all_p = card.query_selector_all('xpath=.//p[contains(@class, "text-base")]')
# # # #             if all_p:
# # # #                 packsize = all_p[-1].inner_text().strip()

# # # #         return {
# # # #             "Rank": rank,
# # # #             "Product Name": name,
# # # #             "Product URL": "https://www.zeptonow.com" + url,
# # # #             "Image URL": img_url,
# # # #             "Price": price,
# # # #             "MRP": mrp,
# # # #             "Discount": discount,
# # # #             "Rating": rating,
# # # #             "Rating Count": rating_count,
# # # #             "Delivery Time": delivery_time,
# # # #             "Pack/Size": packsize,
# # # #         }

# # # #     def add_and_max_quantity(self, card):
# # # #         """Click 'ADD' and then '+' until quantity doesn't increase, then remove all. Uses robust_query_selector."""
# # # #         add_button = robust_query_selector(
# # # #             card,
# # # #             'button[aria-label="add"]',
# # # #             retries=3,
# # # #             refresh_func=None,
# # # #             logger=logger,
# # # #             desc="Add button"
# # # #         )
# # # #         if not add_button:
# # # #             logger.log("Add button not found after retries.")
# # # #             return 0
# # # #         self.human.human_click(add_button)
# # # #         self.human.human_sleep(0.3, 0.6)
# # # #         max_qty = 1
# # # #         while True:
# # # #             plus_btn = card.query_selector('button[aria-label="Add"][data-testid="undefined-plus-btn"]')
# # # #             qty_elem = card.query_selector('p[data-testid="undefined-cart-qty"]')
# # # #             if not plus_btn or not qty_elem:
# # # #                 break
# # # #             try:
# # # #                 last_qty = int(qty_elem.inner_text().strip())
# # # #             except Exception:
# # # #                 last_qty = max_qty
# # # #             self.human.human_click(plus_btn)
# # # #             self.human.human_sleep(0.3, 0.5)
# # # #             qty_elem = card.query_selector('p[data-testid="undefined-cart-qty"]')
# # # #             try:
# # # #                 new_qty = int(qty_elem.inner_text().strip()) if qty_elem else last_qty
# # # #             except Exception:
# # # #                 new_qty = last_qty
# # # #             if new_qty == last_qty:
# # # #                 break
# # # #             max_qty = new_qty
# # # #         # Remove until ADD button reappears
# # # #         while not card.query_selector('button[aria-label="add"]'):
# # # #             minus_btn = card.query_selector('button[aria-label="Remove"][data-testid="undefined-minus-btn"]')
# # # #             if not minus_btn:
# # # #                 break
# # # #             self.human.human_click(minus_btn)
# # # #             self.human.human_sleep(0.2, 0.4)
# # # #         return max_qty

# # # #     def process_all_products(self, save_csv=True, filename="products.csv"):
# # # #         # Use infinite scroll to load all
# # # #         india = pytz.timezone("Asia/Kolkata")
# # # #         now_ist = datetime.now(india)
# # # #         fetch_time = now_ist.strftime("%H:%M:%S")
# # # #         fetch_date = now_ist.strftime("%Y-%m-%d")
# # # #         cards = self.scroll_to_load_all_products()
# # # #         product_list = []
# # # #         for idx, card in enumerate(cards, 1):
# # # #             data = self.extract_product_info(card, idx)
# # # #             self.human.human_sleep(0.3, 0.7)
# # # #             try:
# # # #                 max_qty = self.add_and_max_quantity(card)
# # # #             except Exception as e:
# # # #                 logger.log(f"ERROR: Could not add/check quantity for product {idx}: {e}")
# # # #                 max_qty = ""
# # # #             data["Max Quantity"] = max_qty
# # # #             data["Fetched Date"] = fetch_date
# # # #             data["Fetched Time"] = fetch_time
# # # #             product_list.append(data)
# # # #         if save_csv and product_list:
# # # #             self.save_products_to_csv(product_list, filename)
# # # #             print(f"Saved {len(product_list)} products to {filename}.")
# # # #         else:
# # # #             for prod in product_list:
# # # #                 print(prod)

# # # #     def save_products_to_csv(self, products, filename="products.csv"):
# # # #         if not products:
# # # #             print("No products found to save. CSV not created.")
# # # #             return
# # # #         fieldnames = products[0].keys()
# # # #         with open(filename, "w", newline="", encoding="utf-8") as csvfile:
# # # #             writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
# # # #             writer.writeheader()
# # # #             for prod in products:
# # # #                 writer.writerow(prod)
# # # #         print(f"CSV file '{filename}' created successfully with {len(products)} products.")

# # # import csv
# # # import os
# # # from src.config import PRODUCT_CARD_SELECTOR
# # # from src.ui_actions.human_actions import HumanActions
# # # from datetime import datetime
# # # import pytz
# # # import time 
# # # from src.ui_actions.robust_actions import robust_query_selector
# # # from src.utils.error_logger import ErrorLogger

# # # logger = ErrorLogger("src/data/errors.log")

# # # class ProductActions:
# # #     def __init__(self, page):
# # #         self.page = page
# # #         self.human = HumanActions(page)
    
# # #     def scroll_to_load_all_products(self, max_retries=6):
# # #         """
# # #         Scrolls down by the height of a product card, attempting to load all products.
# # #         If products stop loading, scrolls up and down a few times to "unstick" lazy loading.
# # #         Uses robust element lookup and logs errors.
# # #         """
# # #         prev_count = -1
# # #         stuck_retries = 0
# # #         up_down_cycles = 0

# # #         # Use robust_query_selector for first card
# # #         try:
# # #             first_card = robust_query_selector(
# # #                 self.page,
# # #                 PRODUCT_CARD_SELECTOR,
# # #                 retries=3,
# # #                 refresh_func=lambda: self.page.reload(),
# # #                 logger=logger,
# # #                 desc="Product card"
# # #             )
# # #             card_height = self.page.evaluate("(el) => el.offsetHeight", first_card) if first_card else 400
# # #         except Exception:
# # #             card_height = 400

# # #         while stuck_retries < max_retries:
# # #             cards = self.page.query_selector_all(PRODUCT_CARD_SELECTOR)
# # #             curr_count = len(cards)
# # #             if curr_count == prev_count:
# # #                 stuck_retries += 1

# # #                 # Try scrolling up, then down, then refresh if really stuck
# # #                 if up_down_cycles < 2:
# # #                     logger.log(f"[Scroll] No new products, scrolling up and down. Attempt {up_down_cycles+1}")
# # #                     self.page.evaluate(f"window.scrollBy(0, -{card_height * 8});")
# # #                     self.human.human_sleep(0.7, 1.2)
# # #                     self.page.evaluate(f"window.scrollBy(0, {card_height * 8});")
# # #                     self.human.human_sleep(0.7, 1.2)
# # #                     up_down_cycles += 1
# # #                 else:
# # #                     logger.log("[Scroll] No new products loaded after retries, stopping.")
# # #                     break
# # #             else:
# # #                 stuck_retries = 0
# # #                 up_down_cycles = 0  # Reset up/down cycle
# # #                 prev_count = curr_count
# # #                 self.page.evaluate(f"window.scrollBy(0, {card_height});")
# # #                 self.human.human_sleep(0.5, 1.1)

# # #         logger.log(f"Total loaded product cards: {prev_count}")
# # #         return self.page.query_selector_all(PRODUCT_CARD_SELECTOR)

# # #     def extract_product_info(self, card, rank):
# # #         def safe_inner_text_css(selector):
# # #             elem = card.query_selector(selector)
# # #             return elem.inner_text().strip() if elem else ""

# # #         def safe_inner_text_xpath(xpath):
# # #             elem = card.query_selector(f'xpath={xpath}')
# # #             return elem.inner_text().strip() if elem else ""

# # #         def safe_attr(selector, attr):
# # #             elem = card.query_selector(selector)
# # #             return elem.get_attribute(attr) if elem else ""

# # #         url = card.get_attribute('href') or ""
# # #         name = safe_inner_text_css('[data-testid="product-card-name"]')
# # #         img_url = safe_attr('[data-testid="product-card-image"]', 'src')
# # #         price = safe_inner_text_css('p[class*="text-"]')
# # #         mrp = safe_inner_text_css('p[class*="line-through"]')
# # #         discount = safe_inner_text_css('p[class*="bg-"]')
# # #         rating = safe_inner_text_xpath('.//p[contains(@class, "font-[500]")]')
# # #         rating_count = safe_inner_text_xpath('.//p[contains(@class, "font-[400]")]')
# # #         delivery_time = safe_inner_text_xpath('.//p[contains(@class, "-ml-1")]')

# # #         # Pack/Size robust search
# # #         units = ["ml", "g", "L", "pcs", "pack", "pieces", "Pack", "Pieces"]
# # #         packsize = ""
# # #         for unit in units:
# # #             packsize = safe_inner_text_xpath(f'.//p[contains(@class, "text-base") and contains(text(), "{unit}")]')
# # #             if packsize:
# # #                 break
# # #         if not packsize:
# # #             all_p = card.query_selector_all('xpath=.//p[contains(@class, "text-base")]')
# # #             if all_p:
# # #                 packsize = all_p[-1].inner_text().strip()

# # #         return {
# # #             "Rank": rank,
# # #             "Product Name": name,
# # #             "Product URL": "https://www.zeptonow.com" + url,
# # #             "Image URL": img_url,
# # #             "Price": price,
# # #             "MRP": mrp,
# # #             "Discount": discount,
# # #             "Rating": rating,
# # #             "Rating Count": rating_count,
# # #             "Delivery Time": delivery_time,
# # #             "Pack/Size": packsize,
# # #         }

# # #     def add_and_max_quantity(self, card):
# # #         """Click 'ADD' and then '+' until quantity doesn't increase, then remove all. Uses robust_query_selector."""
# # #         add_button = robust_query_selector(
# # #             card,
# # #             'button[aria-label="add"]',
# # #             retries=3,
# # #             refresh_func=None,
# # #             logger=logger,
# # #             desc="Add button"
# # #         )
# # #         if not add_button:
# # #             logger.log("Add button not found after retries.")
# # #             return 0
# # #         self.human.human_click(add_button)
# # #         self.human.human_sleep(0.3, 0.6)
# # #         max_qty = 1
# # #         while True:
# # #             plus_btn = card.query_selector('button[aria-label="Add"][data-testid="undefined-plus-btn"]')
# # #             qty_elem = card.query_selector('p[data-testid="undefined-cart-qty"]')
# # #             if not plus_btn or not qty_elem:
# # #                 break
# # #             try:
# # #                 last_qty = int(qty_elem.inner_text().strip())
# # #             except Exception:
# # #                 last_qty = max_qty
# # #             self.human.human_click(plus_btn)
# # #             self.human.human_sleep(0.3, 0.5)
# # #             qty_elem = card.query_selector('p[data-testid="undefined-cart-qty"]')
# # #             try:
# # #                 new_qty = int(qty_elem.inner_text().strip()) if qty_elem else last_qty
# # #             except Exception:
# # #                 new_qty = last_qty
# # #             if new_qty == last_qty:
# # #                 break
# # #             max_qty = new_qty
# # #         # Remove until ADD button reappears
# # #         while not card.query_selector('button[aria-label="add"]'):
# # #             minus_btn = card.query_selector('button[aria-label="Remove"][data-testid="undefined-minus-btn"]')
# # #             if not minus_btn:
# # #                 break
# # #             self.human.human_click(minus_btn)
# # #             self.human.human_sleep(0.2, 0.4)
# # #         return max_qty

# # #     def process_all_products(self, save_csv=True, filename="products.csv"):
# # #         # Use infinite scroll to load all
# # #         india = pytz.timezone("Asia/Kolkata")
# # #         now_ist = datetime.now(india)
# # #         fetch_time = now_ist.strftime("%H:%M:%S")
# # #         fetch_date = now_ist.strftime("%Y-%m-%d")
# # #         cards = self.scroll_to_load_all_products()
# # #         product_list = []
# # #         for idx, card in enumerate(cards, 1):
# # #             data = self.extract_product_info(card, idx)
# # #             self.human.human_sleep(0.3, 0.7)
# # #             try:
# # #                 max_qty = self.add_and_max_quantity(card)
# # #             except Exception as e:
# # #                 logger.log(f"ERROR: Could not add/check quantity for product {idx}: {e}")
# # #                 max_qty = ""
# # #             data["Max Quantity"] = max_qty
# # #             data["Fetched Date"] = fetch_date
# # #             data["Fetched Time"] = fetch_time
# # #             product_list.append(data)
# # #         if save_csv and product_list:
# # #             self.save_products_to_csv(product_list, filename)
# # #             print(f"Saved {len(product_list)} products to {filename}.")
# # #         else:
# # #             for prod in product_list:
# # #                 print(prod)

# # #     def save_products_to_csv(self, products, filename="products.csv"):
# # #         if not products:
# # #             print("No products found to save. CSV not created.")
# # #             return
# # #         fieldnames = products[0].keys()
# # #         with open(filename, "w", newline="", encoding="utf-8") as csvfile:
# # #             writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
# # #             writer.writeheader()
# # #             for prod in products:
# # #                 writer.writerow(prod)
# # #         print(f"CSV file '{filename}' created successfully with {len(products)} products.")

# # import csv
# # import os
# # import random
# # import time
# # import re
# # from datetime import datetime
# # import pytz

# # # ---- UPDATE THESE SELECTORS ----
# # PRODUCT_CARD_SELECTOR = "div[data-testid='product-card']"  # ← Update as needed
# # PRODUCT_CONTAINER_SELECTOR = "div.no-scrollbar.grid.grid-cols-2"  # ← Update as needed
# # SUBCATEGORY_SELECTOR = "div.no-scrollbar.sticky.top-[102px] a"    # ← Update as needed
# # # --------------------------------

# # from src.ui_actions.human_actions import HumanActions
# # from src.ui_actions.robust_actions import robust_query_selector
# # from src.utils.error_logger import ErrorLogger

# # logger = ErrorLogger("src/data/errors.log")

# # class ProductActions:
# #     def __init__(self, page, checkpoint_file="last_checkpoint.txt"):
# #         self.page = page
# #         self.human = HumanActions(page)
# #         self.checkpoint_file = checkpoint_file

# #     def get_row_height(self, product_card_selector):
# #         first_card = self.page.query_selector(product_card_selector)
# #         if first_card:
# #             return self.page.evaluate('(el) => el.offsetHeight', first_card)
# #         return 400

# #     def random_cart_interaction(self, product_card_selector):
# #         cards = self.page.query_selector_all(product_card_selector)
# #         # Pick 1-2 random cards to add/remove
# #         for card in random.sample(cards, k=min(len(cards), random.choice([1, 2]))):
# #             add_btn = card.query_selector('button[aria-label="add"]')
# #             if add_btn:
# #                 add_btn.click()
# #                 time.sleep(random.uniform(0.3, 0.7))
# #                 minus_btn = card.query_selector('button[aria-label="Remove"][data-testid="undefined-minus-btn"]')
# #                 if minus_btn:
# #                     minus_btn.click()
# #                     time.sleep(random.uniform(0.2, 0.5))

# #     def scroll_and_scrape(self):
# #         subcategory_links = self.page.query_selector_all(SUBCATEGORY_SELECTOR)
# #         for subcat_idx, link in enumerate(subcategory_links):
# #             subcat_text = link.inner_text().strip()
# #             # Sanitize subcategory for filename
# #             safe_subcat = re.sub(r'\W+', '_', subcat_text)
# #             csv_filename = f"products_{safe_subcat}.csv"

# #             logger.log(f"Processing subcategory: {subcat_text}")
# #             self.human.human_click(link)
# #             self.human.human_sleep(2, 3)
# #             self.page.wait_for_selector(PRODUCT_CARD_SELECTOR, timeout=5000)
# #             self._scroll_rows_and_scrape(subcat_text, csv_filename)

# #     def _scroll_rows_and_scrape(self, subcat_name, csv_filename):
# #         container = robust_query_selector(
# #             self.page,
# #             PRODUCT_CONTAINER_SELECTOR,
# #             retries=4,
# #             refresh_func=lambda: self.page.reload(),
# #             logger=logger,
# #             desc="Product card container"
# #         )
# #         card_height = self.page.evaluate("(el) => el.firstElementChild.offsetHeight", container)
# #         prev_count = -1
# #         last_row_seen = 0
# #         error_scroll_cycles = 0
# #         max_error_scroll_cycles = 3
# #         product_rank = 1

# #         # Write CSV header
# #         with open(csv_filename, "w", newline='', encoding='utf-8') as f:
# #             writer = csv.writer(f)
# #             writer.writerow([
# #                 "Timestamp", "Subcategory", "Rank", "Product Name", "Product URL", "Image URL", "Price",
# #                 "MRP", "Discount", "Rating", "Rating Count", "Delivery Time", "Pack/Size",
# #                 "Max Quantity", "Row", "Col"
# #             ])

# #         while True:
# #             cards = container.query_selector_all(PRODUCT_CARD_SELECTOR)
# #             curr_count = len(cards)
# #             if curr_count == prev_count:
# #                 if error_scroll_cycles < max_error_scroll_cycles:
# #                     logger.log(f"No new products loaded, scrolling up and then extra down. Cycle {error_scroll_cycles + 1}")
# #                     self.page.evaluate("(container, h) => { container.scrollTop -= h; }", container, card_height)
# #                     self.human.human_sleep(0.6, 1.1)
# #                     self.page.evaluate("(container, h) => { container.scrollTop += h * 2; }", container, card_height)
# #                     self.human.human_sleep(0.6, 1.2)
# #                     error_scroll_cycles += 1
# #                     continue
# #                 else:
# #                     logger.log("No new products loaded after multiple up-down cycles, stopping this subcategory.")
# #                     break
# #             else:
# #                 error_scroll_cycles = 0

# #             for i in range(last_row_seen, curr_count):
# #                 card = cards[i]
# #                 try:
# #                     self._process_product_card(card, subcat_name, csv_filename, rank=product_rank, row=i)
# #                     product_rank += 1
# #                 except Exception as e:
# #                     logger.log(f"Error processing product {i}: {e}")
# #                 self.save_checkpoint(subcat_name, i)
# #             last_row_seen = curr_count

# #             # Add a random card from this set (if new cards exist)
# #             if curr_count > last_row_seen:
# #                 rand_idx = random.randint(last_row_seen, curr_count - 1)
# #                 try:
# #                     self._add_random_card(cards[rand_idx])
# #                 except Exception as e:
# #                     logger.log(f"Failed to add product {rand_idx} to cart: {e}")

# #             self.human.human_sleep(0.7, 1.5)
# #             self.page.evaluate("(container, h) => { container.scrollTop += h; }", container, card_height)
# #             self.human.human_sleep(0.5, 1.0)
# #             prev_count = curr_count

# #     def _process_product_card(self, card, subcat_name, csv_filename, rank, row):
# #         def safe_inner_text_css(selector):
# #             elem = card.query_selector(selector)
# #             return elem.inner_text().strip() if elem else ""

# #         def safe_attr(selector, attr):
# #             elem = card.query_selector(selector)
# #             return elem.get_attribute(attr) if elem else ""

# #         url = card.get_attribute('href') or ""
# #         name = safe_inner_text_css('[data-testid="product-card-name"]')
# #         img_url = safe_attr('[data-testid="product-card-image"]', 'src')
# #         price = safe_inner_text_css('p[class*="text-"]')
# #         mrp = safe_inner_text_css('p[class*="line-through"]')
# #         discount = safe_inner_text_css('p[class*="bg-"]')
# #         rating = ""
# #         rating_count = ""
# #         delivery_time = ""
# #         packsize = ""
# #         max_qty = 1

# #         india = pytz.timezone("Asia/Kolkata")
# #         now_ist = datetime.now(india)
# #         timestamp = now_ist.strftime("%Y-%m-%d %H:%M:%S")
# #         row_data = [timestamp, subcat_name, rank, name, "https://www.zeptonow.com" + url, img_url, price, mrp, discount,
# #                     rating, rating_count, delivery_time, packsize, max_qty, row, ""]
# #         with open(csv_filename, "a", newline='', encoding="utf-8") as f:
# #             writer = csv.writer(f)
# #             writer.writerow(row_data)

# #     def _add_random_card(self, card):
# #         add_btn = card.query_selector('button[aria-label="add"]')
# #         if add_btn:
# #             self.human.human_click(add_btn)
# #             self.human.human_sleep(0.2, 0.5)
# #             for _ in range(random.randint(0, 2)):
# #                 plus_btn = card.query_selector('button[aria-label="Add"][data-testid="undefined-plus-btn"]')
# #                 if plus_btn:
# #                     self.human.human_click(plus_btn)
# #                     self.human.human_sleep(0.2, 0.5)
# #                 else:
# #                     break

# #     def save_checkpoint(self, subcat_name, row_idx):
# #         with open(self.checkpoint_file, "w") as f:
# #             f.write(f"{subcat_name},{row_idx}\n")

# #     def load_checkpoint(self):
# #         if os.path.exists(self.checkpoint_file):
# #             with open(self.checkpoint_file, "r") as f:
# #                 content = f.read().strip()
# #                 if content:
# #                     parts = content.split(",")
# #                     return parts[0], int(parts[1])
# #         return None, None
# #     # def get_product_card_row_height(page, product_card_selector):
# #     #     first_card = page.query_selector(product_card_selector)
# #     #     if first_card:
# #     #         # Assumes cards are in a row/grid; get height of one row
# #     #         return page.evaluate('(el) => el.offsetHeight', first_card)
# #     #     return 400  # fallback


# # # --- HOW TO USE ---
# # # scraper = AdvancedProductScraper(page)
# # # scraper.scroll_and_scrape()
# # src/actions/product_actions.py

# import csv
# import os
# import random
# import time
# import re
# from datetime import datetime
# import pytz

# from src.ui_actions.human_actions import HumanActions
# from src.ui_actions.robust_actions import robust_query_selector
# from src.utils.error_logger import ErrorLogger

# # ---- UPDATE THESE SELECTORS IF NEEDED ----
# PRODUCT_CARD_SELECTOR = "div[data-testid='product-card']"
# PRODUCT_CONTAINER_SELECTOR = "div.no-scrollbar.grid.grid-cols-2"
# SUBCATEGORY_SELECTOR = "div.no-scrollbar.sticky.top-[102px] a"
# # ------------------------------------------

# logger = ErrorLogger("src/data/errors.log")

# class ProductActions:
#     def __init__(self, page, checkpoint_file="last_checkpoint.txt"):
#         self.page = page
#         self.human = HumanActions(page)
#         self.checkpoint_file = checkpoint_file

#     def get_row_height(self, product_card_selector):
#         first_card = self.page.query_selector(product_card_selector)
#         if first_card:
#             return self.page.evaluate('(el) => el.offsetHeight', first_card)
#         return 400

#     def random_cart_interaction(self, product_card_selector):
#         cards = self.page.query_selector_all(product_card_selector)
#         if not cards:
#             return
#         # Pick 1-2 random cards to add/remove
#         for card in random.sample(cards, k=min(len(cards), random.choice([1, 2]))):
#             add_btn = card.query_selector('button[aria-label="add"]')
#             if add_btn:
#                 self.human.human_click(add_btn)
#                 time.sleep(random.uniform(0.3, 0.7))
#                 minus_btn = card.query_selector('button[aria-label="Remove"][data-testid="undefined-minus-btn"]')
#                 if minus_btn:
#                     self.human.human_click(minus_btn)
#                     time.sleep(random.uniform(0.2, 0.5))

#     def scroll_and_scrape(self):
#         subcategory_links = self.page.query_selector_all(SUBCATEGORY_SELECTOR)
#         for subcat_idx, link in enumerate(subcategory_links):
#             subcat_text = link.inner_text().strip()
#             # Sanitize subcategory for filename
#             safe_subcat = re.sub(r'\W+', '_', subcat_text)
#             csv_filename = f"src/data/products_{safe_subcat}.csv"

#             logger.log(f"Processing subcategory: {subcat_text}")
#             self.human.human_click(link)
#             self.human.human_sleep(2, 3)
#             self.page.wait_for_selector(PRODUCT_CARD_SELECTOR, timeout=5000)
#             self._scroll_rows_and_scrape(subcat_text, csv_filename)

#     def _scroll_rows_and_scrape(self, subcat_name, csv_filename):
#         container = robust_query_selector(
#             self.page,
#             PRODUCT_CONTAINER_SELECTOR,
#             retries=4,
#             refresh_func=lambda: self.page.reload(),
#             logger=logger,
#             desc="Product card container"
#         )
#         card_height = self.page.evaluate("(el) => el.firstElementChild.offsetHeight", container)
#         prev_count = -1
#         last_row_seen = 0
#         error_scroll_cycles = 0
#         max_error_scroll_cycles = 3
#         product_rank = 1

#         # Write CSV header
#         with open(csv_filename, "w", newline='', encoding='utf-8') as f:
#             writer = csv.writer(f)
#             writer.writerow([
#                 "Timestamp", "Subcategory", "Rank", "Product Name", "Product URL", "Image URL", "Price",
#                 "MRP", "Discount", "Rating", "Rating Count", "Delivery Time", "Pack/Size",
#                 "Max Quantity", "Row", "Col"
#             ])

#         while True:
#             cards = container.query_selector_all(PRODUCT_CARD_SELECTOR)
#             curr_count = len(cards)
#             if curr_count == prev_count:
#                 if error_scroll_cycles < max_error_scroll_cycles:
#                     logger.log(f"No new products loaded, scrolling up and then extra down. Cycle {error_scroll_cycles + 1}")
#                     self.page.evaluate("(container, h) => { container.scrollTop -= h; }", container, card_height)
#                     self.human.human_sleep(0.6, 1.1)
#                     self.page.evaluate("(container, h) => { container.scrollTop += h * 2; }", container, card_height)
#                     self.human.human_sleep(0.6, 1.2)
#                     error_scroll_cycles += 1
#                     continue
#                 else:
#                     logger.log("No new products loaded after multiple up-down cycles, stopping this subcategory.")
#                     break
#             else:
#                 error_scroll_cycles = 0

#             for i in range(last_row_seen, curr_count):
#                 card = cards[i]
#                 try:
#                     self._process_product_card(card, subcat_name, csv_filename, rank=product_rank, row=i)
#                     product_rank += 1
#                 except Exception as e:
#                     logger.log(f"Error processing product {i}: {e}")
#                 self.save_checkpoint(subcat_name, i)
#             last_row_seen = curr_count

#             # Add a random card from this set (if new cards exist)
#             if curr_count > last_row_seen:
#                 rand_idx = random.randint(last_row_seen, curr_count - 1)
#                 try:
#                     self._add_random_card(cards[rand_idx])
#                 except Exception as e:
#                     logger.log(f"Failed to add product {rand_idx} to cart: {e}")

#             self.human.human_sleep(0.7, 1.5)
#             self.page.evaluate("(container, h) => { container.scrollTop += h; }", container, card_height)
#             self.human.human_sleep(0.5, 1.0)
#             prev_count = curr_count

#     def _process_product_card(self, card, subcat_name, csv_filename, rank, row):
#         def safe_inner_text_css(selector):
#             elem = card.query_selector(selector)
#             return elem.inner_text().strip() if elem else ""

#         def safe_attr(selector, attr):
#             elem = card.query_selector(selector)
#             return elem.get_attribute(attr) if elem else ""

#         url = card.get_attribute('href') or ""
#         name = safe_inner_text_css('[data-testid="product-card-name"]')
#         img_url = safe_attr('[data-testid="product-card-image"]', 'src')
#         price = safe_inner_text_css('p[class*="text-"]')
#         mrp = safe_inner_text_css('p[class*="line-through"]')
#         discount = safe_inner_text_css('p[class*="bg-"]')
#         rating = ""
#         rating_count = ""
#         delivery_time = ""
#         packsize = ""
#         max_qty = 1

#         india = pytz.timezone("Asia/Kolkata")
#         now_ist = datetime.now(india)
#         timestamp = now_ist.strftime("%Y-%m-%d %H:%M:%S")
#         row_data = [timestamp, subcat_name, rank, name, "https://www.zeptonow.com" + url, img_url, price, mrp, discount,
#                     rating, rating_count, delivery_time, packsize, max_qty, row, ""]
#         with open(csv_filename, "a", newline='', encoding="utf-8") as f:
#             writer = csv.writer(f)
#             writer.writerow(row_data)

#     def _add_random_card(self, card):
#         add_btn = card.query_selector('button[aria-label="add"]')
#         if add_btn:
#             self.human.human_click(add_btn)
#             self.human.human_sleep(0.2, 0.5)
#             for _ in range(random.randint(0, 2)):
#                 plus_btn = card.query_selector('button[aria-label="Add"][data-testid="undefined-plus-btn"]')
#                 if plus_btn:
#                     self.human.human_click(plus_btn)
#                     self.human.human_sleep(0.2, 0.5)
#                 else:
#                     break

#     def save_checkpoint(self, subcat_name, row_idx):
#         with open(self.checkpoint_file, "w") as f:
#             f.write(f"{subcat_name},{row_idx}\n")

#     def load_checkpoint(self):
#         if os.path.exists(self.checkpoint_file):
#             with open(self.checkpoint_file, "r") as f:
#                 content = f.read().strip()
#                 if content:
#                     parts = content.split(",")
#                     return parts[0], int(parts[1])
#         return None, None
import csv
import os
import random
import time
import re
from datetime import datetime
import pytz

from src.ui_actions.human_actions import HumanActions
from src.ui_actions.robust_actions import robust_query_selector
from src.utils.error_logger import ErrorLogger

PRODUCT_CARD_SELECTOR = "div[data-testid='product-card']"
PRODUCT_CONTAINER_SELECTOR = "div.no-scrollbar.grid.grid-cols-2"
SUBCATEGORY_SELECTOR = "div.no-scrollbar.sticky.top-[102px] a"

logger = ErrorLogger("src/data/errors.log")

class ProductActions:
    def __init__(self, page, checkpoint_file="last_checkpoint.txt"):
        self.page = page
        self.human = HumanActions(page)
        self.checkpoint_file = checkpoint_file

    def get_row_height(self):
        """Get the height of one product card (for smooth scrolling)."""
        first_card = self.page.query_selector(PRODUCT_CARD_SELECTOR)
        if first_card:
            return self.page.evaluate('(el) => el.offsetHeight', first_card)
        return 400

    def get_subcategory_links(self):
        """Return a list of (element, name, href) for each subcategory."""
        links = self.page.query_selector_all(SUBCATEGORY_SELECTOR)
        subcats = []
        for link in links:
            name = link.inner_text().strip()
            href = link.get_attribute('href')
            subcats.append((link, name, href))
        return subcats

    def run(self):
        """Main entry: scrape each subcategory, robust to errors."""
        for link, subcat_name, _ in self.get_subcategory_links():
            try:
                safe_subcat = re.sub(r'\W+', '_', subcat_name)
                csv_filename = f"src/data/products_{safe_subcat}.csv"
                logger.log(f"Scraping subcategory: {subcat_name}")
                self.scrape_subcategory(link, subcat_name, csv_filename)
            except Exception as e:
                logger.log(f"Error scraping subcategory {subcat_name}: {e}")

    def scrape_subcategory(self, link, subcat_name, csv_filename):
        self.human.human_click(link)
        self.human.human_sleep(2, 3)
        self.page.wait_for_selector(PRODUCT_CARD_SELECTOR, timeout=8000)
        container = robust_query_selector(
            self.page,
            PRODUCT_CONTAINER_SELECTOR,
            retries=4,
            refresh_func=lambda: self.page.reload(),
            logger=logger,
            desc="Product card container"
        )
        row_height = self.get_row_height()
        seen_cards = set()
        stuck_count = 0
        MAX_STUCK = 3
        product_rank = 1

        # Write CSV header only once
        if not os.path.exists(csv_filename):
            with open(csv_filename, "w", newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                writer.writerow([
                    "Timestamp", "Subcategory", "Rank", "Product Name", "Product URL", "Image URL", "Price",
                    "MRP", "Discount", "Rating", "Rating Count", "Delivery Time", "Pack/Size",
                    "Max Quantity"
                ])

        while stuck_count < MAX_STUCK:
            cards = container.query_selector_all(PRODUCT_CARD_SELECTOR)
            new_cards = [c for i, c in enumerate(cards) if i not in seen_cards]
            if not new_cards:
                # Try to "unstick" the scroll
                self.recover_scroll(container, row_height)
                stuck_count += 1
                continue

            for idx, card in enumerate(new_cards):
                try:
                    prod_data = self.extract_product_info(card, product_rank, subcat_name)
                    self.append_to_csv(csv_filename, prod_data)
                    seen_cards.add(idx)
                    product_rank += 1
                    self.simulate_cart(card)
                except Exception as e:
                    logger.log(f"Error processing product at index {idx}: {e}")

            self.human.human_sleep(0.7, 1.4)
            self.page.evaluate("(container, h) => { container.scrollTop += h; }", container, row_height)
            stuck_count = 0  # reset if we loaded new cards

    def extract_product_info(self, card, rank, subcat_name):
        def safe_inner_text(selector):
            elem = card.query_selector(selector)
            return elem.inner_text().strip() if elem else ""
        def safe_attr(selector, attr):
            elem = card.query_selector(selector)
            return elem.get_attribute(attr) if elem else ""

        url = card.get_attribute('href') or ""
        name = safe_inner_text('[data-testid="product-card-name"]')
        img_url = safe_attr('[data-testid="product-card-image"]', 'src')
        price = safe_inner_text('p[class*="text-"]')
        mrp = safe_inner_text('p[class*="line-through"]')
        discount = safe_inner_text('p[class*="bg-"]')
        rating = ""
        rating_count = ""
        delivery_time = ""
        packsize = ""
        max_qty = 1  # (could add logic for add/remove if you want)

        timestamp = datetime.now(pytz.timezone("Asia/Kolkata")).strftime("%Y-%m-%d %H:%M:%S")
        return [
            timestamp, subcat_name, rank, name, "https://www.zeptonow.com" + url, img_url, price,
            mrp, discount, rating, rating_count, delivery_time, packsize, max_qty
        ]

    def append_to_csv(self, csv_filename, data_row):
        with open(csv_filename, "a", newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(data_row)

    def simulate_cart(self, card):
        """Randomly add and remove from cart for 1 out of every 2 rows."""
        if random.random() > 0.5:
            add_btn = card.query_selector('button[aria-label="add"]')
            if add_btn:
                self.human.human_click(add_btn)
                self.human.human_sleep(0.2, 0.5)
                # Remove if minus available
                minus_btn = card.query_selector('button[aria-label="Remove"][data-testid="undefined-minus-btn"]')
                if minus_btn:
                    self.human.human_click(minus_btn)
                    self.human.human_sleep(0.2, 0.5)

    def recover_scroll(self, container, row_height):
        """Attempt to unstick the scroll by going up and then down more."""
        self.page.evaluate("(container, h) => { container.scrollTop -= h; }", container, row_height)
        self.human.human_sleep(0.6, 1.1)
        self.page.evaluate("(container, h) => { container.scrollTop += h * 2; }", container, row_height)
        self.human.human_sleep(0.6, 1.2)
