import json
import pandas as pd
import os
import pytz
from datetime import datetime
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

JSON_FILE_PATH = 'src/data/zepto_products.json'
CSV_FILE_PATH = 'zepto_products.csv'

def convert_and_append():
    try:
        with open(JSON_FILE_PATH, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except Exception as e:
        print("Failed to open or parse JSON:", e)
        return

    rows = []
    india = pytz.timezone('Asia/Kolkata')
    now_ist = datetime.now(india).strftime('%d/%m/%y %H:%M:%S')

    for item in data.get("storeProducts", []):
        row = {
            "timestamp": now_ist,
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

    if not rows:
        print("No products to write.")
        return

    df = pd.DataFrame(rows)
    # Deduplicate by 'objectId' (if possible)
    if os.path.exists(CSV_FILE_PATH) and os.path.getsize(CSV_FILE_PATH) > 0:
        existing_df = pd.read_csv(CSV_FILE_PATH)
        # Only append rows that do not exist already (based on objectId and timestamp)
        df = df[~df['objectId'].isin(existing_df['objectId'])]

    if df.empty:
        print("No new products to append.")
        return

    write_header = not os.path.exists(CSV_FILE_PATH) or os.path.getsize(CSV_FILE_PATH) == 0
    df.to_csv(CSV_FILE_PATH, mode='a', header=write_header, index=False)
    print(f"Wrote {len(df)} rows to {CSV_FILE_PATH}")

class JsonFileEventHandler(FileSystemEventHandler):
    def on_modified(self, event):
        if event.src_path.endswith('zepto_products.json'):
            print(f"Detected update in {event.src_path}")
            convert_and_append()

def watch_json_file():
    # Watch the directory containing the JSON file
    path = os.path.dirname(JSON_FILE_PATH)
    event_handler = JsonFileEventHandler()
    observer = Observer()
    observer.schedule(event_handler, path, recursive=False)
    observer.start()
    print(f"Watching for changes in {JSON_FILE_PATH} ...")
    try:
        while True:
            pass
    except KeyboardInterrupt:
        observer.stop()
    observer.join()

if __name__ == "__main__":
    watch_json_file()
