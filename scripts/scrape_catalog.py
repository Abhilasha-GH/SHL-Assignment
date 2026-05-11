import requests
from bs4 import BeautifulSoup
import json

url = "https://www.shl.com/solutions/products/product-catalog/"

headers = {
    "User-Agent": "Mozilla/5.0"
}

response = requests.get(url, headers=headers)

soup = BeautifulSoup(response.text, "lxml")

links = soup.find_all("a")

catalog = []

for link in links:

    title = link.get_text(strip=True)
    href = link.get("href")

    if title and href:

        if "/products/" in href:

            full_url = (
                href
                if href.startswith("http")
                else f"https://www.shl.com{href}"
            )

            description = link.parent.get_text(" ", strip=True)

            item = {
                "name": title,
                "url": full_url,
                "description": description
            }

            if item not in catalog:
                catalog.append(item)

print(f"Found {len(catalog)} assessments")

with open("data/shl_catalog.json", "w", encoding="utf-8") as f:
    json.dump(catalog, f, indent=2)

print("Saved to data/shl_catalog.json")