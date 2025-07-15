# import os
# import json
# import pandas as pd

# class NetworkDataCatcher:

#     def __init__(self, page, keyword='store-products-by-store-subcategory-id',
#                  json_file="src/data/zepto_products.json", csv_file="src/data/zepto_products.csv"):
#         self.page = page
#         self.keyword = keyword
#         self.json_file = json_file
#         self.csv_file = csv_file
#         os.makedirs(os.path.dirname(self.json_file), exist_ok=True)
#         os.makedirs(os.path.dirname(self.csv_file), exist_ok=True)
#         self.page.on("response", self._response_interceptor)

#     # def __init__(self, page, keyword='store-products-by-store-subcategory-id', csv_file="src/data/zepto_products.csv"):
#     #     self.page = page
#     #     self.keyword = keyword
#     #     self.csv_file = csv_file
#     #     os.makedirs(os.path.dirname(self.csv_file), exist_ok=True)
#     #     self.page.on("response", self._response_interceptor)

#     def _response_interceptor(self, response):
#         try:
#             url = response.url
#             rtype = response.request.resource_type
#             if self.keyword in url and rtype == "xhr":
#                 try:
#                     data = response.json()
#                 except Exception as e:
#                     print(f"Could not parse JSON from XHR: {e}")
#                     return

#                 products = data.get("storeProducts", [])
#                 if not products:
#                     print("No products found in this batch.")
#                     return

#                 # 1. Save latest batch to JSON
#                 with open(self.json_file, "w", encoding="utf-8") as f:
#                     json.dump({"storeProducts": products}, f, ensure_ascii=False, indent=2)

#                 # 2. Convert and append to CSV (deduplicate by objectId)
#                 rows = []
#                 for item in products:
#                     row = {
#                         "objectId": item.get("objectId"),
#                         "storeId": item.get("storeId"),
#                         "discountedSellingPrice": item.get("discountedSellingPrice"),
#                         "discountPercent": item.get("discountPercent"),
#                         "discountAmount": item.get("discountAmount"),
#                         "availableQuantity": item.get("availableQuantity"),
#                         "primaryCategoryName": item.get("primaryCategoryName"),
#                         "primarySubcategoryName": item.get("primarySubcategoryName"),
#                         "product_name": item.get("product", {}).get("name"),
#                         "product_brand": item.get("product", {}).get("brand"),
#                         "mrp": item.get("productVariant", {}).get("mrp"),
#                         "formattedPacksize": item.get("productVariant", {}).get("formattedPacksize"),
#                     }
#                     rows.append(row)
#                 import pandas as pd
#                 df = pd.DataFrame(rows)
#                 if os.path.exists(self.csv_file):
#                     existing_df = pd.read_csv(self.csv_file)
#                     df = df[~df['objectId'].isin(existing_df['objectId'])]
#                 write_header = not os.path.exists(self.csv_file) or os.path.getsize(self.csv_file) == 0
#                 if not df.empty:
#                     df.to_csv(self.csv_file, mode='a', header=write_header, index=False)
#                     print(f"Appended {len(df)} new products to {self.csv_file}")
#                 else:
#                     print("No new products to append.")
#         except Exception as e:
#             print("[Network] Interceptor error:", e)
import os
import json
import pandas as pd

class NetworkDataCatcher:
    def __init__(self, page, keyword='store-products-by-products',
                 json_file="src/data/zepto_products.json", csv_file="src/data/zepto_products.csv"):
        self.page = page
        self.keyword = keyword
        self.json_file = json_file
        self.csv_file = csv_file
        os.makedirs(os.path.dirname(self.json_file), exist_ok=True)
        os.makedirs(os.path.dirname(self.csv_file), exist_ok=True)

    def catch_next_batch(self, timeout=10000):
        """Call this immediately after scrolling: waits for and processes next batch."""
        def matcher(response):
            return (
                self.keyword in response.url
                and response.request.resource_type == "xhr"
            )
        try:
            response = self.page.wait_for_response(matcher, timeout=timeout)
            self._process_response(response)
        except Exception as e:
            print(f"No {self.keyword} XHR after scroll:", e)

    def _process_response(self, response):
        try:
            data = response.json()
            products = data.get("storeProducts", [])
            if not products:
                print("No products found in this batch.")
                return

            with open(self.json_file, "w", encoding="utf-8") as f:
                json.dump({"storeProducts": products}, f, ensure_ascii=False, indent=2)

            rows = []
            for item in products:
                row = {
                    "objectId": item.get("objectId"),
                    "storeId": item.get("storeId"),
                    "discountedSellingPrice": item.get("discountedSellingPrice"),
                    "discountPercent": item.get("discountPercent"),
                    "discountAmount": item.get("discountAmount"),
                    "availableQuantity": item.get("availableQuantity"),
                    "primaryCategoryName": item.get("primaryCategoryName"),
                    "primarySubcategoryName": item.get("primarySubcategoryName"),
                    "product_name": item.get("product", {}).get("name"),
                    "product_brand": item.get("product", {}).get("brand"),
                    "mrp": item.get("productVariant", {}).get("mrp"),
                    "formattedPacksize": item.get("productVariant", {}).get("formattedPacksize"),
                }
                rows.append(row)
            df = pd.DataFrame(rows)
            if os.path.exists(self.csv_file):
                existing_df = pd.read_csv(self.csv_file)
                df = df[~df['objectId'].isin(existing_df['objectId'])]
            write_header = not os.path.exists(self.csv_file) or os.path.getsize(self.csv_file) == 0
            if not df.empty:
                df.to_csv(self.csv_file, mode='a', header=write_header, index=False)
                print(f"Appended {len(df)} new products to {self.csv_file}")
            else:
                print("No new products to append.")
        except Exception as e:
            print("Error processing XHR:", e)
