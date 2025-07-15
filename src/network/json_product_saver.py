import os
import csv
from datetime import datetime
import pytz
import json
from pytz import timezone

IST = pytz.timezone('Asia/Kolkata')

import os
import json
from datetime import datetime
import pytz

def save_zepto_products_json(data, json_file="src/data/zepto_products.json"):
    os.makedirs(os.path.dirname(json_file), exist_ok=True)
    IST = pytz.timezone("Asia/Kolkata")
    data_with_time = {
        "timestamp": datetime.now(IST).strftime("%Y-%m-%d %H:%M:%S"),
        "storeProducts": data.get("storeProducts", [])
    }
    with open(json_file, "w", encoding="utf-8") as f:
        json.dump(data_with_time, f, ensure_ascii=False, indent=2)
    print(f"[JSON SAVER] Wrote fresh data to {json_file}")


# def save_zepto_products_json(data, json_file="src/data/zepto_products.json"):
#     # Ensure directory exists
#     os.makedirs(os.path.dirname(json_file), exist_ok=True)
#     # Add timestamp at root
#     # IST = timezone("Asia/Kolkata")
#     data_with_time = {
#         "timestamp": datetime.now(IST).strftime("%Y-%m-%d %H:%M:%S"),
#         "storeProducts": data.get("storeProducts", [])
#     }
#     # Always overwrite the JSON file
#     with open(json_file, "w", encoding="utf-8") as f:
#         json.dump(data_with_time, f, ensure_ascii=False, indent=2)
#     print(f"[JSON SAVER] Wrote fresh data to {json_file}")


# def save_zepto_products_json(json_data, json_file="zepto_products.json"):
#     # Optionally, add a timestamp to each record
#     wrapper = {
#         "timestamp": datetime.now(IST).strftime("%Y-%m-%d %H:%M:%S"),
#         "data": json_data
#     }
#     # Append each record as a new line (JSONL format)
#     with open(json_file, "a", encoding="utf-8") as f:
#         f.write(json.dumps(wrapper, ensure_ascii=False))
#         f.write("\n")
#     print(f"Saved Zepto response as JSON to {json_file}.")

def extract_zepto_row(product):
    # (Same function as shared above)
    p = product
    pv = p.get("productVariant", {})
    prod = p.get("product", {})
    # img_path = ""
    # if pv.get("images") and len(pv["images"]):
    #     img_path = "https://cdn.zeptonow.com/production/" + pv["images"][0]["path"]
    return {
        "timestamp": datetime.now(IST).strftime("%Y-%m-%d %H:%M:%S"),
        "object_id": p.get("objectId"),
        "product_id": prod.get("id"),
        "product_name": prod.get("name"),
        "brand": prod.get("brand"),
        "category": p.get("primaryCategoryName"),
        "subcategory": p.get("primarySubcategoryName"),
        "mrp": pv.get("mrp", 0) / 100,
        "selling_price": p.get("sellingPrice", 0) / 100,
        "discounted_price": p.get("discountedSellingPrice", 0) / 100,
        "discount_percent": p.get("discountPercent"),
        "discount_amount": p.get("discountAmount", 0) / 100,
        "available_quantity": p.get("availableQuantity"),
        "max_allowed_quantity": pv.get("maxAllowedQuantity"),
        "unit": pv.get("unitOfMeasure"),
        "packsize": pv.get("formattedPacksize"),
        "average_rating": (pv.get("ratingSummary") or {}).get("averageRating"),
        "total_ratings": (pv.get("ratingSummary") or {}).get("totalRatings"),
        # "image_url": img_path,
        "is_active": p.get("isActive"),
        "out_of_stock": p.get("outOfStock"),
    }

# def save_zepto_products(json_data, csv_file="zepto_products.csv"):
#     store_products = json_data.get("storeProducts", [])
#     rows = [extract_zepto_row(p) for p in store_products]
#     if not rows:
#         print("No products found in response.")
#         return
#     fieldnames = list(rows[0].keys())
#     file_exists = os.path.exists(csv_file)
#     with open(csv_file, "a", newline='', encoding='utf-8') as f:
#         writer = csv.DictWriter(f, fieldnames=fieldnames)
#         if not file_exists:
#             writer.writeheader()
#         for row in rows:
#             writer.writerow(row)
#     print(f"Saved {len(rows)} Zepto products to {csv_file}.")


def convert_json_to_csv(json_data):
    """
    Converts a list of product dictionaries (from Zepto JSON) into a CSV string,
    adding 'Date' and 'Time' columns.

    Args:
        json_data (dict): The parsed JSON data containing 'storeProducts'.

    Returns:
        str: A string containing the CSV data.
    """
    if not json_data or "data" not in json_data or "storeProducts" not in json_data["data"]:
        print("Error: Invalid JSON structure. 'data' or 'storeProducts' key not found.")
        return ""

    products = json_data["data"]["storeProducts"]
    if not products:
        print("No products found in the JSON data.")
        return ""

    # Define the fieldnames for the CSV, including the new 'Date' and 'Time' columns
    fieldnames = [
        "Product Name", "Brand", "MRP", "Discounted Selling Price",
        "Discount Percent", "Available Quantity", "Primary Category",
        "Primary Subcategory", "Packsize", "Unit of Measure",
        "Date", "Time"
    ]

    csv_rows = []
    # Add the header row
    csv_rows.append(",".join(f'"{header}"' for header in fieldnames))

    current_date = datetime.now().strftime("%Y-%m-%d")
    current_time = datetime.now().strftime("%H:%M:%S")

    for item in products:
        product_info = item.get("product", {})
        product_variant_info = item.get("productVariant", {})
        pricing_info = item.get("pricing", {})
        inventory_info = item.get("inventory", {})
        category_info = product_info.get("primarySubcategoryName", "")

        product_name = product_info.get("name", "N/A")
        brand = product_info.get("brand", "N/A")
        mrp = product_variant_info.get("mrp", 0)
        packsize = product_variant_info.get("packsize", "N/A")
        unit_of_measure = product_variant_info.get("unitOfMeasure", "N/A")
        primary_category = product_info.get("primaryCategoryName", "N/A")
        primary_subcategory = product_info.get("primarySubcategoryName", "N/A")

        # Calculate Discounted Selling Price and Discount Percent
        discounted_selling_price = mrp
        discount_percent = 0

        # Check for selling price in pricing campaigns first
        if pricing_info and pricing_info.get("pricingCampaigns"):
            for campaign in pricing_info["pricingCampaigns"]:
                if campaign.get("pricingCampaignType") == "PriceUpdate":
                    discounted_selling_price = campaign.get("sellingPrice", mrp)
                    break
        elif pricing_info and pricing_info.get("sellingPrice"):
            discounted_selling_price = pricing_info["sellingPrice"]

        if mrp > 0 and discounted_selling_price < mrp:
            discount_percent = round(((mrp - discounted_selling_price) / mrp) * 100)

        available_quantity = inventory_info.get("availableQuantity", 0)

        # Create a dictionary for the current product's data
        row_data = {
            "Product Name": product_name,
            "Brand": brand,
            "MRP": mrp,
            "Discounted Selling Price": discounted_selling_price,
            "Discount Percent": discount_percent,
            "Available Quantity": available_quantity,
            "Primary Category": primary_category,
            "Primary Subcategory": primary_subcategory,
            "Packsize": packsize,
            "Unit of Measure": unit_of_measure,
            "Date": current_date,
            "Time": current_time
        }

        # Format the row for CSV
        csv_row = []
        for field in fieldnames:
            value = row_data.get(field, "")
            # Enclose string values in double quotes and escape existing quotes
            if isinstance(value, str):
                csv_row.append(f'"{value.replace('"', '""')}"')
            else:
                csv_row.append(str(value))
        csv_rows.append(",".join(csv_row))

    return "\n".join(csv_rows)

# def save_zepto_products_json(data, json_file="src/data/zepto_products.json"):
#     # Overwrite the file!
#     os.makedirs(os.path.dirname(json_file), exist_ok=True)
#     IST = timezone("Asia/Kolkata")
#     data_with_time = {
#         "timestamp": datetime.now(IST).strftime("%Y-%m-%d %H:%M:%S"),
#         "storeProducts": data.get("storeProducts", [])
#     }
#     with open(json_file, "w", encoding="utf-8") as f:
#         json.dump(data_with_time, f, ensure_ascii=False, indent=2)
#     print(f"[JSON SAVER] Wrote fresh data to {json_file}")

