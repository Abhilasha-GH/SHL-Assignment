from app.services.retriever import search_assessments

query = "Java backend developer with stakeholder communication"

results = search_assessments(query)

for item in results:
    print(item)