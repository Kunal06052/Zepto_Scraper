# src/config.py

CATEGORY_CARD_SELECTOR = "div.embla__container a"
# src/config.py

CATEGORY_SCROLL_RIGHT_SELECTOR = (
    'section.embla div.embla__viewport '
    'div.absolute.right-5.top-1\\/2.z-10.-translate-y-1\\/2 > button.-rotate-180'
)

CATEGORY_SCROLL_LEFT_SELECTOR = "div.absolute.left-5 button.flex.h-8.w-8"
CATEGORY_SCROLL_RIGHT_SELECTOR = (
    '//div[contains(@class, "absolute") and contains(@class, "right-5") and '
    'contains(@class, "top-1/2") and contains(@class, "z-10") and contains(@class, "-translate-y-1/2")]'
    '/button[contains(@class, "-rotate-180")]'
)

CATEGORY_SCROLL_LEFT_SELECTOR = (
    "div.absolute.left-5.top-1\\/2.-translate-y-1\\/2 > button"
)

CATEGORY_SCROLL_RIGHT_SELECTOR = "button.embla__button--next"
SUBCATEGORY_LINK_SELECTOR = '//div[contains(@class,"no-scrollbar")]//a'
# SUBCATEGORY_LINKS_SELECTOR = "div.no-scrollbar a"
PRODUCT_CARD_SELECTOR = "a[data-testid='product-card']"
TIMEOUT = 10000
DEFAULT_LOCATION = "Golf Course Metro Station"
XHR_KEYWORD = "store-products-by-store-subcategory-id"
DATA_DIR = "src/data/"
JSON_FILE = DATA_DIR + "zepto_products.json"
CSV_FILE = DATA_DIR + "zepto_products.csv"
LOG_FILE = DATA_DIR + "errors.log"
LAST_STATE_FILE = DATA_DIR + "last_state.json"
PRODUCT_CARD_SELECTOR = "div[data-testid='product-card']"      # ← UPDATE: CSS for each product card
PRODUCT_CONTAINER_SELECTOR = "div.no-scrollbar.grid.grid-cols-2" # ← UPDATE: CSS for main scrollable container
SUBCATEGORY_SELECTOR = "ul.subcategories li"                      # ← UPDATE: CSS for subcategory tabs/links
LOCATION_BUTTON_SELECTOR = 'button[aria-haspopup="dialog"][aria-label="Select Location"]'
LOCATION_INPUT_SELECTOR = 'input[placeholder="Search a new address"]'
LOCATION_RESULT_SELECTOR = 'div[data-testid="address-search-container"] div[data-testid="address-search-item"]:first-child'
LOCATION_CONFIRM_SELECTOR = 'button[data-testid="location-confirm-btn"]'
# src/config.py

# PRODUCT_CARD_SELECTOR = "div[data-testid='product-card']"
# SUBCATEGORY_SELECTOR = "div.no-scrollbar.sticky.top-[102px] a"
XHR_PRODUCT_PATTERN = "/api/store-products-by-store-subcategory-id"
# PRODUCT_CARD_SELECTOR = "div[data-testid='product-card']"
# PRODUCT_CONTAINER_SELECTOR = "div.no-scrollbar.grid.grid-cols-2"
ADD_BUTTON_SELECTOR = 'button[aria-label="add"]'
PLUS_BUTTON_SELECTOR = 'button[aria-label="Add"][data-testid="undefined-plus-btn"]'
MINUS_BUTTON_SELECTOR = 'button[aria-label="Remove"][data-testid="undefined-minus-btn"]'