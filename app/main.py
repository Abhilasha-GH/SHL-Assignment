from fastapi import FastAPI
from pydantic import BaseModel
from typing import List

from app.services.retriever import search_assessments
from app.services.comparison import compare_assessments

app = FastAPI()


# -----------------------------
# Models
# -----------------------------

class Message(BaseModel):
    role: str
    content: str


class ChatRequest(BaseModel):
    messages: List[Message]


# -----------------------------
# Root Route
# -----------------------------

@app.get("/")
def root():
    return {
        "message": "SHL Assessment API is running"
    }


# -----------------------------
# Health Check
# -----------------------------

@app.get("/health")
def health():
    return {
        "status": "ok"
    }


# -----------------------------
# Chat Endpoint
# -----------------------------

@app.post("/chat")
def chat(request: ChatRequest):

    # Combine all conversation messages
    conversation_text = " ".join(
        [msg.content for msg in request.messages]
    ).lower()

    # -----------------------------
    # Clarification Queries
    # -----------------------------

    vague_queries = [
        "i need an assessment",
        "help me hire",
        "suggest assessment",
        "hiring",
        "need a test"
    ]

    # -----------------------------
    # Blocked Topics
    # -----------------------------

    blocked_topics = [
        "salary",
        "legal",
        "lawsuit",
        "ignore previous instructions",
        "system prompt",
        "politics",
        "religion"
    ]

    # -----------------------------
    # Clarification Logic
    # -----------------------------

    if any(query in conversation_text for query in vague_queries):

        if len(request.messages) == 1:

            return {
                "reply": "Sure. What role are you hiring for and what skills do you want to assess?",
                "recommendations": [],
                "end_of_conversation": False
            }

    # -----------------------------
    # Refusal Logic
    # -----------------------------

    if any(topic in conversation_text for topic in blocked_topics):

        return {
            "reply": "I can only help with SHL assessment recommendations and comparisons.",
            "recommendations": [],
            "end_of_conversation": False
        }

    # -----------------------------
    # Comparison Logic
    # -----------------------------

    if "difference" in conversation_text or "compare" in conversation_text:

        comparison = compare_assessments(conversation_text)

        if comparison:

            return {
                "reply": comparison,
                "recommendations": [],
                "end_of_conversation": False
            }

    # -----------------------------
    # Query Refinement
    # -----------------------------

    if "personality" in conversation_text:
        conversation_text += " personality behavioral assessment"

    if "technical" in conversation_text:
        conversation_text += " coding programming technical skills"

    if "cognitive" in conversation_text:
        conversation_text += " cognitive reasoning aptitude"

    # -----------------------------
    # Retrieve Assessments
    # -----------------------------

    results = search_assessments(conversation_text)

    recommendations = []

    for item in results:

        recommendations.append({
            "name": item.get("name", "Unknown Assessment"),
            "url": item.get("url", ""),
            "test_type": item.get("test_type", "Unknown")
        })

    # -----------------------------
    # Final Response
    # -----------------------------

    return {
        "reply": "Here are recommended SHL assessments.",
        "recommendations": recommendations,
        "end_of_conversation": False
    }
