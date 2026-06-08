"""
Seed the MongoDB database with initial interview questions.
Run this once to populate the question bank.
"""

import os
from pymongo import MongoClient
from datetime import datetime

MONGODB_URI = os.environ.get(
    "MONGODB_URI",
    "mongodb+srv://prepagent:PrepAgent2026@cluster0.mongodb.net/prepagent"
)

QUESTIONS = [
    # Behavioral
    {
        "category": "behavioral",
        "difficulty": "easy",
        "role": "software-engineer",
        "company": "general",
        "question": "Tell me about a time you had to work with a difficult team member. How did you handle it?",
        "hints": ["Use the STAR method", "Focus on the resolution", "Show empathy"],
        "sample_answer": "In my previous role, I worked with a team member who consistently missed deadlines, affecting our sprint velocity. I scheduled a private 1:1 to understand their challenges. I discovered they were overwhelmed with unclear requirements. I proposed we pair on task breakdown, which improved their delivery by 40% within two sprints. The key was approaching it with curiosity rather than frustration.",
        "tags": ["teamwork", "conflict-resolution", "communication"],
    },
    {
        "category": "behavioral",
        "difficulty": "medium",
        "role": "software-engineer",
        "company": "general",
        "question": "Describe a situation where you had to make a technical decision with incomplete information. What was the outcome?",
        "hints": ["Show your decision-making framework", "Discuss risk mitigation", "Mention what you learned"],
        "sample_answer": "During a production incident, we needed to decide between a quick hotfix and a more thorough solution. With limited data on root cause, I chose to implement a feature flag to disable the problematic feature while we investigated. This reduced impact to 5% of users instead of 100%. We then had 48 hours to find and fix the root cause properly. I learned that having escape hatches built into features is invaluable.",
        "tags": ["decision-making", "risk-management", "production"],
    },
    {
        "category": "behavioral",
        "difficulty": "hard",
        "role": "software-engineer",
        "company": "google",
        "question": "Tell me about a time you led a project that failed. What did you learn and what would you do differently?",
        "hints": ["Be honest about the failure", "Show self-awareness", "Demonstrate growth"],
        "sample_answer": "I led a migration from a monolith to microservices that we had to roll back after 3 months. The failure came from underestimating data consistency requirements across services. I should have: 1) done a proof-of-concept with the most complex service first, 2) involved the database team earlier, 3) defined clear rollback criteria upfront. This taught me that architectural decisions need more upfront validation and that 'fail fast' should be built into the project plan, not discovered during execution.",
        "tags": ["leadership", "failure", "learning", "architecture"],
    },
    # Technical
    {
        "category": "technical",
        "difficulty": "easy",
        "role": "software-engineer",
        "company": "general",
        "question": "Explain the difference between a stack and a queue. When would you use each?",
        "hints": ["LIFO vs FIFO", "Real-world analogies", "Common use cases"],
        "sample_answer": "A stack is LIFO (Last In, First Out) — like a stack of plates. A queue is FIFO (First In, First Out) — like a line at a store. Use stacks for: undo operations, parsing expressions, DFS traversal, function call management. Use queues for: BFS traversal, task scheduling, message buffers, print job management. The choice depends on whether you need to process the most recent item (stack) or the oldest item (queue) first.",
        "tags": ["data-structures", "fundamentals"],
    },
    {
        "category": "technical",
        "difficulty": "medium",
        "role": "software-engineer",
        "company": "general",
        "question": "What is the CAP theorem? How does it affect your choice of database?",
        "hints": ["Consistency, Availability, Partition tolerance", "Trade-offs", "Real examples"],
        "sample_answer": "CAP theorem states that in a distributed system, you can only guarantee two of three: Consistency (all nodes see the same data), Availability (every request gets a response), and Partition tolerance (system works despite network failures). Since network partitions are inevitable, the real choice is between CP (consistent but may be unavailable, like MongoDB with write concern majority) and AP (available but eventually consistent, like Cassandra). For financial transactions, I'd choose CP. For social media feeds, AP is acceptable.",
        "tags": ["distributed-systems", "databases", "theory"],
    },
    {
        "category": "technical",
        "difficulty": "hard",
        "role": "software-engineer",
        "company": "meta",
        "question": "Design a rate limiter that works across multiple servers. What algorithms would you consider and what are their trade-offs?",
        "hints": ["Token bucket vs sliding window", "Distributed coordination", "Redis-based solutions"],
        "sample_answer": "I'd consider: 1) Token Bucket — allows bursts, simple to implement, but hard to synchronize across servers. 2) Sliding Window Log — most accurate, but memory-intensive as it stores every request timestamp. 3) Sliding Window Counter — good balance of accuracy and memory. For distributed: use Redis with atomic operations (MULTI/EXEC). The key design decisions are: per-user vs per-endpoint limits, handling race conditions with Lua scripts in Redis, and graceful degradation when Redis is down (local rate limiting fallback). I'd choose sliding window counter with Redis for most use cases — O(1) memory per user and ~95% accuracy.",
        "tags": ["system-design", "distributed-systems", "algorithms"],
    },
    # System Design
    {
        "category": "system-design",
        "difficulty": "medium",
        "role": "software-engineer",
        "company": "general",
        "question": "Design a URL shortener like bit.ly. Walk me through your approach.",
        "hints": ["Start with requirements", "Think about scale", "Consider the encoding"],
        "sample_answer": "Requirements: shorten URLs, redirect quickly, analytics, custom aliases. Scale: 100M URLs/month, 10:1 read:write ratio. Architecture: 1) Encoding service generates 7-char base62 codes (62^7 = 3.5T combinations). 2) Write path: check uniqueness in DB, store mapping, return short URL. 3) Read path: lookup code in cache (Redis) → DB fallback → 301 redirect. 4) Storage: NoSQL (DynamoDB) for key-value lookups at scale. 5) Cache: Redis with LRU eviction for hot URLs. 6) Analytics: async event stream to Kafka → aggregate in data warehouse. Trade-offs: 301 (cacheable, less analytics) vs 302 (not cached, better tracking).",
        "tags": ["url-shortener", "caching", "encoding"],
    },
    {
        "category": "system-design",
        "difficulty": "hard",
        "role": "software-engineer",
        "company": "google",
        "question": "Design a real-time collaborative document editor like Google Docs.",
        "hints": ["OT vs CRDT", "Conflict resolution", "Presence system"],
        "sample_answer": "Core challenge: multiple users editing simultaneously. Two approaches: 1) Operational Transformation (OT) — transform operations against concurrent edits. Used by Google Docs. Requires a central server. 2) CRDTs (Conflict-free Replicated Data Types) — mathematically guaranteed convergence. Better for P2P. Architecture: WebSocket connections for real-time sync, operation log for history, presence service for cursors. Document stored as operation log + periodic snapshots. Conflict resolution: each character has a unique position ID (like Logoot), insertions between IDs. Scale: shard by document, replicate for availability. Undo: maintain per-user operation stacks, transform undo operations against concurrent edits.",
        "tags": ["collaboration", "real-time", "distributed-systems"],
    },
    # Coding
    {
        "category": "coding",
        "difficulty": "easy",
        "role": "software-engineer",
        "company": "general",
        "question": "Given an array of integers, find two numbers that add up to a specific target. Return their indices.",
        "hints": ["Hash map for O(n) solution", "Consider edge cases", "What if no solution exists?"],
        "sample_answer": "Use a hash map to store complement values. For each number, check if target - number exists in the map. Time: O(n), Space: O(n).\n\ndef two_sum(nums, target):\n    seen = {}\n    for i, num in enumerate(nums):\n        complement = target - num\n        if complement in seen:\n            return [seen[complement], i]\n        seen[num] = i\n    return []",
        "tags": ["arrays", "hash-map", "two-pointers"],
    },
    {
        "category": "coding",
        "difficulty": "medium",
        "role": "software-engineer",
        "company": "general",
        "question": "Implement a function to detect if a linked list has a cycle. Can you do it in O(1) space?",
        "hints": ["Floyd's cycle detection", "Two pointers", "Fast and slow"],
        "sample_answer": "Use Floyd's Tortoise and Hare algorithm. Two pointers: slow moves 1 step, fast moves 2 steps. If they meet, there's a cycle. Time: O(n), Space: O(1).\n\ndef has_cycle(head):\n    slow = fast = head\n    while fast and fast.next:\n        slow = slow.next\n        fast = fast.next.next\n        if slow == fast:\n            return True\n    return False\n\nTo find the cycle start: after detection, reset one pointer to head and move both at speed 1 until they meet again.",
        "tags": ["linked-list", "two-pointers", "cycle-detection"],
    },
    # Data Science specific
    {
        "category": "technical",
        "difficulty": "medium",
        "role": "data-scientist",
        "company": "general",
        "question": "Explain the bias-variance tradeoff. How do you handle it in practice?",
        "hints": ["Underfitting vs overfitting", "Model complexity", "Regularization"],
        "sample_answer": "Bias = error from simplifying assumptions (underfitting). Variance = error from sensitivity to training data (overfitting). Total error = bias² + variance + irreducible noise. In practice: 1) Start simple (high bias), gradually increase complexity. 2) Use cross-validation to detect overfitting. 3) Regularization (L1/L2) to control variance. 4) Ensemble methods: bagging reduces variance (Random Forest), boosting reduces bias (XGBoost). 5) More data reduces variance. The sweet spot minimizes total error — I typically plot train/validation learning curves to find it.",
        "tags": ["machine-learning", "statistics", "model-selection"],
    },
]


def seed():
    client = MongoClient(MONGODB_URI)
    db = client["prepagent"]
    
    # Seed questions
    questions = db["questions"]
    existing = questions.count_documents({})
    if existing > 0:
        print(f"Already have {existing} questions. Skipping seed.")
        return
    
    for q in QUESTIONS:
        q["created_at"] = datetime.utcnow().isoformat()
    
    result = questions.insert_many(QUESTIONS)
    print(f"Seeded {len(result.inserted_ids)} questions")
    
    # Create indexes
    questions.create_index("category")
    questions.create_index("difficulty")
    questions.create_index("role")
    questions.create_index("tags")
    print("Created indexes")
    
    # Initialize empty progress collection
    db["progress"].create_index("user_id", unique=True)
    db["sessions"].create_index([("user_id", 1), ("timestamp", -1)])
    db["plans"].create_index("user_id")
    print("Initialized collections")
    
    client.close()
    print("Done!")


if __name__ == "__main__":
    seed()
