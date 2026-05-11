import json

with open("data/cleaned_catalog.json", "r", encoding="utf-8") as f:
    catalog = json.load(f)


def search_assessments(query: str, top_k: int = 5):

    query = query.lower()

    scored = []

    for item in catalog:

        score = 0

        text = (
            item.get("name", "") + " " +
            item.get("description", "")
        ).lower()

        for word in query.split():

            if word in text:
                score += 1

        if score > 0:
            scored.append((score, item))

    scored.sort(reverse=True, key=lambda x: x[0])

    return [item for _, item in scored[:top_k]]
