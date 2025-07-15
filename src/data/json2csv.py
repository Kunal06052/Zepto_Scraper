import json
import pandas as pd
import os

def convert_and_append(json_file, csv_file):
    try:
        with open(json_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except Exception as e:
        print("Failed to open or parse JSON:", e)
        return

    if "storeProducts" not in data or not data["storeProducts"]:
        print("No products in JSON")
        return

    rows = []
    for item in data["storeProducts"]:
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
    if os.path.exists(csv_file):
        existing_df = pd.read_csv(csv_file)
        df = df[~df['objectId'].isin(existing_df['objectId'])]

    if df.empty:
        print("No new products to append.")
        return

    write_header = not os.path.exists(csv_file) or os.path.getsize(csv_file) == 0
    df.to_csv(csv_file, mode='a', header=write_header, index=False)
    print(f"Appended {len(df)} new products to {csv_file}")
