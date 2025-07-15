# import json
# import csv
# import os


# class ZeptoJSONtoCSVConverter:
#     def __init__(self, json_path, csv_path):
#         self.json_path = json_path
#         self.csv_path = csv_path

#     def extract_row(self, product, timestamp=None):
#         prod = product.get('product', {})
#         pv = product.get('productVariant', {})
#         img_url = ""
#         if pv.get("images") and len(pv["images"]):
#             img_url = "https://cdn.zeptonow.com/production/" + pv["images"][0]["path"]
#         meta_tags = product.get("meta", {}).get("tags", [])
#         tags_v2 = product.get("meta", {}).get("tagsV2", {})
#         pricing_campaigns = product.get("pricingCampaigns", [])
#         bundleItems = product.get("bundleItems", [])
#         valueBasedDiscount = product.get("valueBasedDiscount", {})

#         return {
#             "timestamp": timestamp,
#             "store_id": product.get("storeId"),
#             "object_id": product.get("objectId"),
#             "product_id": prod.get("id"),
#             "product_name": prod.get("name"),
#             "brand": prod.get("brand"),
#             "category": product.get("primaryCategoryName"),
#             "subcategory": product.get("primarySubcategoryName"),
#             "mrp": pv.get("mrp", 0) / 100,
#             "selling_price": product.get("sellingPrice", 0) / 100,
#             "discounted_price": product.get("discountedSellingPrice", 0) / 100,
#             "discount_percent": product.get("discountPercent"),
#             "discount_amount": product.get("discountAmount", 0) / 100,
#             "available_quantity": product.get("availableQuantity"),
#             "max_allowed_quantity": pv.get("maxAllowedQuantity"),
#             "unit": pv.get("unitOfMeasure"),
#             "packsize": pv.get("formattedPacksize"),
#             "average_rating": (pv.get("ratingSummary") or {}).get("averageRating"),
#             "total_ratings": (pv.get("ratingSummary") or {}).get("totalRatings"),
#             "image_url": img_url,
#             "is_active": product.get("isActive"),
#             "out_of_stock": product.get("outOfStock"),
#             "last_updated_at": product.get("lastUpdatedAt"),
#             "product_type": product.get("productType"),
#             "is_new_product": product.get("isNewProduct"),
#             "fssai_license": pv.get("fssaiLicense"),
#             "ingredients": prod.get("ingredients"),
#             "shelf_life": pv.get("shelfLifeInHours"),
#             "packaging_type": pv.get("packagingType"),
#             "description": prod.get("description"),
#             "bundle_items": bundleItems,
#             "meta_tags": meta_tags,
#             "tags_v2": tags_v2,
#             "pricing_campaigns": pricing_campaigns,
#             "value_based_discount": valueBasedDiscount,
#         }

#     def convert(self):
#     # Check if file exists and is not empty
#         if not os.path.exists(self.json_path) or os.path.getsize(self.json_path) == 0:
#             print(f"JSON file '{self.json_path}' is missing or empty. Nothing to convert.")
#             return

#         with open(self.json_path, "r", encoding="utf-8") as infile:
#             try:
#                 data_obj = json.load(infile)
#             except Exception as e:
#                 print(f"Error decoding JSON in '{self.json_path}': {e}")
#                 return

#         if isinstance(data_obj, dict):
#             products = data_obj.get("storeProducts", [])
#             timestamp = data_obj.get("timestamp") or ""
#             rows = [self.extract_row(prod, timestamp) for prod in products]
#         elif isinstance(data_obj, list):
#             rows = []
#             for entry in data_obj:
#                 t = entry.get("timestamp") or ""
#                 for prod in entry.get("storeProducts", []):
#                     rows.append(self.extract_row(prod, t))
#         else:
#             print("Unrecognized JSON structure")
#             return

#         if not rows:
#             print("No product data found in the JSON file.")
#             return

#         fieldnames = list(rows[0].keys())
#         file_exists = os.path.exists(self.csv_path)
#         with open(self.csv_path, "a", newline="", encoding="utf-8") as csvfile:
#             writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
#             if not file_exists or os.path.getsize(self.csv_path) == 0:
#                 writer.writeheader()
#             for row in rows:
#                 writer.writerow(row)
#         print(f"Appended {len(rows)} rows to {self.csv_path}.")

# # # import json
# # # import os

# # # class ZeptoCSVExporter:
# # #     def __init__(self, convert_func):
# # #         self.convert_func = convert_func

# # #     def append_all_jsonl_to_csv(self, jsonl_file, csv_file):
# # #         """Appends all data from JSONL to CSV (useful for full batch export, not for hourly schedule)."""
# # #         # If jsonl_file does not exist, create it as empty
# # #         if not os.path.exists(jsonl_file):
# # #             # Optionally: create an empty file, or just skip
# # #             with open(jsonl_file, "w", encoding="utf-8") as f:
# # #                 pass  # Just create it
# # #             print(f"Created empty {jsonl_file} since it did not exist.")
# # #             return  # or continue as needed

# # #         header_written = os.path.exists(csv_file) and os.path.getsize(csv_file) > 0
# # #         with open(jsonl_file, "r", encoding="utf-8") as infile, \
# # #              open(csv_file, "a", encoding="utf-8") as outfile:
# # #             for line in infile:
# # #                 line = line.strip()
# # #                 if not line:
# # #                     continue
# # #                 json_obj = json.loads(line)
# # #                 csv_str = self.convert_func(json_obj)
# # #                 csv_lines = csv_str.strip().split("\n")
# # #                 if not header_written:
# # #                     outfile.write(csv_lines[0] + "\n")  # write header
# # #                     header_written = True
# # #                 outfile.write("\n".join(csv_lines[1:]) + "\n")  # append only rows

# # #     def append_latest_jsonl_to_csv(self, jsonl_file, csv_file):
# # #         """Appends only the latest line (last scrape) from JSONL to CSV (recommended for hourly runs)."""
# # #         # Check if file exists first
# # #         if not os.path.exists(jsonl_file):
# # #             # Optionally: create the file or just print a warning and skip
# # #             with open(jsonl_file, "w", encoding="utf-8") as f:
# # #                 pass  # Just create it
# # #             print(f"Created empty {jsonl_file} since it did not exist. No data to append.")
# # #             return  # Nothing to append, so we return

# # #         with open(jsonl_file, "rb") as f:
# # #             try:
# # #                 f.seek(-2, os.SEEK_END)
# # #                 while f.read(1) != b'\n':
# # #                     f.seek(-2, os.SEEK_CUR)
# # #             except OSError:
# # #                 f.seek(0)
# # #             last_line = f.readline().decode()

# # #         if not last_line.strip():
# # #             print(f"No latest line found in {jsonl_file}.")
# # #             return

# # #         json_obj = json.loads(last_line)
# # #         csv_str = self.convert_func(json_obj)
# # #         csv_lines = csv_str.strip().split("\n")

# # #         header_needed = not os.path.exists(csv_file) or os.path.getsize(csv_file) == 0
# # #         with open(csv_file, "a", encoding="utf-8") as outfile:
# # #             if header_needed:
# # #                 outfile.write(csv_lines[0] + "\n")
# # #             if len(csv_lines) > 1:
# # #                 outfile.write("\n".join(csv_lines[1:]) + "\n")

# # #         print(f"Appended latest scrape to {csv_file}")
import json
import csv
import os


from src.data.json2csv import flatten_json  # If you put the flattener in another file


class ZeptoJSONtoCSVConverter:
    def __init__(self, json_path, csv_path):
        self.json_path = json_path
        self.csv_path = csv_path

    def extract_row(self, product, timestamp=None):
        # ... (same as your latest, not repeating here for brevity)
        
        prod = product.get('product', {})
        pv = product.get('productVariant', {})
        img_url = ""
        if pv.get("images") and len(pv["images"]):
            img_url = "https://cdn.zeptonow.com/production/" + pv["images"][0]["path"]
        meta_tags = product.get("meta", {}).get("tags", [])
        tags_v2 = product.get("meta", {}).get("tagsV2", {})
        pricing_campaigns = product.get("pricingCampaigns", [])
        bundleItems = product.get("bundleItems", [])
        valueBasedDiscount = product.get("valueBasedDiscount", {})

    def convert(self):
        if not os.path.exists(self.json_path) or os.path.getsize(self.json_path) == 0:
            print(f"JSON file '{self.json_path}' is missing or empty. Nothing to convert.")
            return

        with open(self.json_path, "r", encoding="utf-8") as infile:
            try:
                data_obj = json.load(infile)
            except Exception as e:
                print(f"Error decoding JSON in '{self.json_path}': {e}")
                return

        if isinstance(data_obj, dict):
            products = data_obj.get("storeProducts", [])
            timestamp = data_obj.get("timestamp") or ""
            rows = [self.extract_row(prod, timestamp) for prod in products]
        elif isinstance(data_obj, list):
            rows = []
            for entry in data_obj:
                t = entry.get("timestamp") or ""
                for prod in entry.get("storeProducts", []):
                    rows.append(self.extract_row(prod, t))
        else:
            print("Unrecognized JSON structure")
            return

        if not rows:
            print("No product data found in the JSON file.")
            return

        fieldnames = list(rows[0].keys())
        file_exists = os.path.exists(self.csv_path)
        with open(self.csv_path, "a", newline="", encoding="utf-8") as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            if not file_exists or os.path.getsize(self.csv_path) == 0:
                writer.writeheader()
            for row in rows:
                writer.writerow(row)
        print(f"Appended {len(rows)} rows to {self.csv_path}.")

    # def json_to_flat_csv(json_path, csv_path):
    #     with open(json_path, "r", encoding="utf-8") as infile:
    #         data = json.load(infile)

    #     timestamp = data.get("timestamp")
    #     products = data.get("storeProducts", [])

    #     rows = []
    #     for prod in products:
    #         flat_row = flatten_json(prod)
    #         flat_row['timestamp'] = timestamp
    #         rows.append(flat_row)

    #     # Gather all possible fields
    #     all_keys = set()
    #     for r in rows:
    #         all_keys.update(r.keys())
    #     fieldnames = sorted(all_keys)

    #     # Append to CSV
    #     file_exists = os.path.exists(csv_path)
    #     with open(csv_path, "a", newline="", encoding="utf-8") as csvfile:
    #         writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    #         # Only write header if file is empty
    #         if not file_exists or os.path.getsize(csv_path) == 0:
    #             writer.writeheader()
    #         for row in rows:
    #             writer.writerow(row)
    #     print(f"Appended {len(rows)} rows to {csv_path}.")



    def json_to_flat_csv(json_path, csv_path):
        with open(json_path, "r", encoding="utf-8") as infile:
            data = json.load(infile)

        timestamp = data.get("timestamp")
        products = data.get("storeProducts", [])

        rows = []
        for prod in products:
            flat_row = flatten_json(prod)
            flat_row['timestamp'] = timestamp
            rows.append(flat_row)

        all_keys = set()
        for r in rows:
            all_keys.update(r.keys())
        fieldnames = sorted(all_keys)

        file_exists = os.path.exists(csv_path)
        with open(csv_path, "a", newline="", encoding="utf-8") as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            if not file_exists or os.path.getsize(csv_path) == 0:
                writer.writeheader()
            for row in rows:
                writer.writerow(row)
        print(f"Appended {len(rows)} rows to {csv_path}.")
