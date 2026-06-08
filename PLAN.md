# Google Cloud Rapid Agent Hackathon — Build Plan

## Track: MongoDB ($10K = $5K/$3K/$2K)

## Concept: "PrepAgent" — AI Interview Coaching Agent
An AI-powered agent that helps job seekers prepare for technical interviews through personalized practice, question generation, answer evaluation, and progress tracking.

**Real-world problem:** Candidates fail interviews not because they lack knowledge, but because they don't practice the RIGHT questions for their target role/company. PrepAgent solves this with AI-powered personalized prep.

## Architecture
```
User (Web UI) ←→ Google ADK Agent (Gemini 2.5 Flash)
                        ↓
                  MongoDB MCP Server
                        ↓
                  MongoDB Atlas (Free Tier)
                    ├── questions (curated question bank)
                    ├── sessions (practice history)
                    ├── progress (user analytics)
                    └── plans (study plans)
```

## Core Agent Capabilities (Multi-Step)
1. **Assess** — Ask about target role, company, experience level → query MongoDB for relevant questions
2. **Generate** — Use Gemini to generate custom questions based on role/company
3. **Practice** — Conduct mock interview, evaluate answers, store results in MongoDB
4. **Track** — Query MongoDB for progress data, identify weak areas, adjust study plan
5. **Recommend** — Based on historical performance, suggest focus areas and next practice topics

## Tech Stack
- **Agent Framework:** Google ADK (Agent Development Kit) with LlmAgent
- **LLM:** Gemini 2.5 Flash on Vertex AI (us-central1)
- **MCP Integration:** mongodb-mcp-server (npm package) via McpToolset
- **Database:** MongoDB Atlas (free M0 cluster)
- **Frontend:** Streamlit or FastAPI + simple HTML (quick to build)
- **Deployment:** Cloud Run or local with tunneling
- **Demo Video:** ~3 min screen recording

## Submission Requirements Checklist
- [ ] Hosted URL (running web app)
- [ ] Public GitHub repo with open source license (MIT)
- [ ] ~3 minute demo video
- [ ] Devpost submission form
- [ ] MongoDB partner track selected

## Timeline (3 days)
### Day 1 (June 8) — Foundation
- [ ] Create GitHub repo
- [ ] Set up MongoDB Atlas (free cluster)
- [ ] Seed question bank data
- [ ] Set up ADK project structure
- [ ] Get basic agent working with MongoDB MCP

### Day 2 (June 9) — Core Features
- [ ] Build multi-step interview flow
- [ ] Implement answer evaluation
- [ ] Add progress tracking
- [ ] Build web UI (Streamlit/FastAPI)

### Day 3 (June 10) — Polish & Submit
- [ ] Deploy to Cloud Run
- [ ] Record 3-min demo video
- [ ] Write README and docs
- [ ] Register on Devpost
- [ ] Submit before deadline (June 11)

## MongoDB Schema Design
```json
// questions collection
{
  "_id": ObjectId,
  "category": "behavioral|technical|system-design|coding",
  "difficulty": "easy|medium|hard",
  "roles": ["software-engineer", "data-scientist", ...],
  "companies": ["google", "meta", ...],
  "question": "...",
  "hints": ["..."],
  "sample_answer": "...",
  "tags": ["arrays", "dynamic-programming", ...]
}

// sessions collection  
{
  "_id": ObjectId,
  "user_id": "...",
  "timestamp": ISODate,
  "questions_asked": [{ question_id, user_answer, score, feedback }],
  "overall_score": 0-100,
  "duration_minutes": 30
}

// progress collection
{
  "_id": ObjectId,
  "user_id": "...",
  "category_scores": { "behavioral": 72, "technical": 58, ... },
  "weak_areas": ["system-design", "concurrency"],
  "sessions_completed": 15,
  "streak_days": 3
}
```

## Key Differentiation
- NOT just a chatbot — agent DOES things (creates study plans, tracks progress, adapts)
- Multi-step workflow with real tool use (MongoDB operations)
- Meaningful MCP integration (reads/writes to MongoDB through MCP server)
- Solves a genuine problem millions face
