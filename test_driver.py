# import asyncio
# import os
# import random
# import re
# import time
# from datetime import datetime
# import pytz
# import json
# from playwright.async_api import async_playwright

# # Constants
# BASE_URL = "https://www.zeptonow.com "
# CATEGORY_URL = "/cn/cold-drinks-juices/..."  # Replace with actual category URL
# XHR_PATTERN = "/api/store-products-by-store-subcategory-id"
# OUTPUT_DIR = "output"
# CSV_HEADER = [
#     "Timestamp", "Subcategory", "Rank", "Product Name", "Product URL", "Image URL",
#     "Price", "MRP", "Discount", "Rating", "Rating Count", "Delivery Time", "Pack/Size"
# ]

# # Ensure output directory exists
# os.makedirs(OUTPUT_DIR, exist_ok=True)

# async def intercept_xhr(route, request):
#     """Intercept XHR requests that contain product data."""
#     if XHR_PATTERN in request.url:
#         print(f"[XHR] Intercepted product data request: {request.url}")
#         try:
#             response = await route.fetch()
#             json_data = await response.json()
#             route.continue_()
#             return json_data
#         except Exception as e:
#             print(f"[XHR] Failed to fetch JSON: {e}")
#             route.continue_()
#             return None
#     else:
#         route.continue_()
#         return None


# class ZeptonowScraper:
#     def __init__(self, page):
#         self.page = page
#         self.products_collected = []
#         self.human_delay = self.random_delay
#         self.product_rank = 1

#     async def spoof_browser(self):
#         """Spoof browser properties to avoid bot detection"""
#         await self.page.add_init_script("""
#             delete navigator.__proto__.webdriver;
#             window.chrome = {runtime: {}};
#         """)
#         await self.page.set_user_agent(
#             "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122 Safari/537.36"
#         )

#     def random_delay(self, min_sec=0.5, max_sec=1.5):
#         delay = random.uniform(min_sec, max_sec)
#         time.sleep(delay)

#     async def click_subcategories_and_scrape(self, subcat_links):
#         """Click each subcategory and scrape product data"""
#         for idx, (link, name, href) in enumerate(subcat_links):
#             safe_name = re.sub(r'[^\w]', '_', name[:20])
#             csv_path = f"{OUTPUT_DIR}/products_{safe_name}.csv"

#             print(f"[Main] Processing subcategory: {name} ({idx + 1}/{len(subcat_links)})")
#             await self._click_subcategory(link, name, csv_path)

#     async def _click_subcategory(self, link, subcat_name, csv_path):
#         """Click subcategory and start scraping"""
#         await link.click()
#         self.random_delay(2, 4)

#         # Wait for product grid
#         await self.page.wait_for_selector("div[data-testid='product-card']", timeout=15000)

#         # Set up XHR interception
#         self.products_collected = []
#         await self.page.route("**/store-products-by-store-subcategory-id*", lambda r: self._handle_route(r))

#         # Scroll one row at a time
#         container = await self.page.query_selector("div.no-scrollbar.grid.grid-cols-2")
#         first_card = await self.page.query_selector("div[data-testid='product-card']")
#         row_height = await self.page.evaluate("(el) => el.offsetHeight", first_card) if first_card else 400

#         prev_count = -1
#         stuck_count = 0
#         MAX_STUCK = 3

#         while stuck_count < MAX_STUCK:
#             cards = await self.page.query_selector_all("div[data-testid='product-card']")
#             curr_count = len(cards)

#             if curr_count == prev_count:
#                 stuck_count += 1
#                 print(f"[Scroll] No new products loaded. Stuck count: {stuck_count}")
#                 await self._recover_scroll(container, row_height)
#                 continue

#             print(f"[Scroll] New products detected: {curr_count - prev_count}")
#             stuck_count = 0
#             prev_count = curr_count

#             # Process only newly visible cards
#             for i in range(len(cards)):
#                 card = cards[i]
#                 if i >= len(self.products_collected):
#                     await self._process_product_card(card, subcat_name, csv_path)

#             # Simulate random add/remove
#             if cards:
#                 rand_idx = random.randint(0, len(cards) - 1)
#                 await self._simulate_cart_interaction(cards[rand_idx])

#             # Scroll down by one row
#             await self.page.evaluate(f"window.scrollBy(0, {row_height})")
#             self.random_delay(0.8, 1.5)

#     print(f"[{subcat_name}] Finished scraping.")

#     # Save final batch
#     await self._save_products_to_csv(csv_path, subcat_name)

#     # Reset route handler
#     await self.page.unroute("**/store-products-by-store-subcategory-id*")

#     # Reload page to reset state
#     await self.page.reload()

#     self.random_delay(2, 3)

#     return True

#     async def _handle_route(self, route):
#         """Collect product data from intercepted XHR responses"""
#         try:
#             response = await route.fetch()
#             data = await response.json()
#             self.products_collected.extend(data.get("data", []))
#             print(f"[XHR] Collected {len(data.get('data', []))} products from XHR.")
#         except Exception as e:
#             print(f"[XHR] Error extracting data: {e}")
#         finally:
#             await route.continue_()

#     async def _process_product_card(self, card, subcat_name, csv_path):
#         """Extract product info and save to CSV"""
#         url = await card.get_attribute("href")
#         name_elem = await card.query_selector('[data-testid="product-card-name"]')
#         name = await name_elem.inner_text() if name_elem else ""

#         img_elem = await card.query_selector('[data-testid="product-card-image"]')
#         img_url = await img_elem.get_attribute("src") if img_elem else ""

#         price_elem = await card.query_selector("p[class*='text-']")
#         price = await price_elem.inner_text() if price_elem else ""

#         mrp_elem = await card.query_selector("p[class*='line-through']")
#         mrp = await mrp_elem.inner_text() if mrp_elem else ""

#         discount_elem = await card.query_selector("p[class*='bg-']")
#         discount = await discount_elem.inner_text() if discount_elem else ""

#         india_time = datetime.now(pytz.timezone("Asia/Kolkata")).strftime("%Y-%m-%d %H:%M:%S")

#         product_data = {
#             "Timestamp": india_time,
#             "Subcategory": subcat_name,
#             "Rank": self.product_rank,
#             "Product Name": name,
#             "Product URL": BASE_URL + url if url else "",
#             "Image URL": img_url,
#             "Price": price,
#             "MRP": mrp,
#             "Discount": discount,
#             "Rating": "",
#             "Rating Count": "",
#             "Delivery Time": "",
#             "Pack/Size": "",
#         }

#         await self._append_to_csv(csv_path, product_data)
#         self.product_rank += 1

#     async def _append_to_csv(self, path, data):
#         """Append product data to CSV file"""
#         file_exists = os.path.exists(path)
#         with open(path, "a", newline="", encoding="utf-8") as f:
#             writer = csv.DictWriter(f, fieldnames=CSV_HEADER)
#             if not file_exists:
#                 writer.writeheader()
#             writer.writerow(data)

#     async def _simulate_cart_interaction(self, card):
#         """Add and remove a random product"""
#         add_btn = await card.query_selector("button[aria-label='add']")
#         if add_btn:
#             await add_btn.click()
#             self.random_delay(0.3, 0.7)

#         minus_btn = await card.query_selector("button[aria-label='Remove'][data-testid='undefined-minus-btn']")
#         if minus_btn:
#             await minus_btn.click()
#             self.random_delay(0.3, 0.6)

#     async def _recover_scroll(self, container, row_height):
#         """Scroll up then down to recover lazy loading"""
#         await self.page.evaluate(f"window.scrollBy(0, -{row_height})")
#         self.random_delay(0.6, 1.2)
#         await self.page.evaluate(f"window.scrollBy(0, {row_height * 2})")
#         self.random_delay(0.6, 1.2)

#     async def get_subcategories(self):
#         """Return list of subcategory links with names and hrefs"""
#         links = await self.page.query_selector_all("div.no-scrollbar.sticky.top-\\[102px\\] a")
#         subcats = []

#         for link in links:
#             name = await link.inner_text()
#             href = await link.get_attribute("href")
#             subcats.append((link, name.strip(), href.strip()))

#         return subcats

#     async def run(self):
#         """Main entry point"""
#         async with async_playwright() as p:
#             browser = await p.chromium.launch(headless=False)
#             context = await browser.new_context(
#                 viewport={"width": 1280, "height": 800},
#                 user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0 Safari/537.36"
#             )
#             self.page = await context.new_page()
#             await self.page.goto(BASE_URL)
#             self.random_delay(2, 4)

#             # Set location manually or automate it
#             print("[Location] Setting location...")
#             # You can add code here to interact with location input

#             # Go to category page
#             await self.page.goto(CATEGORY_URL)
#             self.random_delay(3, 5)

#             # Get subcategories
#             subcats = await self.get_subcategories()
#             print(f"[Main] Found {len(subcats)} subcategories.")

#             # Start scraping
#             await self.click_subcategories_and_scrape(subcats)

#             await context.close()
#             await browser.close()

#     async def _save_products_to_csv(self, filename, subcategory):
#         """Save collected product data to CSV"""
#         if not self.products_collected:
#             print(f"[{subcategory}] No product data to save.")
#             return

#         file_exists = os.path.exists(filename)

#         with open(filename, "a", newline="", encoding="utf-8") as f:
#             writer = csv.DictWriter(f, fieldnames=CSV_HEADER)
#             if not file_exists:
#                 writer.writeheader()
#             for item in self.products_collected:
#                 writer.writerow({
#                     "Timestamp": item.get("timestamp", ""),
#                     "Subcategory": subcategory,
#                     "Rank": self.product_rank,
#                     "Product Name": item.get("name", ""),
#                     "Product URL": item.get("url", ""),
#                     "Image URL": item.get("image", ""),
#                     "Price": item.get("price", ""),
#                     "MRP": item.get("mrp", ""),
#                     "Discount": item.get("discount", ""),
#                     "Rating": item.get("rating", ""),
#                     "Rating Count": item.get("rating_count", ""),
#                     "Delivery Time": item.get("delivery_time", ""),
#                     "Pack/Size": item.get("pack_size", "")
#                 })
#                 self.product_rank += 1

#         print(f"[{subcategory}] Saved {len(self.products_collected)} products to {filename}")


# if __name__ == "__main__":
#     async def main():
#         async with async_playwright() as p:
#             browser = await p.chromium.launch(headless=False)
#             page = await browser.new_page()
#             scraper = ZeptonowScraper(page)
#             await scraper.run()
#             await browser.close()

#     asyncio.run(main())


#test for checking subcategory function 
from src.page_objects.subcategory_page import SubCategoryClicker


subcategory = SubCategoryClicker()
subcategory.click_subcategory_by_name("Top Picks")