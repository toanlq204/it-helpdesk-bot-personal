# Import necessary modules
import json
from typing import List, Dict, Any
from .mock_data import faq_data, software_list, ticket_data
from .knowledge_base import (
    search_knowledge_base,
    search_enhanced_faq,
    get_troubleshooting_flow,
    get_available_flows
)
from .ticket_management import (
    create_enhanced_ticket,
    get_ticket_status,
    update_ticket_status,
    list_user_tickets,
    get_ticket_statistics,
    simulate_ticket_progress
)


# Enhanced function to search knowledge base articles
def search_knowledge_base_articles(query: str, max_results: int = 3) -> str:
    """Search comprehensive knowledge base for relevant IT help articles"""
    results = search_knowledge_base(query, max_results)

    if not results:
        return f"No knowledge base articles found for '{query}'. Would you like me to create a support ticket or try a different search?"

    response = f"Found {len(results)} relevant knowledge base articles for '{query}':\n\n"

    for i, article in enumerate(results, 1):
        response += f"**{i}. {article['title']}** (Category: {article['category']})\n"
        # Provide a summary of the content (first 200 characters)
        summary = article['content'][:200].replace('\n', ' ')
        if len(article['content']) > 200:
            summary += "..."
        response += f"{summary}\n"
        response += f"📖 Article ID: {article['id']}\n\n"

    response += "Would you like me to provide the full details for any of these articles, or search for something more specific?"
    return response


# Enhanced FAQ search function
def get_enhanced_faq_answer(question: str) -> str:
    """Search enhanced FAQ database with better matching"""
    results = search_enhanced_faq(question, max_results=3)

    if not results:
        # Fallback to original FAQ search
        return get_faq_answer(question)

    if len(results) == 1:
        faq = results[0]
        return f"**{faq['question']}**\n\n{faq['answer']}\n\n💡 Category: {faq['category']}"

    # Multiple results - show options
    response = f"I found {len(results)} relevant FAQs for your question:\n\n"
    for i, faq in enumerate(results, 1):
        response += f"**{i}. {faq['question']}**\n{faq['answer'][:100]}...\n\n"

    response += "Which of these is most relevant to your question?"
    return response


# Function to get an FAQ answer based on a question (legacy support)
def get_faq_answer(question: str) -> str:
    q = (question or "").lower().strip()  # Normalize the question
    # Check for exact match in FAQ data
    for faq in faq_data:
        if q in faq["question"].lower():
            return faq["answer"]
    # Check for partial match in FAQ data
    for faq in faq_data:
        if any(k in faq["question"].lower() for k in q.split() if len(k) > 3):
            return faq["answer"]
    # Return default response if no match is found
    return "I couldn't find a specific FAQ for that. Would you like me to create a support ticket?"


# Enhanced ticket creation function
def create_ticket(issue: str, created_by: str = "user", priority: str = None) -> str:
    """Create an enhanced support ticket with auto-categorization"""
    ticket = create_enhanced_ticket(issue, created_by, priority)

    response = f"✅ **Ticket {ticket['id']} Created Successfully**\n\n"
    response += f"📝 **Issue:** {ticket['issue']}\n"
    response += f"🏷️ **Category:** {ticket['category']}\n"
    response += f"⚡ **Priority:** {ticket['priority']}\n"
    response += f"👤 **Assigned to:** {ticket['assigned_to']}\n"
    response += f"📅 **Created:** {ticket['created_at'][:19].replace('T', ' ')}\n"
    response += f"⏰ **Estimated Resolution:** {ticket['estimated_resolution'][:19].replace('T', ' ')}\n\n"
    response += f"You can check the status anytime by asking about ticket {ticket['id']}."

    return response


# Function to check ticket status
def check_ticket_status(ticket_id: str) -> str:
    """Get detailed status information for a specific ticket"""
    status_info = get_ticket_status(ticket_id)

    if "error" in status_info:
        return status_info["error"]

    ticket = status_info["ticket"]

    # Simulate some progress for demo purposes
    simulate_ticket_progress(ticket_id)
    # Get updated status after simulation
    status_info = get_ticket_status(ticket_id)
    ticket = status_info["ticket"]

    response = f"🎫 **Ticket {ticket['id']} Status**\n\n"
    response += f"📝 **Issue:** {ticket['issue']}\n"
    response += f"📊 **Status:** {ticket['status']}\n"
    response += f"⚡ **Priority:** {ticket['priority']}\n"
    response += f"👤 **Assigned to:** {ticket['assigned_to']}\n"
    response += f"⏱️ **Time Elapsed:** {status_info['time_elapsed_hours']} hours\n"

    if status_info['is_overdue']:
        response += "⚠️ **OVERDUE** - This ticket has exceeded the estimated resolution time.\n"

    response += f"\n📋 **Status Description:** {status_info['status_description']}\n"

    if ticket['comments']:
        response += f"\n💬 **Recent Updates:**\n"
        for comment in ticket['comments'][-3:]:  # Show last 3 comments
            timestamp = comment['timestamp'][:19].replace('T', ' ')
            response += f"• {timestamp} - {comment['author']}: {comment['comment']}\n"

    return response


# Function to list user's tickets
def list_my_tickets(created_by: str = "user", status_filter: str = None) -> str:
    """List tickets created by the user"""
    tickets = list_user_tickets(created_by, status_filter)

    if not tickets:
        filter_text = f" with status '{status_filter}'" if status_filter else ""
        return f"No tickets found{filter_text}. Would you like to create a new support ticket?"

    response = f"📋 **Your Support Tickets** ({len(tickets)} found)\n\n"

    for ticket in tickets:
        created_date = ticket['created_at'][:10]  # Just the date
        response += f"🎫 **{ticket['id']}** - {ticket['status']}\n"
        response += f"   📝 {ticket['issue'][:60]}{'...' if len(ticket['issue']) > 60 else ''}\n"
        response += f"   📅 Created: {created_date} | Priority: {ticket['priority']}\n\n"

    response += "Ask me about any specific ticket ID for detailed status information."
    return response


# Function to start interactive troubleshooting
def start_troubleshooting_flow(issue_type: str) -> str:
    """Start an interactive troubleshooting flow for common issues"""
    available_flows = get_available_flows()

    if issue_type not in available_flows:
        flows_list = ", ".join(available_flows)
        return f"Available troubleshooting flows: {flows_list}. Please specify which type of issue you're experiencing."

    flow = get_troubleshooting_flow(issue_type)
    if not flow:
        return "Sorry, that troubleshooting flow is not available right now."

    first_step = flow['steps'][0]

    response = f"🛠️ **Starting {flow['title']}**\n\n"
    response += f"Let's work through this step by step:\n\n"
    response += f"**Step 1:** {first_step['question']}\n\n"

    if first_step['type'] == 'yes_no':
        response += "Please answer: **Yes** or **No**"
    elif first_step['type'] == 'multiple_choice':
        response += "Please choose from:\n"
        for i, option in enumerate(first_step['options'], 1):
            response += f"{i}. {option['text']}\n"

    return response


# Function to get software information based on its name
def get_software_info(name: str) -> str:
    n = (name or "").lower().strip()  # Normalize the software name
    # Search for the software in the software list
    for s in software_list:
        if n in s["name"].lower():
            return f"{s['name']} (v{s['version']}): {s['installer_link']}"
    # Return default response if software is not found
    return "Software not found in the catalog."


# Function to get IT helpdesk statistics
def get_helpdesk_stats() -> str:
    """Get current helpdesk statistics"""
    stats = get_ticket_statistics()

    if stats['total'] == 0:
        return "📊 **IT Helpdesk Statistics**\n\nNo tickets in the system currently."

    response = f"📊 **IT Helpdesk Statistics**\n\n"
    response += f"📋 **Total Tickets:** {stats['total']}\n\n"

    if stats['by_status']:
        response += "**By Status:**\n"
        for status, count in stats['by_status'].items():
            response += f"• {status}: {count}\n"
        response += "\n"

    if stats['by_priority']:
        response += "**By Priority:**\n"
        for priority, count in stats['by_priority'].items():
            response += f"• {priority}: {count}\n"
        response += "\n"

    if stats['by_category']:
        response += "**By Category:**\n"
        for category, count in stats['by_category'].items():
            response += f"• {category}: {count}\n"

    return response


# Function to get the schema of available tools
def get_tools_schema() -> List[Dict[str, Any]]:
    return [
        {
            "type": "function",
            "function": {
                "name": "search_knowledge_base_articles",
                "description": "Search comprehensive knowledge base for detailed IT help articles and troubleshooting guides",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "query": {"type": "string", "description": "Search query for knowledge base articles"},
                        "max_results": {"type": "integer", "description": "Maximum number of articles to return (default: 3)"}
                    },
                    "required": ["query"]
                }
            },
        },
        {
            "type": "function",
            "function": {
                "name": "get_enhanced_faq_answer",
                "description": "Search enhanced FAQ database with better matching and multiple results",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "question": {"type": "string", "description": "The FAQ question to search for"}
                    },
                    "required": ["question"]
                }
            },
        },
        {
            "type": "function",
            "function": {
                "name": "create_ticket",
                "description": "Create an enhanced IT support ticket with auto-categorization and priority assignment",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "issue": {"type": "string", "description": "Description of the IT issue"},
                        "created_by": {"type": "string", "description": "User creating the ticket"},
                        "priority": {"type": "string", "description": "Priority level (Low, Medium, High, Urgent, Critical)"}
                    },
                    "required": ["issue"]
                }
            },
        },
        {
            "type": "function",
            "function": {
                "name": "check_ticket_status",
                "description": "Get detailed status information for a specific support ticket",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "ticket_id": {"type": "string", "description": "The ticket ID to check"}
                    },
                    "required": ["ticket_id"]
                }
            },
        },
        {
            "type": "function",
            "function": {
                "name": "list_my_tickets",
                "description": "List all tickets created by the user, optionally filtered by status",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "created_by": {"type": "string", "description": "User whose tickets to list"},
                        "status_filter": {"type": "string", "description": "Filter by ticket status (Open, In Progress, Resolved, etc.)"}
                    },
                    "required": []
                }
            },
        },
        {
            "type": "function",
            "function": {
                "name": "start_troubleshooting_flow",
                "description": "Start an interactive step-by-step troubleshooting flow for common IT issues",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "issue_type": {"type": "string", "description": "Type of issue (wifi_issues, printer_issues, email_issues)"}
                    },
                    "required": ["issue_type"]
                }
            },
        },
        {
            "type": "function",
            "function": {
                "name": "get_software_info",
                "description": "Get software version and installer link by name",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "name": {"type": "string", "description": "Software name to look up"}
                    },
                    "required": ["name"]
                }
            },
        },
        {
            "type": "function",
            "function": {
                "name": "get_helpdesk_stats",
                "description": "Get current IT helpdesk statistics and ticket summaries",
                "parameters": {
                    "type": "object",
                    "properties": {},
                    "required": []
                }
            },
        },
    ]


# Function to call a tool by its name and arguments
def call_tool_by_name(name: str, arguments_json: str) -> str:
    try:
        args = json.loads(arguments_json or "{}")  # Parse the arguments JSON
    except Exception:
        args = {}  # Default to an empty dictionary if parsing fails

    # Call the appropriate tool based on its name
    if name == "search_knowledge_base_articles":
        return search_knowledge_base_articles(
            args.get("query", ""),
            args.get("max_results", 3)
        )
    elif name == "get_enhanced_faq_answer":
        return get_enhanced_faq_answer(args.get("question", ""))
    elif name == "get_faq_answer":
        return get_faq_answer(args.get("question", ""))
    elif name == "create_ticket":
        return create_ticket(
            args.get("issue", ""),
            args.get("created_by", "user"),
            args.get("priority")
        )
    elif name == "check_ticket_status":
        return check_ticket_status(args.get("ticket_id", ""))
    elif name == "list_my_tickets":
        return list_my_tickets(
            args.get("created_by", "user"),
            args.get("status_filter")
        )
    elif name == "start_troubleshooting_flow":
        return start_troubleshooting_flow(args.get("issue_type", ""))
    elif name == "get_software_info":
        return get_software_info(args.get("name", ""))
    elif name == "get_helpdesk_stats":
        return get_helpdesk_stats()

    # Return a default response if the tool name is unknown
    return "Unknown tool"
