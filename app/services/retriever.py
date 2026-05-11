import json
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))

CATALOG_PATH = os.path.join(BASE_DIR, "data", "cleaned_catalog.json")


def search_assessments(query: str):

    with open(CATALOG_PATH, "r", encoding="utf-8") as f:
        catalog = json.load(f)

    results = []

    query = query.lower()

    for item in catalog:

        name = item.get("name", "").lower()
        description = item.get("description", "").lower()

        if query in name or query in description:
            results.append(item)

    if len(results) == 0:
        results = catalog[:5]

    return results[:5]
