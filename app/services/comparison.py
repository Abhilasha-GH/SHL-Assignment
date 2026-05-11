import json


with open("data/cleaned_catalog.json", "r", encoding="utf-8") as f:
    catalog = json.load(f)


def compare_assessments(query):

    matches = []

    for item in catalog:

        name = item["name"].lower()

        if name in query.lower():
            matches.append(item)

    if len(matches) < 2:
        return None

    comparison_text = "Comparison between assessments:\n\n"

    for item in matches[:2]:

        comparison_text += (
            f"Name: {item['name']}\n"
            f"URL: {item['url']}\n"
            f"Description: {item.get('description', 'No description')}\n\n"
        )

    return comparison_text