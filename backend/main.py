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
from .context_manager import (
    get_enhanced_session,
    update_conversation_state,
    add_context_memory,
    detect_follow_up_intent,
    generate_contextual_response,
    should_batch_queries,
    extract_sub_queries,
    create_context_summary,
    cleanup_old_sessions,
    ContextType,
    ConversationState
)
from .ticket_management import get_ticket_statistics

# Initialize FastAPI application
app = FastAPI(title="IT Helpdesk Bot API - Enhanced Edition")

# CORS middleware for frontend development
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Adjust to frontend domain when deploying
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Enhanced system prompt for the IT Helpdesk assistant
SYSTEM_PROMPT = """You are an advanced IT Helpdesk assistant for an enterprise environment. You have access to:

🔧 **Core Capabilities:**
- Comprehensive knowledge base with detailed troubleshooting guides
- Enhanced FAQ database with smart matching
- Interactive step-by-step troubleshooting flows
- Advanced ticket management with auto-categorization
- Multi-turn conversation context awareness

🎯 **Your Approach:**
- Be helpful, concise, and professional
- Use the knowledge base and troubleshooting flows for complex issues
- Create tickets when hands-on assistance is needed
- Remember context from previous interactions in the conversation
- Handle follow-up questions intelligently
- Process multiple questions efficiently when asked together

🛠️ **Available Tools:**
- Search knowledge base articles for detailed solutions
- Access enhanced FAQ database
- Start interactive troubleshooting flows (wifi_issues, printer_issues, email_issues)
- Create and track support tickets with priorities
- Check ticket status and list user tickets
- Get helpdesk statistics

💡 **Guidelines:**
- Always search the knowledge base first for technical issues
- Use troubleshooting flows for common problems (Wi-Fi, printers, email)
- Create tickets for issues requiring hands-on support or when solutions don't work
- Maintain conversation context and handle follow-ups like "that didn't work"
- Be proactive in suggesting next steps or alternatives

Remember: You can handle multiple questions at once and maintain context throughout the conversation."""


def get_session_messages(session_id: str) -> List[Dict[str, str]]:
    """Get or initialize enhanced session messages with system prompt and context"""
    session = get_enhanced_session(session_id)

    if not session["messages"]:
        # Initialize with enhanced system prompt
        session["messages"] = [{"role": "system", "content": SYSTEM_PROMPT}]

    return session["messages"]


def enhanced_split_into_subqueries(user_text: str, session_id: str) -> List[str]:
    """
    Enhanced batching logic with context awareness:
    - Use context manager to determine if batching is appropriate
    - Split by question marks, line breaks, or conjunctions for multiple questions
    - Keep related questions grouped intelligently
    """
    # Check if this should be batched
    if not should_batch_queries(user_text):
        return [user_text]

    # Extract sub-queries using enhanced logic
    subqueries = extract_sub_queries(user_text)

    # Update context to indicate we're processing multiple queries
    if len(subqueries) > 1:
        update_conversation_state(session_id, ConversationState.GENERAL.value, {
            "batch_processing": True,
            "total_queries": len(subqueries)
        })

    # Limit batch to maximum 4 items for efficiency
    return subqueries[:4] if subqueries else [user_text]


@app.post("/chat", response_model=ChatResponse)
def chat(req: ChatRequest):
    """Enhanced chat endpoint with context awareness and advanced features"""
    try:
        client = get_client()

        # Get enhanced session with context management
        session = get_enhanced_session(req.session_id)
        messages = get_session_messages(req.session_id)

        # Detect follow-up intent and generate contextual response if applicable
        follow_up_analysis = detect_follow_up_intent(
            req.message, req.session_id)

        if follow_up_analysis["is_follow_up"] and follow_up_analysis["has_context"]:
            contextual_response = generate_contextual_response(
                follow_up_analysis, req.session_id)
            if contextual_response:
                # Add context-aware response and continue with enhanced processing
                context_prefix = f"{contextual_response}\n\nLet me help you further: "
                user_message = context_prefix + req.message
            else:
                user_message = req.message
        else:
            user_message = req.message

        # Enhanced batching: if user sends multiple questions, wrap them appropriately
        subqs = enhanced_split_into_subqueries(req.message, req.session_id)
        if len(subqs) > 1:
            user_payload = "The user has multiple questions:\n" + \
                "\n".join([f"- {q}" for q in subqs])
            user_payload += f"\n\nPlease address each question clearly and comprehensively."
        else:
            user_payload = user_message

        # Add conversation context summary for the AI
        context_summary = create_context_summary(req.session_id)
        if context_summary:
            user_payload = f"{context_summary}\n\nUser: {user_payload}"

        # Store the current issue in context for future follow-ups
        add_context_memory(
            req.session_id, ContextType.LAST_ISSUE.value, req.message)

        messages.append({"role": "user", "content": user_payload})

        tools = get_tools_schema()

        # Enhanced tool calling loop with better context management
        MAX_TOOL_TURNS = 6  # Increased for more complex workflows
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
                # Convert tool calls to dict format for messages
                tool_calls_dict = []
                for tc in msg.tool_calls:
                    tool_calls_dict.append({
                        "id": tc.id,
                        "type": "function",
                        "function": {
                            "name": tc.function.name,
                            "arguments": tc.function.arguments
                        }
                    })

                messages.append({
                    "role": "assistant",
                    "content": msg.content or "",
                    "tool_calls": tool_calls_dict
                })

                # Process each tool call and update context as needed
                for tool_call in msg.tool_calls:
                    name = tool_call.function.name
                    arguments = tool_call.function.arguments
                    result = call_tool_by_name(name, arguments)

                    # Update conversation state based on tool usage
                    if name == "create_ticket":
                        update_conversation_state(
                            req.session_id, ConversationState.TICKET_CREATION.value)
                        # Extract ticket info for context
                        try:
                            args = eval(arguments) if arguments else {}
                            ticket_info = {"issue": args.get(
                                "issue", ""), "tool_result": result}
                            add_context_memory(
                                req.session_id, ContextType.RECENT_TICKET.value, ticket_info)
                        except:
                            pass
                    elif name == "start_troubleshooting_flow":
                        update_conversation_state(
                            req.session_id, ConversationState.TROUBLESHOOTING.value)
                        try:
                            args = eval(arguments) if arguments else {}
                            flow_info = {"type": args.get(
                                "issue_type", ""), "started": True}
                            add_context_memory(
                                req.session_id, ContextType.CURRENT_FLOW.value, flow_info)
                        except:
                            pass
                    elif name in ["search_knowledge_base_articles", "get_enhanced_faq_answer"]:
                        update_conversation_state(
                            req.session_id, ConversationState.KB_SEARCH.value)
                        try:
                            args = eval(arguments) if arguments else {}
                            search_info = {"query": args.get("question", "") or args.get(
                                "query", ""), "results": result}
                            add_context_memory(
                                req.session_id, ContextType.SEARCH_RESULTS.value, search_info)
                        except:
                            pass

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
                assistant_text = msg.content or "I'm here to help with your IT needs."
                messages.append(
                    {"role": "assistant", "content": assistant_text})
                break

        # Enhanced session management - trim overly long history but preserve important context
        if len(messages) > 40:  # Increased limit for better context retention
            # Keep system prompt + last 35 messages
            preserved_messages = [messages[0]] + messages[-35:]
            session["messages"] = preserved_messages
        else:
            session["messages"] = messages

        # Cleanup old sessions periodically (every 50th request approximately)
        import random
        if random.randint(1, 50) == 1:
            cleanup_old_sessions(24)  # Clean up sessions older than 24 hours

        # Create enhanced payload to return to frontend
        history_for_client: List[ChatMessage] = [
            ChatMessage(role=m["role"], content=m.get("content", "") or "")
            for m in messages if m["role"] in ("user", "assistant") and m.get("content")
        ]

        # Get updated ticket statistics for frontend
        ticket_stats = get_ticket_statistics()

        return ChatResponse(
            reply=history_for_client[-1].content if history_for_client else "",
            messages=history_for_client,
            tickets=ticket_data,  # Keep for backward compatibility
            stats=ticket_stats  # Add enhanced statistics
        )

    except Exception as e:
        print(f"Error in chat endpoint: {str(e)}")
        raise HTTPException(
            status_code=500, detail=f"Internal server error: {str(e)}")


@app.get("/health")
def health():
    """Enhanced health check endpoint with system statistics"""
    try:
        ticket_stats = get_ticket_statistics()
        return {
            "status": "ok",
            "tickets_total": ticket_stats.get("total", 0),
            "tickets_open": ticket_stats.get("by_status", {}).get("Open", 0),
            "tickets_in_progress": ticket_stats.get("by_status", {}).get("In Progress", 0),
            "system": "IT Helpdesk Bot - Enhanced Edition",
            "features": [
                "Knowledge Base Search",
                "Interactive Troubleshooting",
                "Enhanced Ticket Management",
                "Multi-turn Context Memory",
                "Batch Request Processing"
            ]
        }
    except Exception as e:
        return {
            "status": "error",
            "error": str(e),
            "system": "IT Helpdesk Bot - Enhanced Edition"
        }


@app.get("/stats")
def get_system_stats():
    """Get comprehensive system statistics"""
    try:
        from .context_manager import get_session_statistics

        ticket_stats = get_ticket_statistics()
        session_stats = get_session_statistics()

        return {
            "tickets": ticket_stats,
            "sessions": session_stats,
            "system_status": "operational"
        }
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Error retrieving stats: {str(e)}")


# Remove the old SESSIONS dictionary as we're now using enhanced session management
# SESSIONS: Dict[str, List[Dict[str, str]]] = {}
