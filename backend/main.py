# Import necessary modules
import os
import re
from typing import Dict, List, Any

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from .models import ChatRequest, ChatResponse, ChatMessage
from .openai_client import get_client, MODEL_NAME
from .functions import get_tools_schema, call_tool_by_name
from .mock_data import ticket_data

# Initialize FastAPI application
app = FastAPI(title="IT Helpdesk Bot API")

# CORS middleware for frontend development
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Adjust to frontend domain when deploying
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Context memory storage by session_id
SESSIONS: Dict[str, List[Dict[str, str]]] = {}

# System prompt for the IT Helpdesk assistant
SYSTEM_PROMPT = (
    "You are an IT Helpdesk assistant for an enterprise. "
    "Be concise, friendly, and propose creating a support ticket when needed. "
    "Use tools when appropriate. If the user asks multiple questions at once, "
    "answer each clearly."
)


def get_session_messages(session_id: str) -> List[Dict[str, str]]:
    """Get or initialize session messages with system prompt"""
    if session_id not in SESSIONS:
        SESSIONS[session_id] = [{"role": "system", "content": SYSTEM_PROMPT}]
    return SESSIONS[session_id]


def split_into_subqueries(user_text: str) -> List[str]:
    """
    Simple batching logic:
    - Split by question marks, line breaks, or 'Also,' / 'and' if there are multiple questions.
    - Keep short sentences grouped together if needed.
    """
    # Prioritize question marks
    parts = re.split(r"\?\s*|\n+", user_text.strip())
    parts = [p.strip() for p in parts if p.strip()]
    if len(parts) <= 1:
        # Light split by 'Also,' or ' and ' when it appears to be two questions
        parts = re.split(r"\balso,?\b|\band\b", user_text, flags=re.IGNORECASE)
        parts = [p.strip().rstrip(".") for p in parts if p.strip()]
    # Limit batch to maximum 4 items for efficiency
    return parts[:4] if parts else [user_text]


@app.post("/chat", response_model=ChatResponse)
def chat(req: ChatRequest):
    """Main chat endpoint that handles user messages and tool calls"""
    try:
        client = get_client()

        # Get server-side history to ensure context management
        messages = get_session_messages(req.session_id)

        # Batching: if user sends multiple questions, wrap them in a meta-prompt
        subqs = split_into_subqueries(req.message)
        if len(subqs) > 1:
            user_payload = "The user has multiple questions:\n" + \
                "\n".join([f"- {q}" for q in subqs])
        else:
            user_payload = req.message

        messages.append({"role": "user", "content": user_payload})

        tools = get_tools_schema()

        # Loop to handle tool calls until model doesn't request tools anymore
        MAX_TOOL_TURNS = 4
        tool_turns = 0
        while tool_turns < MAX_TOOL_TURNS:
            completion = client.chat.completions.create(
                model=MODEL_NAME,
                messages=messages,
                tools=tools,
                tool_choice="auto",
                temperature=0.2,
            )
            msg = completion.choices[0].message

            if msg.tool_calls:
                # Model requests function call(s)
                messages.append(
                    {"role": "assistant", "content": msg.content or "", "tool_calls": []})
                for tool_call in msg.tool_calls:
                    name = tool_call.function.name
                    arguments = tool_call.function.arguments
                    result = call_tool_by_name(name, arguments)
                    # Push function result to model
                    messages.append({
                        "role": "tool",
                        "content": result,
                        "tool_call_id": tool_call.id
                    })
                tool_turns += 1
                continue
            else:
                # No more tool calls → this is the final answer
                assistant_text = msg.content or "I'm here to help."
                messages.append(
                    {"role": "assistant", "content": assistant_text})
                break

        # Trim overly long history (keep system + 16 recent turns)
        if len(messages) > 34:
            SESSIONS[req.session_id] = [messages[0]] + messages[-33:]

        # Create payload to return to frontend
        history_for_client: List[ChatMessage] = [
            ChatMessage(role=m["role"], content=m.get("content", "") or "")
            for m in messages if m["role"] in ("user", "assistant")
        ]
        return ChatResponse(
            reply=history_for_client[-1].content if history_for_client else "",
            messages=history_for_client,
            tickets=ticket_data,
        )

    except Exception as e:
        print(f"Error in chat endpoint: {str(e)}")
        raise HTTPException(
            status_code=500, detail=f"Internal server error: {str(e)}")


@app.get("/health")
def health():
    """Health check endpoint"""
    return {"status": "ok", "tickets_open": len([t for t in ticket_data if t["status"] == "Open"])}
