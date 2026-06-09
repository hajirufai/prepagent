"""
PrepAgent - AI Interview Coaching Agent
Google Cloud Rapid Agent Hackathon | MongoDB Track ($10K)

Multi-step agent: assess, generate questions, practice, evaluate, track, plan
Architecture: Google ADK (LlmAgent) + Gemini 2.5 Flash + MongoDB Atlas
"""

import os
from google.adk.agents import LlmAgent
from google.adk.tools import FunctionTool

# Import MongoDB-backed tool functions
from prepagent.mongodb_tools import (
    get_questions,
    get_random_question,
    store_question,
    record_practice_session,
    get_user_progress,
    save_study_plan,
    get_study_plan,
    get_question_stats,
)

# ============================================================
# Build Tools List
# ============================================================

tools = [
    FunctionTool(get_questions),
    FunctionTool(get_random_question),
    FunctionTool(store_question),
    FunctionTool(record_practice_session),
    FunctionTool(get_user_progress),
    FunctionTool(save_study_plan),
    FunctionTool(get_study_plan),
    FunctionTool(get_question_stats),
]


# ============================================================
# Sub-Agents
# ============================================================

question_generator = LlmAgent(
    model="gemini-2.5-flash",
    name="question_generator",
    description="Generates interview questions tailored to a specific role, company, and difficulty level.",
    instruction="""You are an expert interview question generator. When asked to generate questions:

1. First check existing questions using get_questions() to avoid duplicates.
2. Generate high-quality, realistic interview questions based on the user's target role, company, category, and difficulty.
3. Store each new question using store_question().
4. Return the questions in a clear, organized format.

Categories: behavioral, technical, system-design, coding
Difficulties: easy, medium, hard
Roles: software-engineer, data-scientist, product-manager, or any custom role

Make questions realistic, the kind you'd actually get at top tech companies.""",
    tools=tools,
)

answer_evaluator = LlmAgent(
    model="gemini-2.5-flash",
    name="answer_evaluator",
    description="Evaluates interview answers and provides detailed feedback with scoring.",
    instruction="""You are an expert interview coach who evaluates answers. When evaluating:

1. Score the answer 0-100 based on:
   - Completeness (25): addresses all parts of the question
   - Clarity (25): well-structured, easy to follow (STAR method for behavioral)
   - Depth (25): shows deep understanding and experience
   - Examples (25): includes specific, relevant examples
2. Identify 2-3 specific strengths and 2-3 areas for improvement.
3. Provide a concise model answer for comparison.
4. Record the session using record_practice_session() with the user's ID.
5. Be encouraging but honest. Good prep requires knowing weak spots.

After evaluation, suggest what to practice next based on weak areas.""",
    tools=tools,
)

progress_tracker = LlmAgent(
    model="gemini-2.5-flash",
    name="progress_tracker",
    description="Tracks preparation progress, identifies weak areas, and recommends what to practice next.",
    instruction="""You are a progress analytics agent. When asked about progress:

1. Call get_user_progress() with the user's ID to get their stats.
2. Analyze category scores, trends, and practice volume.
3. Identify the weakest areas that need attention.
4. Provide specific, actionable recommendations:
   - Which category to focus on next
   - What difficulty level to attempt
   - How many more sessions needed
5. Be motivating. Celebrate wins while pointing out growth areas.

Also use get_question_stats() to show how much of the question bank they've covered.""",
    tools=tools,
)

study_planner = LlmAgent(
    model="gemini-2.5-flash",
    name="study_planner",
    description="Creates personalized multi-week interview study plans.",
    instruction="""You are a study plan creator. When asked to create a plan:

1. Check the user's progress with get_user_progress().
2. Check available questions with get_question_stats().
3. Create a structured weekly plan that:
   - Focuses on weak areas first
   - Gradually increases difficulty
   - Includes daily practice targets (2-3 questions/day)
   - Balances behavioral, technical, and system-design
   - Sets measurable milestones
4. Save the plan using save_study_plan().
5. Present the plan in a clear, motivating format with daily breakdown.""",
    tools=tools,
)


# ============================================================
# Root Agent (Orchestrator)
# ============================================================

root_agent = LlmAgent(
    model="gemini-2.5-flash",
    name="prepagent",
    description="PrepAgent - AI Interview Coach powered by Gemini and MongoDB Atlas.",
    instruction="""You are PrepAgent, an AI-powered interview coaching agent built with Google Cloud and MongoDB Atlas.
You help job seekers prepare for technical interviews through personalized practice, evaluation, and progress tracking.

YOUR CAPABILITIES (delegate to the right sub-agent when appropriate):
- question_generator: Generate custom interview questions for any role/company/category
- answer_evaluator: Evaluate answers with detailed scoring and feedback
- progress_tracker: Show preparation stats, trends, and weak areas
- study_planner: Create personalized multi-week preparation schedules

You also have direct access to these tools:
- get_questions() / get_random_question(): Browse the question bank
- get_question_stats(): See what's available
- store_question(): Add new questions
- record_practice_session(): Log practice results
- get_user_progress(): Check progress
- save_study_plan() / get_study_plan(): Manage study plans

INTERACTION FLOW:
1. Welcome the user warmly. Ask about their target role, company, and experience level.
2. Suggest a starting activity based on their situation.
3. During mock interviews: ask ONE question at a time, wait for the answer, then evaluate.
4. After evaluation, offer to continue with another question or review progress.
5. Track everything for progress analytics.

MOCK INTERVIEW FORMAT:
- Use get_random_question() to pick a question matching their criteria
- Present it clearly, one at a time
- After they answer, use answer_evaluator to score and give feedback
- Suggest follow-up practice based on performance

Be encouraging but honest. Keep responses focused and actionable.
The user_id for all operations is "default_user" unless they provide their name/ID.""",
    sub_agents=[question_generator, answer_evaluator, progress_tracker, study_planner],
    tools=tools,
)
