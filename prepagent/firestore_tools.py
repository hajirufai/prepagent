"""
Firestore-backed tools for PrepAgent.
Fallback when MongoDB MCP is not available.
Uses Google Cloud Firestore (free tier: 1 GiB storage, 50K reads/day).
"""

import os
import json
from datetime import datetime
from google.oauth2 import service_account
from google.auth.transport.requests import AuthorizedSession

PROJECT = os.environ.get("GOOGLE_CLOUD_PROJECT", "interview-buddy-457520")
KEY_FILE = os.environ.get("GOOGLE_APPLICATION_CREDENTIALS", "/work/secrets/gcp-interview-buddy-sa.json")

def _get_session():
    creds = service_account.Credentials.from_service_account_file(
        KEY_FILE, scopes=["https://www.googleapis.com/auth/cloud-platform"]
    )
    return AuthorizedSession(creds)

BASE = f"https://firestore.googleapis.com/v1/projects/{PROJECT}/databases/(default)/documents"


def store_question(category: str, difficulty: str, role: str, question: str, 
                   hints: list, sample_answer: str, tags: list, company: str = "general") -> str:
    """Store an interview question in Firestore."""
    session = _get_session()
    doc = {
        "fields": {
            "category": {"stringValue": category},
            "difficulty": {"stringValue": difficulty},
            "role": {"stringValue": role},
            "company": {"stringValue": company},
            "question": {"stringValue": question},
            "hints": {"arrayValue": {"values": [{"stringValue": h} for h in hints]}},
            "sample_answer": {"stringValue": sample_answer},
            "tags": {"arrayValue": {"values": [{"stringValue": t} for t in tags]}},
            "created_at": {"stringValue": datetime.utcnow().isoformat()},
        }
    }
    resp = session.post(f"{BASE}/questions", json=doc)
    return f"Question stored: {resp.status_code}"


def get_questions(category: str = None, difficulty: str = None, role: str = None, limit: int = 10) -> str:
    """Retrieve interview questions from Firestore with optional filters."""
    session = _get_session()
    # Use structured query
    query = {
        "structuredQuery": {
            "from": [{"collectionId": "questions"}],
            "limit": limit,
        }
    }
    if category or difficulty or role:
        filters = []
        if category:
            filters.append({"fieldFilter": {"field": {"fieldPath": "category"}, "op": "EQUAL", "value": {"stringValue": category}}})
        if difficulty:
            filters.append({"fieldFilter": {"field": {"fieldPath": "difficulty"}, "op": "EQUAL", "value": {"stringValue": difficulty}}})
        if role:
            filters.append({"fieldFilter": {"field": {"fieldPath": "role"}, "op": "EQUAL", "value": {"stringValue": role}}})
        
        if len(filters) == 1:
            query["structuredQuery"]["where"] = filters[0]
        else:
            query["structuredQuery"]["where"] = {"compositeFilter": {"op": "AND", "filters": filters}}
    
    resp = session.post(f"{BASE}:runQuery", json=query)
    results = resp.json()
    
    questions = []
    for doc in results:
        if "document" in doc:
            fields = doc["document"]["fields"]
            questions.append({
                k: v.get("stringValue", v.get("arrayValue", {}).get("values", []))
                for k, v in fields.items()
            })
    
    return json.dumps(questions, indent=2)


def store_session(user_id: str, question: str, user_answer: str, score: int,
                  feedback: dict, category: str) -> str:
    """Store a practice session result in Firestore."""
    session = _get_session()
    doc = {
        "fields": {
            "user_id": {"stringValue": user_id},
            "timestamp": {"stringValue": datetime.utcnow().isoformat()},
            "question": {"stringValue": question},
            "user_answer": {"stringValue": user_answer},
            "score": {"integerValue": str(score)},
            "feedback": {"stringValue": json.dumps(feedback)},
            "category": {"stringValue": category},
        }
    }
    resp = session.post(f"{BASE}/sessions", json=doc)
    return f"Session stored: {resp.status_code}"


def get_progress(user_id: str) -> str:
    """Get user's practice progress from Firestore."""
    session = _get_session()
    query = {
        "structuredQuery": {
            "from": [{"collectionId": "sessions"}],
            "where": {
                "fieldFilter": {
                    "field": {"fieldPath": "user_id"},
                    "op": "EQUAL",
                    "value": {"stringValue": user_id}
                }
            },
            "orderBy": [{"field": {"fieldPath": "timestamp"}, "direction": "DESCENDING"}],
            "limit": 50,
        }
    }
    resp = session.post(f"{BASE}:runQuery", json=query)
    results = resp.json()
    
    sessions = []
    for doc in results:
        if "document" in doc:
            fields = doc["document"]["fields"]
            sessions.append({
                "score": int(fields.get("score", {}).get("integerValue", "0")),
                "category": fields.get("category", {}).get("stringValue", ""),
                "timestamp": fields.get("timestamp", {}).get("stringValue", ""),
            })
    
    # Calculate stats
    if not sessions:
        return json.dumps({"message": "No practice sessions yet. Start practicing!"})
    
    by_category = {}
    for s in sessions:
        cat = s["category"]
        if cat not in by_category:
            by_category[cat] = []
        by_category[cat].append(s["score"])
    
    stats = {
        "total_sessions": len(sessions),
        "category_averages": {cat: round(sum(scores)/len(scores), 1) for cat, scores in by_category.items()},
        "overall_average": round(sum(s["score"] for s in sessions) / len(sessions), 1),
        "recent_sessions": sessions[:5],
    }
    
    return json.dumps(stats, indent=2)


def store_plan(user_id: str, plan: dict) -> str:
    """Store a study plan in Firestore."""
    session = _get_session()
    doc = {
        "fields": {
            "user_id": {"stringValue": user_id},
            "plan": {"stringValue": json.dumps(plan)},
            "created_at": {"stringValue": datetime.utcnow().isoformat()},
        }
    }
    resp = session.post(f"{BASE}/plans", json=doc)
    return f"Plan stored: {resp.status_code}"
