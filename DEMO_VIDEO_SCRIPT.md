# PrepAgent Demo Video Script
## Google Cloud Rapid Agent Hackathon, MongoDB Track
Target length: 2-3 minutes
Format: Screen recording with voiceover (or text overlays)

---

## SHOT LIST & SCRIPT

### INTRO (0:00 - 0:15)
Screen: Title card or PrepAgent landing page
Script:
> "This is PrepAgent, an AI interview coaching agent I built with Google's Agent Development Kit, Gemini 2.5 Flash, and MongoDB Atlas. It lets you practice interviews, get scored on your answers, track your progress over time, and build a study plan."

---

### ACT 1: Starting a practice session (0:15 - 0:45)
Screen: Open https://prepagent-k3mbjwurja-uc.a.run.app
Actions:
1. Show the chat UI (dark theme, quick action buttons)
2. Click "Practice for Google SWE" button
3. Agent responds with a tailored interview question

Script:
> "PrepAgent runs on Cloud Run with a simple chat interface. You pick a role and company. Here I'll practice for a Google Software Engineer interview. The agent pulls questions from MongoDB Atlas using aggregation pipelines and the $sample operator so you get a random, relevant question each time."

---

### ACT 2: Getting evaluated (0:45 - 1:15)
Screen: Type an answer to the question
Actions:
1. Type a realistic answer (doesn't need to be perfect, the evaluation is the point)
2. Agent scores the answer with detailed feedback

Script:
> "After I answer, the Answer Evaluator sub-agent scores my response on completeness, technical depth, and communication clarity. It checks whether I used the STAR method and gives specific feedback on what to improve."

Suggested answer to type:
> "I would start by clarifying the requirements with the interviewer, then design a high-level architecture. For scalability, I'd consider load balancing and horizontal scaling. I'd use a database like MongoDB for flexible schema design."

---

### ACT 3: Tracking progress (1:15 - 1:40)
Screen: Continue in chat
Actions:
1. Type "Show my progress" or click the progress button
2. Agent shows session history and performance trends from MongoDB

Script:
> "PrepAgent stores every practice session in MongoDB: scores, categories, timestamps. The Progress Tracker sub-agent runs aggregation pipelines with $group and $avg to find trends. You can see which categories you're strong in and where you still need work."

---

### ACT 4: Study plan (1:40 - 2:05)
Screen: Continue in chat
Actions:
1. Type "Create a study plan for Amazon SDE interview in 2 weeks"
2. Agent generates a personalized plan and saves it to MongoDB

Script:
> "The Study Planner sub-agent creates prep schedules based on your target role, timeline, and weak areas. Plans get saved to MongoDB using upsert operations so they stay up to date."

---

### ACT 5: Architecture overview (2:05 - 2:30)
Screen: Show the architecture diagram from the README (or a quick slide)
Script:
> "Under the hood, PrepAgent uses Google ADK to run four sub-agents, each with access to eight MongoDB tool functions. These tools use $facet for multi-dimensional stats, $sample for random selection, aggregation pipelines for progress analytics, and upserts for study plan management. Everything runs on Gemini 2.5 Flash through Vertex AI, deployed on Cloud Run."

---

### CLOSING (2:30 - 2:45)
Screen: Back to the app / GitHub repo
Script:
> "That's PrepAgent. Interview prep powered by Google Cloud and MongoDB Atlas. Try it live or check out the code on GitHub."

Show URLs:
- Live: https://prepagent-k3mbjwurja-uc.a.run.app
- Code: https://github.com/hajirufai/prepagent

---

## RECORDING TIPS

1. Screen resolution: 1920x1080, browser at ~90% zoom so text is readable
2. Use Chrome, clear other tabs, use incognito for a clean look
3. Record voiceover separately in a quiet room, or use text overlays instead
4. Don't rush. Let the AI responses load naturally so it's clear the demo is live
5. Cut any long loading pauses down to 2-3 seconds max in editing
6. Background music is optional; keep it low volume if you add it

## TOOLS FOR RECORDING
- Screen recording: OBS Studio (free), QuickTime (Mac), or Loom
- Video editing: iMovie, CapCut, or DaVinci Resolve (all free)
- If you skip voiceover, use large text overlays to explain each section

## KEY POINTS TO HIT (judges care about these)
- MongoDB integration goes beyond CRUD: aggregation pipelines, $sample, $facet, upserts
- Multi-agent architecture: 4 sub-agents coordinated through Google ADK
- Working live demo, deployed on Cloud Run, publicly accessible
- Solves a real problem (interview prep) with clear practical value
