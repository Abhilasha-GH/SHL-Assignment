from app.services.retriever import search_assessments


def compare_assessments(query: str):

    results = search_assessments(query)

    if len(results) < 2:
        return "Not enough assessments found to compare."

    response = "Comparison between assessments:\n\n"

    for item in results[:2]:

        response += (
            f"Name: {item['name']}\n"
            f"URL: {item['url']}\n"
            f"Description: {item.get('description', 'No description')}\n\n"
        )

    return response
