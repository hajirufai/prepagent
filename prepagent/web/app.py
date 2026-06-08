"""
PrepAgent Web UI — Simple chat interface for the interview coaching agent.
Uses FastAPI with SSE for streaming responses.
"""

import asyncio
import json
import os
import sys
from pathlib import Path

from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, StreamingResponse
from fastapi.staticfiles import StaticFiles

# Add parent to path for agent import
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.genai.types import Content, Part

from prepagent.agent import root_agent

app = FastAPI(title="PrepAgent — AI Interview Coach")
session_service = InMemorySessionService()
runner = Runner(agent=root_agent, app_name="prepagent", session_service=session_service)


HTML_TEMPLATE = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>PrepAgent — AI Interview Coach</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
            background: #0a0a0a;
            color: #e0e0e0;
            height: 100vh;
            display: flex;
            flex-direction: column;
        }
        .header {
            background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%);
            padding: 16px 24px;
            border-bottom: 1px solid #2a2a4a;
            display: flex;
            align-items: center;
            gap: 12px;
        }
        .header h1 {
            font-size: 1.4rem;
            font-weight: 700;
            background: linear-gradient(135deg, #00d2ff, #7b2ff7);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }
        .header .badge {
            font-size: 0.7rem;
            background: #7b2ff7;
            color: white;
            padding: 2px 8px;
            border-radius: 12px;
            font-weight: 600;
        }
        .header .subtitle {
            font-size: 0.85rem;
            color: #888;
            margin-left: auto;
        }
        .chat-container {
            flex: 1;
            overflow-y: auto;
            padding: 24px;
            display: flex;
            flex-direction: column;
            gap: 16px;
        }
        .message {
            max-width: 80%;
            padding: 14px 18px;
            border-radius: 16px;
            line-height: 1.6;
            font-size: 0.95rem;
            white-space: pre-wrap;
        }
        .message.user {
            align-self: flex-end;
            background: linear-gradient(135deg, #7b2ff7, #5b1fd7);
            color: white;
            border-bottom-right-radius: 4px;
        }
        .message.agent {
            align-self: flex-start;
            background: #1a1a2e;
            border: 1px solid #2a2a4a;
            border-bottom-left-radius: 4px;
        }
        .message.agent strong { color: #00d2ff; }
        .message.agent code {
            background: #0d0d1a;
            padding: 2px 6px;
            border-radius: 4px;
            font-size: 0.85rem;
        }
        .typing {
            align-self: flex-start;
            color: #666;
            font-style: italic;
            padding: 8px 18px;
        }
        .input-area {
            padding: 16px 24px;
            background: #111;
            border-top: 1px solid #2a2a4a;
            display: flex;
            gap: 12px;
        }
        .input-area textarea {
            flex: 1;
            background: #1a1a2e;
            border: 1px solid #2a2a4a;
            color: #e0e0e0;
            padding: 12px 16px;
            border-radius: 12px;
            font-size: 0.95rem;
            font-family: inherit;
            resize: none;
            outline: none;
            min-height: 48px;
            max-height: 120px;
        }
        .input-area textarea:focus { border-color: #7b2ff7; }
        .input-area button {
            background: linear-gradient(135deg, #7b2ff7, #00d2ff);
            color: white;
            border: none;
            padding: 12px 24px;
            border-radius: 12px;
            font-weight: 600;
            cursor: pointer;
            font-size: 0.95rem;
            transition: opacity 0.2s;
        }
        .input-area button:hover { opacity: 0.9; }
        .input-area button:disabled { opacity: 0.5; cursor: not-allowed; }
        .welcome {
            text-align: center;
            padding: 60px 20px;
            color: #666;
        }
        .welcome h2 {
            font-size: 1.8rem;
            margin-bottom: 12px;
            background: linear-gradient(135deg, #00d2ff, #7b2ff7);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }
        .welcome p { font-size: 1rem; margin-bottom: 8px; }
        .quick-actions {
            display: flex;
            gap: 8px;
            justify-content: center;
            flex-wrap: wrap;
            margin-top: 20px;
        }
        .quick-actions button {
            background: #1a1a2e;
            border: 1px solid #2a2a4a;
            color: #ccc;
            padding: 8px 16px;
            border-radius: 20px;
            cursor: pointer;
            font-size: 0.85rem;
            transition: all 0.2s;
        }
        .quick-actions button:hover {
            border-color: #7b2ff7;
            color: white;
        }
        .powered-by {
            text-align: center;
            padding: 8px;
            font-size: 0.75rem;
            color: #444;
        }
        .powered-by a { color: #7b2ff7; text-decoration: none; }
    </style>
</head>
<body>
    <div class="header">
        <h1>🎯 PrepAgent</h1>
        <span class="badge">AI Interview Coach</span>
        <span class="subtitle">Powered by Gemini + MongoDB</span>
    </div>
    
    <div class="chat-container" id="chat">
        <div class="welcome">
            <h2>Ready to ace your interviews?</h2>
            <p>I'm PrepAgent — your AI interview coach. I'll help you practice with</p>
            <p>personalized questions, real-time feedback, and progress tracking.</p>
            <div class="quick-actions">
                <button onclick="sendQuick('I want to practice for a software engineering interview at Google')">🎯 Practice for Google SWE</button>
                <button onclick="sendQuick('Generate 5 behavioral interview questions for a senior role')">💡 Generate Questions</button>
                <button onclick="sendQuick('Show me my progress and what I should focus on')">📊 Check Progress</button>
                <button onclick="sendQuick('Create a 2-week interview study plan for a data scientist role')">📋 Study Plan</button>
            </div>
        </div>
    </div>
    
    <div class="input-area">
        <textarea id="input" placeholder="Tell me about your target role, or ask me anything about interview prep..." 
                  onkeydown="if(event.key==='Enter'&&!event.shiftKey){event.preventDefault();send()}" rows="1"></textarea>
        <button id="sendBtn" onclick="send()">Send →</button>
    </div>
    
    <div class="powered-by">
        Built with <a href="https://adk.dev">Google ADK</a> + Gemini 2.5 Flash + 
        <a href="https://www.mongodb.com/mcp">MongoDB MCP</a> | 
        <a href="https://rapid-agent.devpost.com">Rapid Agent Hackathon 2026</a>
    </div>

    <script>
        const chat = document.getElementById('chat');
        const input = document.getElementById('input');
        const sendBtn = document.getElementById('sendBtn');
        let sessionId = 'user_' + Math.random().toString(36).substr(2, 9);

        function addMessage(text, role) {
            // Remove welcome on first message
            const welcome = chat.querySelector('.welcome');
            if (welcome) welcome.remove();
            
            const div = document.createElement('div');
            div.className = 'message ' + role;
            div.textContent = text;
            chat.appendChild(div);
            chat.scrollTop = chat.scrollHeight;
            return div;
        }

        function sendQuick(text) {
            input.value = text;
            send();
        }

        async function send() {
            const text = input.value.trim();
            if (!text) return;
            
            input.value = '';
            sendBtn.disabled = true;
            addMessage(text, 'user');
            
            const typing = document.createElement('div');
            typing.className = 'typing';
            typing.textContent = '🤔 Thinking...';
            chat.appendChild(typing);
            chat.scrollTop = chat.scrollHeight;

            try {
                const resp = await fetch('/chat', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({ message: text, session_id: sessionId })
                });
                const data = await resp.json();
                typing.remove();
                addMessage(data.response || 'No response', 'agent');
            } catch (err) {
                typing.remove();
                addMessage('Error: ' + err.message, 'agent');
            }
            
            sendBtn.disabled = false;
            input.focus();
        }
        
        // Auto-resize textarea
        input.addEventListener('input', function() {
            this.style.height = 'auto';
            this.style.height = Math.min(this.scrollHeight, 120) + 'px';
        });
    </script>
</body>
</html>"""


@app.get("/", response_class=HTMLResponse)
async def home():
    return HTML_TEMPLATE


@app.post("/chat")
async def chat_endpoint(request: Request):
    data = await request.json()
    message = data.get("message", "")
    session_id = data.get("session_id", "default")
    user_id = "user_1"  # Simplified for hackathon

    # Create or get session
    session = await session_service.get_session(
        app_name="prepagent", user_id=user_id, session_id=session_id
    )
    if session is None:
        session = await session_service.create_session(
            app_name="prepagent", user_id=user_id, session_id=session_id
        )

    # Create user message
    user_content = Content(role="user", parts=[Part(text=message)])

    # Run agent
    response_text = ""
    async for event in runner.run_async(
        user_id=user_id,
        session_id=session.id,
        new_message=user_content,
    ):
        if event.content and event.content.parts:
            for part in event.content.parts:
                if part.text:
                    response_text += part.text

    return {"response": response_text, "session_id": session_id}


if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8080))
    uvicorn.run(app, host="0.0.0.0", port=port)
