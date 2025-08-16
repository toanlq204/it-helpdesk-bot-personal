# Enhanced IT Helpdesk Bot Functions
# Consolidated and optimized function calling system

import json
from typing import List, Dict, Any
from .knowledge_base import (
    search_knowledge_base,
    search_enhanced_faq,
    get_troubleshooting_flow,
    get_available_flows
)
from .ticket_management import (
    create_enhanced_ticket,
    get_ticket_status,
    list_user_tickets,
    get_ticket_statistics,
    simulate_ticket_progress
)

# Import new unified knowledge base functionality
try:
    from .tools.knowledge_handler import query_it_knowledge
    VECTOR_STORE_AVAILABLE = True
except ImportError:
    VECTOR_STORE_AVAILABLE = False
    print("Vector store not available, using legacy knowledge base")


def search_knowledge_with_vector_store(query: str, collection: str = None) -> str:
    """Search knowledge base using vector store for relevant IT information"""
    if not VECTOR_STORE_AVAILABLE:
        # Fallback to legacy knowledge base if vector store is not available
        return search_knowledge_base_articles(query, 3)

    try:
        context = query_it_knowledge(query, collection)

        if "No relevant knowledge found" in context or "Error" in context:
            # Fallback to legacy search if vector store fails
            return search_knowledge_base_articles(query, 3)

        return context + "\n\n💡 This information comes from our comprehensive IT knowledge base. Would you like more specific details about any of these topics?"

    except Exception as e:
        # Fallback to legacy search on any error
        print(f"Vector store error, using fallback: {e}")
        return search_knowledge_base_articles(query, 3)


# Workshop 4 Enhanced Functions
def search_enhanced_vector_store(query: str, namespace: str = None) -> str:
    """Enhanced vector search using Pinecone (Workshop 4) with improved relevance filtering"""
    try:
        from .tools.pinecone_handler import query_pinecone_knowledge

        # Use the improved query function with better filtering
        result = query_pinecone_knowledge(query, namespace, max_results=3)

        # Check if we got meaningful results
        if "No relevant knowledge found" in result or "No highly relevant information found" in result:
            # Try with broader search if no results
            if namespace:
                # Try searching all namespaces if specific namespace had no results
                result = query_pinecone_knowledge(query, None, max_results=3)

        if "No relevant knowledge found" in result or "No highly relevant information found" in result:
            return "I couldn't find relevant information in our knowledge base for your specific query. Please try rephrasing your question or ask for help with a specific IT topic like 'VPN setup', 'password reset', or 'network troubleshooting'."

        return result + "\n\n🚀 **Enhanced with Workshop 4 Pinecone Vector Search**"
    except ImportError:
        # Fallback to vector store
        return search_knowledge_with_vector_store(query)
    except Exception as e:
        # Fallback to legacy search
        print(f"Enhanced vector search error: {e}")
        return search_knowledge_base_articles(query, 3)


def enhanced_rag_response(query: str, session_id: str = "default") -> str:
    """Enhanced RAG using LangChain (Workshop 4)"""
    try:
        from .tools.langchain_manager import enhanced_rag_query
        result = enhanced_rag_query(query, session_id)
        return result + "\n\n🔗 **Enhanced with Workshop 4 LangChain RAG**"
    except ImportError:
        # Fallback to basic search
        return search_knowledge_with_vector_store(query)
    except Exception as e:
        # Fallback to legacy search
        return search_knowledge_base_articles(query, 3)


def agent_function_call(query: str, session_id: str = "default") -> str:
    """Enhanced function calling using agents (Workshop 4)"""
    try:
        from .tools.enhanced_function_handler import enhanced_function_call
        result = enhanced_function_call(query, session_id)
        return result + "\n\n🤖 **Enhanced with Workshop 4 Agent Function Calling**"
    except ImportError:
        # Fallback to regular function calling
        return "Enhanced function calling not available. Using legacy mode."
    except Exception as e:
        return f"Enhanced function calling error: {e}"


def search_knowledge_base_articles(query: str, max_results: int = 3) -> str:
    """Search comprehensive knowledge base for relevant IT help articles"""
    results = search_knowledge_base(query, max_results)

    if not results:
        return f"No knowledge base articles found for '{query}'. Would you like me to create a support ticket or try a different search?"

    response = f"Found {len(results)} relevant knowledge base articles:\n\n"

    for i, article in enumerate(results, 1):
        summary = article['content'][:200].replace('\n', ' ')
        if len(article['content']) > 200:
            summary += "..."
        response += f"**{i}. {article['title']}** ({article['category']})\n{summary}\n📖 ID: {article['id']}\n\n"

    response += "Would you like me to provide full details for any of these articles?"
    return response


def get_enhanced_faq_answer(question: str) -> str:
    """Search enhanced FAQ database with better matching"""
    results = search_enhanced_faq(question, max_results=3)

    if not results:
        return get_faq_answer(question)  # Fallback to legacy FAQ

    if len(results) == 1:
        faq = results[0]
        return f"**{faq['question']}**\n\n{faq['answer']}\n\n💡 Category: {faq['category']}"

    response = f"I found {len(results)} relevant FAQs:\n\n"
    for i, faq in enumerate(results, 1):
        response += f"**{i}. {faq['question']}**\n{faq['answer'][:100]}...\n\n"

    return response + "Which of these is most relevant to your question?"


def get_faq_answer(question: str) -> str:
    """Legacy FAQ search for backward compatibility - now uses enhanced FAQ"""
    return get_enhanced_faq_answer(question)


def create_ticket(issue: str, created_by: str = "user", priority: str = None) -> str:
    """Create an enhanced support ticket with auto-categorization"""
    if not issue.strip():
        return "Please provide a description of the issue to create a ticket."

    ticket = create_enhanced_ticket(issue, created_by, priority)

    return (
        f"✅ **Ticket {ticket['id']} Created Successfully**\n\n"
        f"📝 **Issue:** {ticket['issue']}\n"
        f"🏷️ **Category:** {ticket['category']}\n"
        f"⚡ **Priority:** {ticket['priority']}\n"
        f"👤 **Assigned to:** {ticket['assigned_to']}\n"
        f"📅 **Created:** {ticket['created_at'][:19].replace('T', ' ')}\n"
        f"⏰ **Estimated Resolution:** {ticket['estimated_resolution'][:19].replace('T', ' ')}\n\n"
        f"You can check the status anytime by asking about ticket {ticket['id']}."
    )


def check_ticket_status(ticket_id: str) -> str:
    """Get detailed status information for a specific ticket"""
    if not ticket_id.strip():
        return "Please provide a valid ticket ID."

    # Simulate progress for demo
    simulate_ticket_progress(ticket_id)
    status_info = get_ticket_status(ticket_id)

    if "error" in status_info:
        return status_info["error"]

    ticket = status_info["ticket"]
    response = (
        f"🎫 **Ticket {ticket['id']} Status**\n\n"
        f"📝 **Issue:** {ticket['issue']}\n"
        f"📊 **Status:** {ticket['status']}\n"
        f"⚡ **Priority:** {ticket['priority']}\n"
        f"👤 **Assigned to:** {ticket['assigned_to']}\n"
        f"⏱️ **Time Elapsed:** {status_info['time_elapsed_hours']} hours\n"
    )

    if status_info['is_overdue']:
        response += "⚠️ **OVERDUE** - This ticket has exceeded the estimated resolution time.\n"

    response += f"\n📋 **Status Description:** {status_info['status_description']}\n"

    if ticket['comments']:
        response += "\n💬 **Recent Updates:**\n"
        for comment in ticket['comments'][-3:]:
            timestamp = comment['timestamp'][:19].replace('T', ' ')
            response += f"• {timestamp} - {comment['author']}: {comment['comment']}\n"

    return response


def list_my_tickets(created_by: str = "user", status_filter: str = None) -> str:
    """List tickets created by the user"""
    tickets = list_user_tickets(created_by, status_filter)

    if not tickets:
        filter_text = f" with status '{status_filter}'" if status_filter else ""
        return f"No tickets found{filter_text}. Would you like to create a new support ticket?"

    response = f"📋 **Your Support Tickets** ({len(tickets)} found)\n\n"

    for ticket in tickets:
        created_date = ticket['created_at'][:10]
        issue_preview = ticket['issue'][:60] + \
            ('...' if len(ticket['issue']) > 60 else '')
        response += (
            f"🎫 **{ticket['id']}** - {ticket['status']}\n"
            f"   📝 {issue_preview}\n"
            f"   📅 Created: {created_date} | Priority: {ticket['priority']}\n\n"
        )

    return response + "Ask me about any specific ticket ID for detailed status information."


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

    response = f"🛠️ **Starting {flow['title']}**\n\nLet's work through this step by step:\n\n**Step 1:** {first_step['question']}\n\n"

    if first_step['type'] == 'yes_no':
        response += "Please answer: **Yes** or **No**"
    elif first_step['type'] == 'multiple_choice':
        response += "Please choose from:\n"
        for i, option in enumerate(first_step['options'], 1):
            response += f"{i}. {option['text']}\n"

    return response


def get_software_info(name: str) -> str:
    """Get software version and installer link by name"""
    if not name.strip():
        return "Please provide a software name to search for."

    # Basic software catalog (inline data for legacy compatibility)
    software_catalog = [
        {"name": "Outlook", "version": "2024.1",
            "installer_link": "https://company.example/install/outlook"},
        {"name": "Zoom", "version": "6.5",
            "installer_link": "https://company.example/install/zoom"},
        {"name": "VSCode", "version": "1.92",
            "installer_link": "https://company.example/install/vscode"},
    ]

    n = name.lower().strip()
    for software in software_catalog:
        if n in software["name"].lower():
            return f"{software['name']} (v{software['version']}): {software['installer_link']}"

    return "Software not found in the catalog. Please contact IT for assistance with other software installations."


def get_helpdesk_stats() -> str:
    """Get current helpdesk statistics"""
    stats = get_ticket_statistics()

    if stats['total'] == 0:
        return "📊 **IT Helpdesk Statistics**\n\nNo tickets in the system currently."

    response = f"📊 **IT Helpdesk Statistics**\n\n📋 **Total Tickets:** {stats['total']}\n\n"

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


# Tool schema configuration
def get_tools_schema() -> List[Dict[str, Any]]:
    """Get the schema of available tools for the AI assistant"""
    return [
        {
            "type": "function",
            "function": {
                "name": "search_knowledge_base_articles",
                "description": "Search comprehensive knowledge base for detailed IT help articles",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "query": {"type": "string", "description": "Search query for knowledge base articles"},
                        "max_results": {"type": "integer", "description": "Maximum articles to return (default: 3)"}
                    },
                    "required": ["query"]
                }
            },
        },
        {
            "type": "function",
            "function": {
                "name": "get_enhanced_faq_answer",
                "description": "Search enhanced FAQ database with better matching",
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
                "description": "Create an IT support ticket with auto-categorization and priority assignment",
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
                        "status_filter": {"type": "string", "description": "Filter by ticket status"}
                    },
                    "required": []
                }
            },
        },
        {
            "type": "function",
            "function": {
                "name": "start_troubleshooting_flow",
                "description": "Start interactive step-by-step troubleshooting for common IT issues",
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
        {
            "type": "function",
            "function": {
                "name": "search_knowledge_with_vector_store",
                "description": "Search comprehensive IT knowledge base using Pinecone vector store for FAQs, software guides, and IT policies",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "query": {"type": "string", "description": "Search query for knowledge base"},
                        "collection": {"type": "string", "description": "Specific collection to search (faqs, software, policies) or leave empty for all"}
                    },
                    "required": ["query"]
                }
            },
        },
        # Workshop 4 Enhanced Tools
        {
            "type": "function",
            "function": {
                "name": "search_enhanced_vector_store",
                "description": "Enhanced vector search using Pinecone for superior knowledge retrieval (Workshop 4)",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "query": {"type": "string", "description": "Search query for vector database"},
                        "namespace": {"type": "string", "description": "Specific namespace (faqs, kb_articles, policies, troubleshooting) or leave empty for all"}
                    },
                    "required": ["query"]
                }
            },
        },
        {
            "type": "function",
            "function": {
                "name": "enhanced_rag_response",
                "description": "Enhanced RAG response using LangChain for conversational context (Workshop 4)",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "query": {"type": "string", "description": "User query for RAG processing"},
                        "session_id": {"type": "string", "description": "Session ID for conversation context"}
                    },
                    "required": ["query"]
                }
            },
        },
        {
            "type": "function",
            "function": {
                "name": "agent_function_call",
                "description": "Enhanced function calling using AI agents for complex task execution (Workshop 4)",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "query": {"type": "string", "description": "Complex query for agent processing"},
                        "session_id": {"type": "string", "description": "Session ID for agent context"}
                    },
                    "required": ["query"]
                }
            },
        },
    ]


# Function dispatcher
def call_tool_by_name(name: str, arguments_json: str) -> str:
    """Call a tool function by name with JSON arguments"""
    try:
        args = json.loads(arguments_json or "{}")
    except json.JSONDecodeError:
        return "Error: Invalid JSON arguments provided."

    # Function mapping for cleaner dispatch
    function_map = {
        "search_knowledge_base_articles": lambda: search_knowledge_base_articles(
            args.get("query", ""),
            args.get("max_results", 3)
        ),
        "get_enhanced_faq_answer": lambda: get_enhanced_faq_answer(args.get("question", "")),
        "get_faq_answer": lambda: get_faq_answer(args.get("question", "")),
        "create_ticket": lambda: create_ticket(
            args.get("issue", ""),
            args.get("created_by", "user"),
            args.get("priority")
        ),
        "check_ticket_status": lambda: check_ticket_status(args.get("ticket_id", "")),
        "list_my_tickets": lambda: list_my_tickets(
            args.get("created_by", "user"),
            args.get("status_filter")
        ),
        "start_troubleshooting_flow": lambda: start_troubleshooting_flow(args.get("issue_type", "")),
        "get_software_info": lambda: get_software_info(args.get("name", "")),
        "get_helpdesk_stats": lambda: get_helpdesk_stats(),
        "search_knowledge_with_vector_store": lambda: search_knowledge_with_vector_store(
            args.get("query", ""),
            args.get("collection")
        ),
        # Workshop 4 Enhanced Functions
        "search_enhanced_vector_store": lambda: search_enhanced_vector_store(
            args.get("query", ""),
            args.get("namespace")
        ),
        "enhanced_rag_response": lambda: enhanced_rag_response(
            args.get("query", ""),
            args.get("session_id", "default")
        ),
        "agent_function_call": lambda: agent_function_call(
            args.get("query", ""),
            args.get("session_id", "default")
        )
    }

    if name in function_map:
        try:
            return function_map[name]()
        except Exception as e:
            return f"Error executing {name}: {str(e)}"

    return f"Unknown tool: {name}"
