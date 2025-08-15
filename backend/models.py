# Import necessary modules for data models
from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any


class ChatMessage(BaseModel):
    """Represents a single chat message"""
    role: str  # "user" | "assistant" | "system"
    content: str


class ChatRequest(BaseModel):
    """Request model for chat endpoint"""
    session_id: str = Field(...,
                            description="Client session id to keep context")
    message: str
    # Optional history, if sent from client
    history: Optional[List[ChatMessage]] = None


class ChatResponse(BaseModel):
    """Response model for chat endpoint"""
    reply: str
    messages: List[ChatMessage]
    tickets: Optional[List[Dict[str, Any]]] = None


class ToolCallResult(BaseModel):
    """Result of a tool function call"""
    name: str
    result: str
