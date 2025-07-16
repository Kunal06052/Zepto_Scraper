# src/ui_actions/category_clicker.py
import os
import csv

class SubCategoryClicker:
    def __init__(self, page):
        self.page = page

#clicking the subcategories one by one 
    def click_subcategory_by_name(self, subcat_name): 
        """
        Clicks a subcategory whose text matches subcat_name (case-insensitive).
        Returns True if clicked, False if not found.
        """
        # Find all <a> elements inside the scrollable div
        links = self.page.query_selector_all('div[data-hide-appsflyer-cls-element="true"] .no-scrollbar a.relative')
        for link in links:
            # Each <a> has a <p> inside with the name
            name_elem = link.query_selector("p")
            name = name_elem.inner_text().strip() if name_elem else ""
            if name.lower() == subcat_name.lower():
                link.click()
                print(f"[CategoryClicker] Clicked subcategory: {name}")
                return True
        print(f"[CategoryClicker] Subcategory '{subcat_name}' not found!")
        return False
    
    def get_or_create_subcategory_csv(self, csv_path="subcategories.csv"):
        """
        If CSV exists and has data, read and return list.
        Otherwise, scrape subcategory names, save, and return list.
        """
        subcat_names = []

        # Check if file exists and is not empty
        if os.path.isfile(csv_path) and os.path.getsize(csv_path) > 0:
            with open(csv_path, "r", encoding="utf-8") as f:
                reader = csv.DictReader(f)
                for row in reader:
                    name = row["subcategory_name"].strip()
                    if name:
                        subcat_names.append(name)
            if subcat_names:
                print(f"Loaded {len(subcat_names)} subcategories from {csv_path}")
                return subcat_names

        # Else, scrape from website and save
        print(f"{csv_path} not found or empty. Scraping subcategory names from site...")
        links = self.page.query_selector_all("div.no-scrollbar a.relative")
        for link in links:
            name_elem = link.query_selector("p")
            name = name_elem.inner_text().strip() if name_elem else ""
            if name:
                subcat_names.append(name)

        # Save to CSV
        with open(csv_path, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=["subcategory_name"])
            writer.writeheader()
            for name in subcat_names:
                writer.writerow({"subcategory_name": name})

        print(f"Saved {len(subcat_names)} subcategories to {csv_path}")
        return subcat_names