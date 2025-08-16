# Enhanced Conversation Context Manager
# Manages multi-turn conversations, context memory, and intelligent follow-up handling

import json
from typing import Dict, List, Any, Optional
from datetime import datetime, timedelta
from enum import Enum


class ConversationState(Enum):
    GENERAL = "general"
    TROUBLESHOOTING = "troubleshooting"
    TICKET_CREATION = "ticket_creation"
    FOLLOW_UP = "follow_up"
    KB_SEARCH = "kb_search"


class ContextType(Enum):
    LAST_ISSUE = "last_issue"
    CURRENT_FLOW = "current_flow"
    RECENT_TICKET = "recent_ticket"
    SEARCH_RESULTS = "search_results"
    USER_PREFERENCES = "user_preferences"


# Session storage with enhanced context tracking
enhanced_sessions: Dict[str, Dict[str, Any]] = {}


def get_enhanced_session(session_id: str) -> Dict[str, Any]:
    """Get or initialize enhanced session context"""
    if session_id not in enhanced_sessions:
        enhanced_sessions[session_id] = {
            "messages": [],
            "context": {
                "state": ConversationState.GENERAL.value,
                "last_issue": None,
                "current_troubleshooting_flow": None,
                "recent_tickets": [],
                "search_history": [],
                "user_preferences": {},
                "follow_up_context": None
            },
            "created_at": datetime.now().isoformat(),
            "last_activity": datetime.now().isoformat()
        }
    else:
        # Update last activity
        enhanced_sessions[session_id]["last_activity"] = datetime.now(
        ).isoformat()

    return enhanced_sessions[session_id]


def update_conversation_state(session_id: str, new_state: str, context_data: Optional[Dict[str, Any]] = None) -> None:
    """Update the conversation state and associated context"""
    session = get_enhanced_session(session_id)
    session["context"]["state"] = new_state

    if context_data:
        session["context"].update(context_data)


def add_context_memory(session_id: str, context_type: str, data: Any) -> None:
    """Add specific context information to session memory"""
    session = get_enhanced_session(session_id)
    context = session["context"]

    if context_type == ContextType.LAST_ISSUE.value:
        context["last_issue"] = {
            "description": data,
            "timestamp": datetime.now().isoformat()
        }
    elif context_type == ContextType.CURRENT_FLOW.value:
        context["current_troubleshooting_flow"] = data
    elif context_type == ContextType.RECENT_TICKET.value:
        context["recent_tickets"].insert(0, data)
        # Keep only last 5 tickets
        context["recent_tickets"] = context["recent_tickets"][:5]
    elif context_type == ContextType.SEARCH_RESULTS.value:
        context["search_history"].insert(0, {
            "query": data["query"],
            "results": data["results"],
            "timestamp": datetime.now().isoformat()
        })
        # Keep only last 10 searches
        context["search_history"] = context["search_history"][:10]
    elif context_type == ContextType.USER_PREFERENCES.value:
        context["user_preferences"].update(data)


def get_context_memory(session_id: str, context_type: str) -> Any:
    """Retrieve specific context information from session memory"""
    session = get_enhanced_session(session_id)
    context = session["context"]

    if context_type == ContextType.LAST_ISSUE.value:
        return context.get("last_issue")
    elif context_type == ContextType.CURRENT_FLOW.value:
        return context.get("current_troubleshooting_flow")
    elif context_type == ContextType.RECENT_TICKET.value:
        return context.get("recent_tickets", [])
    elif context_type == ContextType.SEARCH_RESULTS.value:
        return context.get("search_history", [])
    elif context_type == ContextType.USER_PREFERENCES.value:
        return context.get("user_preferences", {})

    return None


def detect_follow_up_intent(user_message: str, session_id: str) -> Dict[str, Any]:
    """
    Detect if user message is a follow-up to previous conversation and determine intent
    """
    message_lower = user_message.lower().strip()
    session = get_enhanced_session(session_id)
    context = session["context"]

    # Common follow-up phrases
    follow_up_patterns = {
        "that_didnt_work": [
            "that didn't work", "that doesn't work", "still not working",
            "still having issues", "didn't help", "doesn't help", "not working",
            "same problem", "still broken", "didn't fix"
        ],
        "need_more_help": [
            "what else", "other options", "another way", "different solution",
            "more help", "something else", "alternative", "what now"
        ],
        "clarification": [
            "what do you mean", "how do i", "where is", "which", "what",
            "can you explain", "i don't understand", "confused"
        ],
        "status_check": [
            "what's the status", "any update", "how long", "when will",
            "is it ready", "progress", "update on"
        ],
        "escalation": [
            "speak to someone", "call someone", "escalate", "manager",
            "human", "person", "phone", "urgent"
        ]
    }

    intent_detected = None
    confidence = 0

    for intent, patterns in follow_up_patterns.items():
        for pattern in patterns:
            if pattern in message_lower:
                intent_detected = intent
                confidence = 0.8
                break
        if intent_detected:
            break

    # Check if we have relevant context for this follow-up
    has_context = False
    context_details = {}

    if intent_detected:
        # Check for recent issue context
        last_issue = context.get("last_issue")
        if last_issue:
            has_context = True
            context_details["last_issue"] = last_issue

        # Check for troubleshooting flow context
        current_flow = context.get("current_troubleshooting_flow")
        if current_flow:
            has_context = True
            context_details["troubleshooting_flow"] = current_flow

        # Check for recent ticket context
        recent_tickets = context.get("recent_tickets", [])
        if recent_tickets:
            has_context = True
            context_details["recent_ticket"] = recent_tickets[0]

    return {
        "is_follow_up": intent_detected is not None,
        "intent": intent_detected,
        "confidence": confidence,
        "has_context": has_context,
        "context_details": context_details
    }


def generate_contextual_response(follow_up_analysis: Dict[str, Any], session_id: str) -> str:
    """
    Generate an appropriate response based on follow-up analysis and context
    """
    if not follow_up_analysis["is_follow_up"] or not follow_up_analysis["has_context"]:
        return None

    intent = follow_up_analysis["intent"]
    context_details = follow_up_analysis["context_details"]

    if intent == "that_didnt_work":
        if "last_issue" in context_details:
            issue = context_details["last_issue"]["description"]
            return f"I understand the previous solution for '{issue}' didn't work. Let me suggest alternative approaches or we can escalate this to create a support ticket for hands-on assistance."
        elif "troubleshooting_flow" in context_details:
            return "I see the current troubleshooting step wasn't successful. Let me guide you to the next alternative solution."

    elif intent == "need_more_help":
        if "last_issue" in context_details:
            return "I'd be happy to provide additional solutions. Would you like me to search our knowledge base for more advanced troubleshooting steps, or shall we create a support ticket for personalized assistance?"

    elif intent == "clarification":
        if "last_issue" in context_details:
            return "Of course! Let me provide more detailed step-by-step instructions for the solution I suggested. Which part would you like me to clarify?"

    elif intent == "status_check":
        if "recent_ticket" in context_details:
            ticket = context_details["recent_ticket"]
            return f"Let me check the status of your recent ticket {ticket.get('id', 'N/A')} regarding '{ticket.get('issue', 'your issue')}'."

    elif intent == "escalation":
        return "I understand you'd like to speak with someone directly. Let me create a support ticket for you, and our IT team will contact you as soon as possible. What priority level would you consider this issue?"

    return None


def should_batch_queries(user_message: str) -> bool:
    """
    Determine if user message contains multiple queries that should be batched
    """
    # Look for multiple question indicators
    question_marks = user_message.count("?")
    if question_marks > 1:
        return True

    # Look for conjunction words that might indicate multiple requests
    batch_indicators = [
        " and also ", " also ", " plus ", " additionally ",
        ". also", ". i also", ". can you also", ". another",
        "second question", "another issue", "one more thing"
    ]

    message_lower = user_message.lower()
    for indicator in batch_indicators:
        if indicator in message_lower:
            return True

    return False


def extract_sub_queries(user_message: str) -> List[str]:
    """
    Extract individual queries from a batched message
    """
    import re

    # Split by question marks first
    parts = re.split(r'\?\s*', user_message)
    queries = []

    for i, part in enumerate(parts):
        part = part.strip()
        if part:
            # Add question mark back if it was in the original (except last part if empty)
            if i < len(parts) - 1 or (i == len(parts) - 1 and user_message.endswith('?')):
                part += "?"
            queries.append(part)

    # If no question marks, try splitting by other indicators
    if len(queries) <= 1:
        batch_patterns = [
            r'\.\s*(?:also|additionally|another|second)',
            r'\.\s*(?:can you also|could you also)',
            r'\.\s*(?:i also|i need|i want)'
        ]

        for pattern in batch_patterns:
            parts = re.split(pattern, user_message, flags=re.IGNORECASE)
            if len(parts) > 1:
                queries = [part.strip() for part in parts if part.strip()]
                break

    # Limit to reasonable number of queries
    return queries[:4] if len(queries) > 1 else [user_message]


def create_context_summary(session_id: str) -> str:
    """
    Create a summary of the current conversation context for the AI
    """
    session = get_enhanced_session(session_id)
    context = session["context"]

    summary_parts = []

    # Add conversation state
    state = context.get("state", "general")
    summary_parts.append(f"Conversation state: {state}")

    # Add last issue context
    last_issue = context.get("last_issue")
    if last_issue:
        summary_parts.append(
            f"User's last reported issue: {last_issue['description']}")

    # Add troubleshooting context
    current_flow = context.get("current_troubleshooting_flow")
    if current_flow:
        summary_parts.append(
            f"Currently in troubleshooting flow: {current_flow.get('title', 'Unknown')}")

    # Add recent ticket context
    recent_tickets = context.get("recent_tickets", [])
    if recent_tickets:
        latest_ticket = recent_tickets[0]
        summary_parts.append(
            f"Recent ticket: {latest_ticket.get('id')} - {latest_ticket.get('issue')}")

    # Add search history context
    search_history = context.get("search_history", [])
    if search_history:
        latest_search = search_history[0]
        summary_parts.append(f"Recent search: '{latest_search['query']}'")

    if summary_parts:
        return "CONTEXT: " + " | ".join(summary_parts)

    return ""


def cleanup_old_sessions(max_age_hours: int = 24) -> int:
    """
    Clean up sessions older than max_age_hours
    Returns number of sessions cleaned up
    """
    current_time = datetime.now()
    cutoff_time = current_time - timedelta(hours=max_age_hours)

    sessions_to_remove = []

    for session_id, session_data in enhanced_sessions.items():
        last_activity = datetime.fromisoformat(session_data["last_activity"])
        if last_activity < cutoff_time:
            sessions_to_remove.append(session_id)

    for session_id in sessions_to_remove:
        del enhanced_sessions[session_id]

    return len(sessions_to_remove)


def get_session_statistics() -> Dict[str, Any]:
    """
    Get statistics about current sessions
    """
    total_sessions = len(enhanced_sessions)
    states = {}

    for session_data in enhanced_sessions.values():
        state = session_data["context"]["state"]
        states[state] = states.get(state, 0) + 1

    return {
        "total_sessions": total_sessions,
        "by_state": states,
        "active_sessions": total_sessions
    }
