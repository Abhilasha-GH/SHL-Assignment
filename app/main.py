from fastapi import FastAPI
from pydantic import BaseModel
from typing import List

from app.services.retriever import search_assessments
from app.services.comparison import compare_assessments

app = FastAPI()


# Message schema
class Message(BaseModel):
    role: str
    content: str


# Request schema
class ChatRequest(BaseModel):
    messages: List[Message]


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/chat")
def chat(request: ChatRequest):

    # Combine full conversation history
    conversation_text = " ".join(
        [msg.content for msg in request.messages]
    ).lower()

    # Vague queries
    vague_queries = [
        "i need an assessment",
        "help me hire",
        "suggest assessment",
        "hiring",
        "need a test"
    ]

    # Blocked topics
    blocked_topics = [
        "salary",
        "legal",
        "lawsuit",
        "ignore previous instructions",
        "system prompt",
        "politics",
        "religion"
    ]

    # Clarification logic
    if any(query in conversation_text for query in vague_queries):

        if len(request.messages) == 1:

            return {
                "reply": "Sure. What role are you hiring for and what skills do you want to assess?",
                "recommendations": [],
                "end_of_conversation": False
            }

    # Refusal logic
    if any(topic in conversation_text for topic in blocked_topics):

        return {
            "reply": "I can only help with SHL assessment recommendations and comparisons.",
            "recommendations": [],
            "end_of_conversation": False
        }

    # Comparison logic
    if "difference" in conversation_text or "compare" in conversation_text:

        comparison = compare_assessments(conversation_text)

        if comparison:

            return {
                "reply": comparison,
                "recommendations": [],
                "end_of_conversation": False
            }

    # Refinement logic
    if "personality" in conversation_text:
        conversation_text += " personality assessment behavioral assessment"

    if "technical" in conversation_text:
        conversation_text += " coding technical skills"

    if "cognitive" in conversation_text:
        conversation_text += " cognitive ability reasoning"

    # Retrieval step
    results = search_assessments(conversation_text)

    recommendations = []

    for item in results:

        recommendations.append({
            "name": item["name"],
            "url": item["url"],
            "test_type": "Unknown"
        })

    return {
        "reply": "Here are recommended SHL assessments.",
        "recommendations": recommendations,
        "end_of_conversation": False
    }