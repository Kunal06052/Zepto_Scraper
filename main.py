# # # At the top of your main.py or a globals.py
# # NEW_PRODUCTS_FOUND = False

# # def network_batch_callback():
# #     global NEW_PRODUCTS_FOUND
# #     NEW_PRODUCTS_FOUND = True



# # # # from src.core.driver_manager import DriverManagers
# # # # from src.actions.location_actions import Action
# # # # from src.actions.navigation_actions import NavigationActions
# # # # from src.actions.product_actions import ProductActions
# # # # from src.network.network_catcher import NetworkDataCatcher
# # # # from src.network.json_product_saver import convert_json_to_csv
# # # # from src.utils.exporters import ZeptoJSONtoCSVConverter
# # # # from src.utils.error_logger import ErrorLogger
# # # # logger = ErrorLogger("logs/errors.log")



# # # # if __name__ == "__main__":
# # # #     driver = DriverManagers(headless=True)
# # # #     page = driver.get_page()
# # # #     page.goto("https://www.zeptonow.com")

# # # #     # Location and navigation
# # # #     location_actions = Action(page)
# # # #     location_actions.set_location("Golf Course Metro Station")

# # # #     navigation = NavigationActions(page)
# # # #     navigation.scroll_right_n_times(2)
# # # #     navigation.click_category_by_href("/cn/cold-drinks-juices")

# # # #     # Attach network catcher
# # # #     network_catcher = NetworkDataCatcher(
# # # #         page,
# # # #         keyword="store-products-by-store-subcategory-id",
# # # #         save_file="src/data/zepto_products.json"
# # # #     )
    
# # # #     subcategories = navigation.list_subcategories()
# # # #     print("Available subcategories:")
# # # #     for idx, name, _ in subcategories:
# # # #         print(f"{idx}: {name}")
# # # #     chosen = int(input("Enter the number of the subcategory you want to select: "))
# # # #     navigation.choose_subcategory_by_index(chosen)

# # # #     product_actions = ProductActions(page)
# # # #     product_actions.process_all_products(save_csv=True)
# # # #         # Append latest JSON to CSV
# # # #     # json_path = "src/data/zepto_products.json"
# # # #     # csv_path = "src/data/zepto_products.csv"
# # # #     # converter = ZeptoJSONtoCSVConverter(json_path, csv_path)
# # # #     # converter.convert()

# # # #     input("Press Enter to close browser after selecting Subcategory...")

# # # #     driver.close()


# # # from src.core.driver_manager import DriverManagers
# # # from src.actions.location_actions import Action
# # # from src.actions.navigation_actions import NavigationActions
# # # from src.actions.product_actions import ProductActions
# # # from src.network.network_catcher import NetworkDataCatcher

# # # if __name__ == "__main__":
# # #     driver = DriverManagers(headless=False)
# # #     page = driver.get_page()
# # #     page.goto("https://www.zeptonow.com")

# # #     # Location and navigation
# # #     location_actions = Action(page)
# # #     location_actions.set_location("Golf Course Metro Station")

# # #     navigation = NavigationActions(page)
# # #     navigation.scroll_right_n_times(2)
# # #     navigation.click_category_by_href("/cn/cold-drinks-juices")

# # #     # Attach network catcher (JSON, not JSONL)
# # #     network_catcher = NetworkDataCatcher(
# # #         page,
# # #         keyword="store-products-by-store-subcategory-id",
# # #         save_file="src/data/zepto_products.json"
# # #     )

# # #     subcategories = navigation.list_subcategories()
# # #     print("Available subcategories:")
# # #     for idx, name, _ in subcategories:
# # #         print(f"{idx}: {name}")
# # #     chosen = int(input("Enter the number of the subcategory you want to select: "))
# # #     navigation.choose_subcategory_by_index(chosen)

# # #     product_actions = ProductActions(page)
# # #     product_actions.process_all_products(save_csv=False)

# # #     input("Press Enter to close browser after selecting Subcategory...")
# # #     driver.close()
# import schedule
# import time
# import traceback
# from src.core.driver_manager import DriverManagers
# from src.actions.location_actions import Action
# from src.actions.navigation_actions import NavigationActions
# from src.actions.product_actions import ProductActions
# from src.network.network_catcher import NetworkDataCatcher
# from src.utils.error_logger import ErrorLogger

# logger = ErrorLogger("src/data/errors.log")

# def zepto_scrape_job():
#     try:
#         driver = DriverManagers(headless=False)
#         page = driver.get_page()
#         page.goto("https://www.zeptonow.com")
#         location_actions = Action(page)
#         location_actions.set_location("Golf Course Metro Station")
#         navigation = NavigationActions(page)
#         navigation.scroll_right_n_times(2)
#         navigation.click_category_by_href("/cn/cold-drinks-juices")
#         network_catcher = NetworkDataCatcher(
#             page,
#             keyword='store-products-by-store-subcategory-id',
#             json_file="src/data/zepto_products.json",
#             csv_file="src/data/zepto_products.csv"
#         )

#         subcategories = navigation.list_subcategories()
#         logger.log("Available subcategories listed", context=str([x[1] for x in subcategories]))
#         # Pick first subcategory for automation; or you can randomize/iterate
#         navigation.choose_subcategory_by_index(0)
#         product_actions = ProductActions(page)
#         product_actions.scroll_and_scrape()
#         driver.close()
#     except Exception as e:
#         logger.log_exception(e, context="main.zepto_scrape_job")
#         print(traceback.format_exc())

# if __name__ == "__main__":
#     # Run once at start
#     zepto_scrape_job()
#     # Then schedule every hour
#     schedule.every().hour.at(":00").do(zepto_scrape_job)
#     print("Scheduler started, will run job every hour.")
#     while True:
#         schedule.run_pending()
#         time.sleep(10)
# # from src.core.driver_manager import DriverManagers
# # from src.actions.location_actions import Action
# # from src.actions.navigation_actions import NavigationActions
# # from src.actions.product_actions import ProductActions

# # def main():
# #     driver = DriverManagers(headless=False)
# #     page = driver.get_page()
# #     page.goto("https://www.zeptonow.com")
# #     location_actions = Action(page)
# #     location_actions.set_location("Golf Course Metro Station")
# #     navigation = NavigationActions(page)
# #     navigation.scroll_right_n_times(2)
# #     navigation.click_category_by_href("/cn/cold-drinks-juices")
# #     product_actions = ProductActions(page)
# #     product_actions.scroll_and_scrape()
# #     driver.close()

# # if __name__ == "__main__":
# #     main()
from src.core.driver_manager import DriverManagers
from src.actions.location_actions import Action
from src.actions.navigation_actions import NavigationActions
from src.actions.product_actions import ProductActions
from src.page_objects.category_page import CategoryPage
import time

def main():
    driver = DriverManagers(headless=False)
    page = driver.get_page()
    page.goto("https://www.zeptonow.com")
    time.sleep(10)
    location_actions = Action(page)
    location_actions.set_location("Golf Course Metro Station")
    time.sleep(10)
    category_page = CategoryPage(page)
    category_page.humanized_carousel_scroll(net_right=2)
    time.sleep(10)
    category_page.click_link_by_exact_href("/cn/cold-drinks-juices/cold-drinks-juices/cid/947a72ae-b371-45cb-ad3a-778c05b64399/scid/7dceec53-78f9-4f06-83d7-c8edd9c2f71a?")
    # category_page.select_category_by_href("/cn/cold-drinks-juices/")
    # navigation = NavigationActions(page)
    # navigation.scroll_right_n_times(2)
    # navigation.click_category_by_href("/cn/cold-drinks-juices")
    time.sleep(10)
    product_actions = ProductActions(page)
    product_actions.run()
    driver.close()

if __name__ == "__main__":
    main()
