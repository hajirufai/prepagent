"""
MongoDB-backed tools for PrepAgent.
Primary data layer using MongoDB Atlas via pymongo.
Replaces Firestore for the Google Cloud Rapid Agent Hackathon — MongoDB Track.
"""

import os
import json
from datetime import datetime, timezone
from typing import Optional
from bson import ObjectId
from pymongo import MongoClient

MONGODB_URI = os.environ.get(
    "MONGODB_URI",
    "mongodb+srv://prepagent:PrepAgent2026!Hackathon@prepagentcluster.z1ydauh.mongodb.net/?retryWrites=true&w=majority"
)

_client = None
_db = None

def _get_db():
    """Get MongoDB database connection (lazy singleton)."""
    global _client, _db
    if _db is None:
        _client = MongoClient(MONGODB_URI, serverSelectionTimeoutMS=10000)
        _db = _client["prepagent"]
    return _db


def get_questions(category: Optional[str] = None, difficulty: Optional[str] = None,
                  role: Optional[str] = None, limit: int = 10) -> dict:
    """Retrieve interview questions from MongoDB with optional filters.

    Args:
        category: Filter by category (behavioral, technical, system-design, coding). Optional.
        difficulty: Filter by difficulty (easy, medium, hard). Optional.
        role: Filter by target role (e.g., software-engineer, data-scientist). Optional.
        limit: Maximum number of questions to return. Default 10.

    Returns:
        Dictionary with list of matching questions and count.
    """
    db = _get_db()
    query = {}
    if category:
        query["category"] = category
    if difficulty:
        query["difficulty"] = difficulty
    if role:
        query["role"] = role

    cursor = db.questions.find(query, {"_id": 0}).limit(limit)
    questions = list(cursor)
    return {"questions": questions, "count": len(questions)}


def get_random_question(category: Optional[str] = None, difficulty: Optional[str] = None,
                        role: Optional[str] = None) -> dict:
    """Get a single random interview question, optionally filtered.

    Args:
        category: Filter by category. Optional.
        difficulty: Filter by difficulty. Optional.
        role: Filter by target role. Optional.

    Returns:
        A single random question or message if none found.
    """
    db = _get_db()
    pipeline = []
    match = {}
    if category:
        match["category"] = category
    if difficulty:
        match["difficulty"] = difficulty
    if role:
        match["role"] = role
    if match:
        pipeline.append({"$match": match})
    pipeline.append({"$sample": {"size": 1}})
    pipeline.append({"$project": {"_id": 0}})

    results = list(db.questions.aggregate(pipeline))
    if results:
        return {"question": results[0]}
    return {"message": "No questions found matching your criteria. Try broader filters."}


def store_question(category: str, difficulty: str, role: str, question: str,
                   hints: str, sample_answer: str, tags: str,
                   company: str = "general") -> dict:
    """Store a new interview question in MongoDB.

    Args:
        category: Question category (behavioral, technical, system-design, coding).
        difficulty: Difficulty level (easy, medium, hard).
        role: Target role (e.g., software-engineer, data-scientist).
        question: The full interview question text.
        hints: Comma-separated hints for answering.
        sample_answer: A model answer for reference.
        tags: Comma-separated topic tags.
        company: Target company or 'general'. Default: general.

    Returns:
        Confirmation with the stored question ID.
    """
    db = _get_db()
    doc = {
        "category": category,
        "difficulty": difficulty,
        "role": role,
        "company": company,
        "question": question,
        "hints": [h.strip() for h in hints.split(",")],
        "sample_answer": sample_answer,
        "tags": [t.strip() for t in tags.split(",")],
        "created_at": datetime.now(timezone.utc).isoformat(),
    }
    result = db.questions.insert_one(doc)
    return {"status": "stored", "id": str(result.inserted_id)}


def record_practice_session(user_id: str, question: str, user_answer: str,
                            score: int, strengths: str, improvements: str,
                            model_answer: str, category: str) -> dict:
    """Record a completed practice session with evaluation results in MongoDB.

    Args:
        user_id: The user's identifier.
        question: The interview question that was asked.
        user_answer: The user's answer text.
        score: Score from 0-100.
        strengths: Comma-separated list of strengths in the answer.
        improvements: Comma-separated list of areas for improvement.
        model_answer: An ideal answer for comparison.
        category: The question category.

    Returns:
        Confirmation with session ID.
    """
    db = _get_db()
    doc = {
        "user_id": user_id,
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "question": question,
        "user_answer": user_answer,
        "score": score,
        "strengths": [s.strip() for s in strengths.split(",")],
        "improvements": [i.strip() for i in improvements.split(",")],
        "model_answer": model_answer,
        "category": category,
    }
    result = db.sessions.insert_one(doc)
    return {"status": "recorded", "session_id": str(result.inserted_id)}


def get_user_progress(user_id: str) -> dict:
    """Get a user's interview preparation progress and statistics from MongoDB.

    Uses MongoDB aggregation pipeline for analytics.

    Args:
        user_id: The user's identifier.

    Returns:
        Dictionary with progress stats including category scores, trends, and recommendations.
    """
    db = _get_db()

    # Aggregation pipeline for category stats
    pipeline = [
        {"$match": {"user_id": user_id}},
        {"$group": {
            "_id": "$category",
            "avg_score": {"$avg": "$score"},
            "count": {"$sum": 1},
            "max_score": {"$max": "$score"},
            "min_score": {"$min": "$score"},
        }},
        {"$sort": {"avg_score": 1}},
    ]
    cat_stats = list(db.sessions.aggregate(pipeline))

    if not cat_stats:
        return {
            "message": "No practice sessions yet. Start practicing to see your progress!",
            "total_sessions": 0,
        }

    # Overall stats
    overall = db.sessions.aggregate([
        {"$match": {"user_id": user_id}},
        {"$group": {
            "_id": None,
            "total": {"$sum": 1},
            "avg_score": {"$avg": "$score"},
            "max_score": {"$max": "$score"},
        }},
    ])
    overall_stats = list(overall)[0]

    # Recent sessions
    recent = list(
        db.sessions.find(
            {"user_id": user_id},
            {"_id": 0, "score": 1, "category": 1, "timestamp": 1, "question": 1}
        ).sort("timestamp", -1).limit(5)
    )

    category_averages = {s["_id"]: round(s["avg_score"], 1) for s in cat_stats}
    weakest = cat_stats[0]["_id"] if cat_stats else None
    strongest = cat_stats[-1]["_id"] if cat_stats else None

    return {
        "total_sessions": overall_stats["total"],
        "overall_average": round(overall_stats["avg_score"], 1),
        "best_score": overall_stats["max_score"],
        "category_averages": category_averages,
        "category_details": {
            s["_id"]: {"avg": round(s["avg_score"], 1), "count": s["count"],
                       "best": s["max_score"], "worst": s["min_score"]}
            for s in cat_stats
        },
        "weakest_category": weakest,
        "strongest_category": strongest,
        "recent_sessions": recent,
    }


def save_study_plan(user_id: str, target_role: str, target_company: str,
                    duration_weeks: int, plan_json: str) -> dict:
    """Save a personalized study plan for the user in MongoDB.

    Args:
        user_id: The user's identifier.
        target_role: The role they're preparing for.
        target_company: The target company or 'general'.
        duration_weeks: Plan duration in weeks.
        plan_json: JSON string of the weekly schedule and milestones.

    Returns:
        Confirmation message.
    """
    db = _get_db()
    doc = {
        "user_id": user_id,
        "target_role": target_role,
        "target_company": target_company,
        "duration_weeks": duration_weeks,
        "plan": plan_json,
        "created_at": datetime.now(timezone.utc).isoformat(),
        "status": "active",
    }
    # Upsert — replace existing plan for this user
    result = db.plans.update_one(
        {"user_id": user_id},
        {"$set": doc},
        upsert=True
    )
    return {"status": "saved", "upserted": result.upserted_id is not None}


def get_study_plan(user_id: str) -> dict:
    """Retrieve the user's current study plan from MongoDB.

    Args:
        user_id: The user's identifier.

    Returns:
        The study plan or a message if none exists.
    """
    db = _get_db()
    plan = db.plans.find_one({"user_id": user_id}, {"_id": 0})
    if plan:
        return plan
    return {"message": "No study plan found. Ask me to create one for you!"}


def get_question_stats() -> dict:
    """Get statistics about the question bank in MongoDB.

    Returns:
        Dictionary with question counts by category, difficulty, and role.
    """
    db = _get_db()
    pipeline = [
        {"$facet": {
            "by_category": [
                {"$group": {"_id": "$category", "count": {"$sum": 1}}}
            ],
            "by_difficulty": [
                {"$group": {"_id": "$difficulty", "count": {"$sum": 1}}}
            ],
            "by_role": [
                {"$group": {"_id": "$role", "count": {"$sum": 1}}}
            ],
            "total": [
                {"$count": "count"}
            ],
        }}
    ]
    result = list(db.questions.aggregate(pipeline))[0]
    return {
        "total": result["total"][0]["count"] if result["total"] else 0,
        "by_category": {r["_id"]: r["count"] for r in result["by_category"]},
        "by_difficulty": {r["_id"]: r["count"] for r in result["by_difficulty"]},
        "by_role": {r["_id"]: r["count"] for r in result["by_role"]},
    }
