# # from playwright.sync_api import sync_playwright
# # import random
# # from src.utils.error_logger import ErrorLogger  # Assuming you have error_logger.py

# # logger = ErrorLogger("src/data/errors.log")

# # def get_human_window_size():
# #     # Common desktop sizes, not always "maximized"
# #     sizes = [
# #         (1366, 768), (1440, 900), (1536, 864), (1600, 900),
# #         (1680, 1050), (1920, 1080), (1280, 720)
# #     ]
# #     return random.choice(sizes)

# # class DriverManagers:
# #     def __init__(self, headless=True):
# #         try:
# #             self.playwright = sync_playwright().start()
# #             width, height = get_human_window_size()
# #             self.browser = self.playwright.chromium.launch(headless=headless)
# #             # You can also set user-agent here for stealth
# #             self.context = self.browser.new_context(
# #                 viewport={"width": width, "height": height},
# #                 user_agent=self.get_random_user_agent()
# #             )
# #             self.page = self.context.new_page()
# #         except Exception as e:
# #             logger.log_error("Error initializing browser context", error=e)
# #             raise

# #     def get_random_user_agent(self):
# #         # Add a pool of real user agents
# #         agents = [
# #             "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
# #             "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0.1 Safari/605.1.15",
# #             # Add more if needed
# #         ]
# #         return random.choice(agents)

# #     def get_page(self):
# #         return self.page

# #     def maximize_window(self):
# #         # Playwright doesn't have a 'maximize', but you can set a big viewport
# #         try:
# #             self.page.set_viewport_size({"width": 1920, "height": 1080})
# #         except Exception as e:
# #             logger.log_error("Error maximizing window", error=e)

# #     def close(self):
# #         try:
# #             self.browser.close()
# #             self.playwright.stop()
# #         except Exception as e:
# #             logger.log_error("Error closing browser", error=e)

# from playwright.sync_api import sync_playwright
# import random
# from src.utils.error_logger import ErrorLogger

# logger = ErrorLogger("src/data/errors.log")

# def get_human_window_size():
#     sizes = [
#         (1920, 1080)
#     ]
#     return random.choice(sizes)

# class DriverManagers:
#     def __init__(self, headless=False):
#         try:
#             self.playwright = sync_playwright().start()
#             width, height = get_human_window_size()
#             self.browser = self.playwright.chromium.launch(headless=headless)
#             self.context = self.browser.new_context(
#                 viewport={"width": width, "height": height},
#                 user_agent=self.get_random_user_agent()
#             )
#             self.page = self.context.new_page()
#         except Exception as e:
#             logger.log_exception(e, context="Error initializing browser context")
#             raise

#     def get_random_user_agent(self):
#         agents = [
#             "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
#             "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36",
#             "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
#             "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36",
#             "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"
#         ]
#         return random.choice(agents)

#     def get_page(self):
#         return self.page

#     def close(self):
#         try:
#             self.browser.close()
#             self.playwright.stop()
#         except Exception as e:
#             logger.log_exception(e, context="Error closing browser")
from playwright.sync_api import sync_playwright
import random
from src.utils.error_logger import ErrorLogger

logger = ErrorLogger("src/data/errors.log")

class DriverManagers:
    def __init__(self, headless=False, use_max_window=True):
        try:
            self.playwright = sync_playwright().start()
            self.browser = self.playwright.chromium.launch(headless=headless)
            if use_max_window:
                # Use no_viewport to get full native window (not headless)
                self.context = self.browser.new_context(
                    no_viewport=True,
                    user_agent=self.get_random_user_agent()
                )
            else:
                width, height = 1920, 1080  # Or (2560, 1440) for 2K monitor
                self.context = self.browser.new_context(
                    viewport={"width": width, "height": height},
                    user_agent=self.get_random_user_agent()
                )
            self.page = self.context.new_page()
        except Exception as e:
            logger.log_exception(e, context="Error initializing browser context")
            raise

    def get_random_user_agent(self):
        agents = [
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"
        ]
        return random.choice(agents)

    def get_page(self):
        return self.page

    def close(self):
        try:
            self.browser.close()
            self.playwright.stop()
        except Exception as e:
            logger.log_exception(e, context="Error closing browser")
