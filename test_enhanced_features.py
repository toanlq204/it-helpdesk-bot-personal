# Enhanced IT Helpdesk Bot - Test Cases and Examples
# This file demonstrates all the advanced features implemented

"""
TEST CASES FOR ENHANCED IT HELPDESK BOT

This file contains test scenarios that showcase the advanced capabilities:
1. Dynamic Knowledge Base Search
2. Multi-Turn Context Memory
3. Interactive Troubleshooting Flows
4. Enhanced Ticket Management
5. Batch Request Handling

To test these features, start the backend server and send these example messages.
"""

import json
import requests
from typing import Dict, Any, List

# Configuration
BASE_URL = "http://localhost:8000"
SESSION_ID = "test-session-enhanced"


def send_chat_message(message: str, session_id: str = SESSION_ID) -> Dict[str, Any]:
    """Send a chat message to the bot and return the response"""
    response = requests.post(
        f"{BASE_URL}/chat",
        json={
            "session_id": session_id,
            "message": message
        }
    )
    return response.json()


def print_response(response: Dict[str, Any]) -> None:
    """Pretty print the bot response"""
    print("="*60)
    print("BOT RESPONSE:")
    print("-"*60)
    print(response.get("reply", "No reply"))
    print("="*60)
    print()

# Test Case 1: Dynamic Knowledge Base Search


def test_knowledge_base_search():
    """Test the enhanced knowledge base search functionality"""
    print("🔍 TESTING KNOWLEDGE BASE SEARCH")
    print("="*50)

    test_queries = [
        "How to fix slow Wi-Fi connection?",
        "My printer is not working",
        "Outlook email not syncing",
        "Cannot install software on Windows",
        "VPN connection issues",
        "Computer running slowly after update"
    ]

    for query in test_queries:
        print(f"Query: {query}")
        response = send_chat_message(query)
        print_response(response)

# Test Case 2: Multi-Turn Context Memory


def test_context_memory():
    """Test multi-turn conversation with context awareness"""
    print("🧠 TESTING MULTI-TURN CONTEXT MEMORY")
    print("="*50)

    # Start with an initial issue
    print("Step 1: Report initial issue")
    response1 = send_chat_message("My laptop WiFi keeps disconnecting")
    print_response(response1)

    # Follow up with context-aware queries
    print("Step 2: Follow-up - that didn't work")
    response2 = send_chat_message("That didn't work")
    print_response(response2)

    print("Step 3: Follow-up - need more help")
    response3 = send_chat_message("What else can I try?")
    print_response(response3)

    print("Step 4: Follow-up - clarification")
    response4 = send_chat_message("What do you mean by network adapter?")
    print_response(response4)

# Test Case 3: Interactive Troubleshooting Flows


def test_troubleshooting_flows():
    """Test interactive step-by-step troubleshooting"""
    print("🛠️ TESTING TROUBLESHOOTING FLOWS")
    print("="*50)

    # Test Wi-Fi troubleshooting flow
    print("Starting Wi-Fi troubleshooting flow:")
    response1 = send_chat_message("Start Wi-Fi troubleshooting")
    print_response(response1)

    # Test printer troubleshooting flow
    print("Starting printer troubleshooting flow:")
    response2 = send_chat_message("My printer won't print anything")
    print_response(response2)

    # Test email troubleshooting flow
    print("Starting email troubleshooting flow:")
    response3 = send_chat_message("Help me troubleshoot Outlook problems")
    print_response(response3)

# Test Case 4: Enhanced Ticket Management


def test_ticket_management():
    """Test advanced ticket creation and management"""
    print("🎫 TESTING ENHANCED TICKET MANAGEMENT")
    print("="*50)

    # Create tickets with different priorities
    ticket_scenarios = [
        "Server is completely down and no one can access email",  # Should be Critical
        "My laptop screen is flickering urgently need help",      # Should be Urgent
        "Need to install new software for the accounting team",   # Should be Medium
        "Printer in break room making weird noises"               # Should be Low
    ]

    ticket_ids = []

    for scenario in ticket_scenarios:
        print(f"Creating ticket: {scenario}")
        response = send_chat_message(f"Create a ticket: {scenario}")
        print_response(response)

        # Extract ticket ID from response (simple extraction for demo)
        reply = response.get("reply", "")
        if "Ticket" in reply and "Created" in reply:
            # Try to extract ticket ID
            import re
            match = re.search(r'Ticket (\w+)', reply)
            if match:
                ticket_ids.append(match.group(1))

    # Check ticket statuses
    print("\nChecking ticket statuses:")
    for ticket_id in ticket_ids:
        if ticket_id:
            print(f"Checking status of {ticket_id}")
            response = send_chat_message(
                f"What's the status of ticket {ticket_id}?")
            print_response(response)

    # List all user tickets
    print("Listing all my tickets:")
    response = send_chat_message("Show me all my tickets")
    print_response(response)

# Test Case 5: Batch Request Handling


def test_batch_requests():
    """Test handling multiple questions in one request"""
    print("📦 TESTING BATCH REQUEST HANDLING")
    print("="*50)

    batch_queries = [
        "How do I reset my password? Also, how can I connect to the VPN?",
        "I need help with printer setup and also my Outlook is not syncing. Can you help with both?",
        "What's the WiFi password? How do I install Zoom? Also, where can I download Office 365?",
        "My computer is slow. I also can't print. Another issue is my email won't send.",
    ]

    for query in batch_queries:
        print(f"Batch Query: {query}")
        response = send_chat_message(query)
        print_response(response)

# Test Case 6: Advanced Search and FAQ


def test_advanced_search():
    """Test enhanced FAQ and knowledge base search"""
    print("🔎 TESTING ADVANCED SEARCH CAPABILITIES")
    print("="*50)

    search_scenarios = [
        "password reset steps",
        "VPN connection troubleshooting",
        "email sync problems",
        "printer driver installation",
        "software installation errors",
        "network connectivity issues"
    ]

    for scenario in search_scenarios:
        print(f"Searching for: {scenario}")
        response = send_chat_message(f"Search knowledge base for {scenario}")
        print_response(response)

# Test Case 7: System Statistics and Health


def test_system_stats():
    """Test system statistics and health endpoints"""
    print("📊 TESTING SYSTEM STATISTICS")
    print("="*50)

    # Test health endpoint
    print("Health Check:")
    health_response = requests.get(f"{BASE_URL}/health")
    print(json.dumps(health_response.json(), indent=2))
    print()

    # Test stats endpoint
    print("System Statistics:")
    try:
        stats_response = requests.get(f"{BASE_URL}/stats")
        print(json.dumps(stats_response.json(), indent=2))
    except:
        print("Stats endpoint may not be available")
    print()

    # Get helpdesk stats via chat
    print("Helpdesk Statistics via Chat:")
    response = send_chat_message("Show me helpdesk statistics")
    print_response(response)

# Test Case 8: Edge Cases and Error Handling


def test_edge_cases():
    """Test edge cases and error handling"""
    print("⚠️ TESTING EDGE CASES")
    print("="*50)

    edge_cases = [
        "",  # Empty message
        "Invalid ticket ID: INVALID123",  # Invalid ticket lookup
        "Start troubleshooting for invalid_issue_type",  # Invalid flow type
        "???",  # Unclear query
        "Help" * 100,  # Very long message
    ]

    for case in edge_cases:
        if case.strip():  # Skip empty message for now
            print(f"Edge Case: {case[:50]}{'...' if len(case) > 50 else ''}")
            try:
                response = send_chat_message(case)
                print_response(response)
            except Exception as e:
                print(f"Error: {e}")
                print()


def run_all_tests():
    """Run all test cases"""
    print("🚀 STARTING ENHANCED IT HELPDESK BOT TESTS")
    print("="*60)
    print()

    try:
        test_knowledge_base_search()
        test_context_memory()
        test_troubleshooting_flows()
        test_ticket_management()
        test_batch_requests()
        test_advanced_search()
        test_system_stats()
        test_edge_cases()

        print("✅ ALL TESTS COMPLETED!")
        print("="*60)

    except requests.exceptions.ConnectionError:
        print("❌ ERROR: Cannot connect to the backend server.")
        print("Please make sure the backend is running on http://localhost:8000")
    except Exception as e:
        print(f"❌ ERROR: {e}")


if __name__ == "__main__":
    # Example usage:
    print("Enhanced IT Helpdesk Bot - Test Suite")
    print("Please ensure the backend server is running before running tests.")
    print()

    # Uncomment the line below to run all tests
    # run_all_tests()

    # Or run individual test cases:
    print("Available test functions:")
    print("- test_knowledge_base_search()")
    print("- test_context_memory()")
    print("- test_troubleshooting_flows()")
    print("- test_ticket_management()")
    print("- test_batch_requests()")
    print("- test_advanced_search()")
    print("- test_system_stats()")
    print("- test_edge_cases()")
    print("- run_all_tests()")
