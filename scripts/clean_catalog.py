import json

with open("data/shl_catalog.json", "r", encoding="utf-8") as f:
    data = json.load(f)

cleaned = []
seen_urls = set()

valid_keywords = [
    "assessment",
    "personality",
    "ability",
    "cognitive",
    "behavioral",
    "skills"
]

bad_names = [
    "learn more",
    "view all",
    "read more"
]

bad_url_keywords = [
    "report",
    "framework",
    "catalog"
]

for item in data:

    name = item["name"].strip()
    url = item["url"].strip()

    # Remove duplicates
    if url in seen_urls:
        continue

    # Keep relevant assessment pages
    if not any(keyword in url.lower() for keyword in valid_keywords):
        continue

    # Remove empty names
    if len(name) < 3:
        continue

    # Remove noisy names
    if name.lower() in bad_names:
        continue

    # Remove noisy URLs
    if any(word in url.lower() for word in bad_url_keywords):
        continue

    cleaned.append({
        "name": name,
        "url": url,
        "description": item.get("description", "")
    })

    seen_urls.add(url)

with open("data/cleaned_catalog.json", "w", encoding="utf-8") as f:
    json.dump(cleaned, f, indent=2)

print(f"Cleaned assessments: {len(cleaned)}")