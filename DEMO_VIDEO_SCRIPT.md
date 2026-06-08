# PrepAgent Demo Video Script
## Google Cloud Rapid Agent Hackathon — MongoDB Track
**Target length:** 2-3 minutes
**Format:** Screen recording with voiceover (or text overlays)

---

## SHOT LIST & SCRIPT

### INTRO (0:00 - 0:15)
**Screen:** Title card or PrepAgent landing page
**Script:**
> "Meet PrepAgent — an AI-powered interview coaching agent built with Google's Agent Development Kit, Gemini 2.5 Flash, and MongoDB Atlas. It helps job seekers practice interviews, get scored, track progress, and build personalized study plans."

---

### ACT 1: Starting a Practice Session (0:15 - 0:45)
**Screen:** Open https://prepagent-k3mbjwurja-uc.a.run.app
**Actions:**
1. Show the chat UI — dark theme, quick action buttons
2. Click **"Practice for Google SWE"** button
3. Agent responds with a tailored interview question

**Script:**
> "PrepAgent runs on Cloud Run and uses a chat interface. You can pick a role and company — here I'll practice for a Google Software Engineer interview. The agent pulls questions from MongoDB Atlas using aggregation pipelines and the $sample operator to serve random, relevant questions."

---

### ACT 2: Getting Evaluated (0:45 - 1:15)
**Screen:** Type an answer to the question
**Actions:**
1. Type a realistic answer (doesn't need to be perfect — showing the evaluation is the point)
2. Agent scores the answer with detailed feedback

**Script:**
> "Once I answer, the Answer Evaluator sub-agent scores my response across multiple dimensions — completeness, technical depth, communication clarity. It uses the STAR method framework and gives specific, actionable feedback on how to improve."

**Suggested answer to type:**
> "I would start by clarifying the requirements with the interviewer, then design a high-level architecture. For scalability, I'd consider load balancing and horizontal scaling. I'd use a database like MongoDB for flexible schema design."

---

### ACT 3: Tracking Progress (1:15 - 1:40)
**Screen:** Continue in chat
**Actions:**
1. Type **"Show my progress"** or click the progress button
2. Agent shows session history and performance trends from MongoDB

**Script:**
> "PrepAgent tracks every practice session in MongoDB — scores, categories, timestamps. The Progress Tracker sub-agent runs aggregation pipelines with $group and $avg to surface trends. You can see which categories you're strong in and where you need work."

---

### ACT 4: Study Plan (1:40 - 2:05)
**Screen:** Continue in chat
**Actions:**
1. Type **"Create a study plan for Amazon SDE interview in 2 weeks"**
2. Agent generates a personalized plan and saves it to MongoDB

**Script:**
> "The Study Planner sub-agent creates personalized prep schedules based on your target role, timeline, and weak areas. Plans are saved to MongoDB using upsert operations so they're always up to date."

---

### ACT 5: Architecture Overview (2:05 - 2:30)
**Screen:** Show the architecture diagram from the README (or a quick slide)
**Script:**
> "Under the hood, PrepAgent uses Google ADK to orchestrate four specialized sub-agents, each with access to eight MongoDB tool functions. These tools use advanced MongoDB features — $facet for multi-dimensional stats, $sample for random selection, aggregation pipelines for progress analytics, and upserts for study plan management. Everything runs on Gemini 2.5 Flash via Vertex AI, deployed on Cloud Run."

---

### CLOSING (2:30 - 2:45)
**Screen:** Back to the app / GitHub repo
**Script:**
> "PrepAgent — making interview prep smarter with Google Cloud and MongoDB Atlas. Try it live or check out the code on GitHub."

**Show URLs:**
- Live: https://prepagent-k3mbjwurja-uc.a.run.app
- Code: https://github.com/hajirufai/prepagent

---

## RECORDING TIPS

1. **Screen resolution:** 1920x1080, browser at ~90% zoom so text is readable
2. **Browser:** Use Chrome, clear other tabs, use incognito for clean look
3. **Voiceover:** Record separately in a quiet room, or use text overlays
4. **Pace:** Don't rush — let the AI responses load naturally, it shows it's real
5. **Edit:** Cut any long loading pauses down to 2-3 seconds max
6. **Music:** Optional — soft background music at low volume

## TOOLS FOR RECORDING
- **Screen recording:** OBS Studio (free), QuickTime (Mac), or Loom
- **Video editing:** iMovie, CapCut, or DaVinci Resolve (all free)
- **If no voiceover:** Use large text overlays explaining each section

## KEY POINTS TO EMPHASIZE (judges care about these)
- ✅ **MongoDB integration depth** — not just CRUD, using aggregation pipelines, $sample, $facet, upserts
- ✅ **Multi-agent architecture** — 4 specialized sub-agents via Google ADK
- ✅ **Working live demo** — deployed on Cloud Run, publicly accessible
- ✅ **Practical use case** — real problem (interview prep) with real value
