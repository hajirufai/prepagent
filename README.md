# PrepAgent — AI Interview Coaching Agent

> Built for the [Google Cloud Rapid Agent Hackathon](https://googlecloud-rapidagent.devpost.com/) | MongoDB Track

**PrepAgent** is an AI-powered interview coaching agent that helps job seekers practice and improve their interview skills. It generates tailored questions, evaluates answers using structured rubrics, tracks progress over time, and creates personalized study plans.

🌐 **Live Demo:** [https://prepagent-k3mbjwurja-uc.a.run.app](https://prepagent-k3mbjwurja-uc.a.run.app)

## What It Does

- **Practice interviews** across behavioral, technical, system design, and coding categories
- **Get scored** with detailed feedback on completeness, depth, and communication
- **Track progress** across sessions with performance trends
- **Generate study plans** tailored to your target role and weak areas
- **Access a growing question bank** stored in MongoDB Atlas

## Architecture

```
┌─────────────────────────────────────────┐
│           PrepAgent (Root Agent)        │
│         Google ADK Orchestrator         │
├─────────┬──────────┬──────────┬─────────┤
│Question │ Answer   │Progress  │ Study   │
│Generator│Evaluator │Tracker   │Planner  │
└────┬────┴────┬─────┴────┬────┴────┬────┘
     │         │          │         │
     └─────────┴──────────┴─────────┘
                    │
            ┌───────┴───────┐
            │ MongoDB Atlas │
            │  (8 Tools)    │
            └───────────────┘
```

**4 Specialized Sub-Agents:**
1. **Question Generator** — Fetches and creates interview questions by category, difficulty, and role
2. **Answer Evaluator** — Scores responses using STAR method rubrics, provides actionable feedback
3. **Progress Tracker** — Records sessions and surfaces performance trends
4. **Study Planner** — Builds personalized prep schedules based on target roles and weak areas

## MongoDB Integration

PrepAgent uses **8 MongoDB tool functions** that demonstrate deep Atlas integration:

| Tool | MongoDB Features Used |
|------|----------------------|
| `get_questions` | `$match`, `$facet`, compound filters |
| `get_random_question` | `$sample` aggregation pipeline |
| `store_question` | `insert_one` with schema validation |
| `record_practice_session` | `insert_one` with embedded scoring documents |
| `get_user_progress` | `$group`, `$avg`, `$sort` aggregation pipeline |
| `save_study_plan` | `update_one` with `upsert=True` |
| `get_study_plan` | `find_one` with projection |
| `get_question_stats` | `$facet` with multiple `$group` pipelines |

**Collections:** `questions`, `practice_sessions`, `study_plans`

## Tech Stack

| Component | Technology |
|-----------|-----------|
| Agent Framework | [Google Agent Development Kit (ADK)](https://google.github.io/adk-docs/) |
| LLM | Gemini 2.5 Flash via Vertex AI |
| Database | MongoDB Atlas (M0, AWS us-east-1) |
| Backend | FastAPI + Uvicorn |
| Deployment | Google Cloud Run |
| Container | Docker (Python 3.12-slim) |

## Getting Started

### Prerequisites
- Python 3.12+
- Google Cloud project with Vertex AI enabled
- MongoDB Atlas cluster

### Local Development

```bash
# Clone the repo
git clone https://github.com/hajirufai/prepagent.git
cd prepagent

# Install dependencies
pip install -r requirements.txt

# Set environment variables
export MONGODB_URI="mongodb+srv://user:pass@cluster.mongodb.net/"
export GOOGLE_CLOUD_PROJECT="your-project-id"
export GOOGLE_CLOUD_LOCATION="us-central1"
export GOOGLE_GENAI_USE_VERTEXAI="TRUE"

# Seed the database
python seed_data.py

# Run locally
uvicorn prepagent.web.app:app --host 0.0.0.0 --port 8080
```

### Deploy to Cloud Run

```bash
gcloud run deploy prepagent \
  --source . \
  --region us-central1 \
  --allow-unauthenticated \
  --set-env-vars "MONGODB_URI=$MONGODB_URI,GOOGLE_CLOUD_PROJECT=$PROJECT,GOOGLE_CLOUD_LOCATION=us-central1,GOOGLE_GENAI_USE_VERTEXAI=TRUE"
```

## Project Structure

```
prepagent/
├── prepagent/
│   ├── __init__.py
│   ├── agent.py          # ADK agent with 4 sub-agents
│   ├── mongodb_tools.py  # 8 MongoDB tool functions
│   └── web/
│       └── app.py        # FastAPI chat UI
├── seed_data.py           # Database seeder (11 questions)
├── Dockerfile
├── requirements.txt
└── README.md
```

## License

MIT
