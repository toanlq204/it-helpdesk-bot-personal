# Import necessary modules
import json
from typing import List, Dict, Any
from .mock_data import faq_data, software_list, ticket_data


# Function to get an FAQ answer based on a question
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


# Function to create a support ticket
def create_ticket(issue: str, created_by: str = "user") -> str:
    ticket_id = f"T{len(ticket_data)+1:04d}"  # Generate a unique ticket ID
    # Add the ticket to the ticket data
    ticket_data.append({"id": ticket_id, "issue": issue,
                       "status": "Open", "created_by": created_by})
    # Return confirmation message
    return f"Ticket {ticket_id} has been created for your issue: {issue}"


# Function to get software information based on its name
def get_software_info(name: str) -> str:
    n = (name or "").lower().strip()  # Normalize the software name
    # Search for the software in the software list
    for s in software_list:
        if n in s["name"].lower():
            return f"{s['name']} (v{s['version']}): {s['installer_link']}"
    # Return default response if software is not found
    return "Software not found in the catalog."


# Function to get the schema of available tools
def get_tools_schema() -> List[Dict[str, Any]]:
    return [
        {
            "type": "function",
            "function": {
                "name": "get_faq_answer",
                "description": "Lookup an IT FAQ answer by question",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "question": {"type": "string"}
                    },
                    "required": ["question"]
                }
            },
        },
        {
            "type": "function",
            "function": {
                "name": "create_ticket",
                "description": "Create an IT support ticket with the described issue",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "issue": {"type": "string"},
                        "created_by": {"type": "string"}
                    },
                    "required": ["issue"]
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
                        "name": {"type": "string"}
                    },
                    "required": ["name"]
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
    if name == "get_faq_answer":
        return get_faq_answer(args.get("question", ""))
    if name == "create_ticket":
        return create_ticket(args.get("issue", ""), args.get("created_by", "user"))
    if name == "get_software_info":
        return get_software_info(args.get("name", ""))
    # Return a default response if the tool name is unknown
    return "Unknown tool"
