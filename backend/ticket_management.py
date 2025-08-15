# Enhanced Ticket Management System
# Provides comprehensive ticket creation, tracking, and management capabilities

import json
import uuid
from datetime import datetime, timedelta
from typing import List, Dict, Any, Optional
from enum import Enum


class TicketStatus(Enum):
    OPEN = "Open"
    IN_PROGRESS = "In Progress"
    PENDING_USER = "Pending User Response"
    RESOLVED = "Resolved"
    CLOSED = "Closed"
    CANCELLED = "Cancelled"


class TicketPriority(Enum):
    LOW = "Low"
    MEDIUM = "Medium"
    HIGH = "High"
    URGENT = "Urgent"
    CRITICAL = "Critical"


class TicketCategory(Enum):
    HARDWARE = "Hardware"
    SOFTWARE = "Software"
    NETWORK = "Network"
    EMAIL = "Email"
    SECURITY = "Security"
    ACCOUNT = "Account"
    GENERAL = "General"


# In-memory ticket storage (mock database)
ticket_database: List[Dict[str, Any]] = []

# Mock IT staff for assignment
it_staff = [
    {"id": "tech001", "name": "Alex Johnson",
        "specialties": ["Network", "Security"]},
    {"id": "tech002", "name": "Sarah Chen",
        "specialties": ["Software", "Email"]},
    {"id": "tech003", "name": "Mike Rodriguez",
        "specialties": ["Hardware", "General"]},
    {"id": "tech004", "name": "Emily Davis",
        "specialties": ["Account", "Security"]}
]


def generate_ticket_id() -> str:
    """Generate a unique ticket ID"""
    return f"INC{datetime.now().strftime('%Y%m%d')}{len(ticket_database)+1:04d}"


def auto_assign_ticket(category: str) -> str:
    """Automatically assign ticket to appropriate IT staff based on category"""
    for staff in it_staff:
        if category in staff["specialties"]:
            return staff["name"]
    return "IT Support Team"  # Default assignment


def determine_priority(issue_description: str) -> str:
    """Auto-determine ticket priority based on keywords in issue description"""
    issue_lower = issue_description.lower()

    critical_keywords = ["server down", "system crash",
                         "security breach", "cannot login", "total outage"]
    urgent_keywords = ["urgent", "asap", "critical",
                       "emergency", "broken", "not working at all"]
    high_keywords = ["important", "deadline",
                     "multiple users", "department", "slow performance"]

    for keyword in critical_keywords:
        if keyword in issue_lower:
            return TicketPriority.CRITICAL.value

    for keyword in urgent_keywords:
        if keyword in issue_lower:
            return TicketPriority.URGENT.value

    for keyword in high_keywords:
        if keyword in issue_lower:
            return TicketPriority.HIGH.value

    return TicketPriority.MEDIUM.value


def categorize_issue(issue_description: str) -> str:
    """Auto-categorize ticket based on keywords in issue description"""
    issue_lower = issue_description.lower()

    category_keywords = {
        TicketCategory.NETWORK.value: ["wifi", "vpn", "internet", "connection", "network", "dns", "ip"],
        TicketCategory.EMAIL.value: ["email", "outlook", "exchange", "mail", "smtp", "sync"],
        TicketCategory.HARDWARE.value: ["printer", "monitor", "keyboard", "mouse", "laptop", "desktop", "hardware"],
        TicketCategory.SOFTWARE.value: ["software", "application", "install", "update", "program", "app"],
        TicketCategory.SECURITY.value: ["password", "login", "access", "permission", "security", "virus", "malware"],
        TicketCategory.ACCOUNT.value: [
            "account", "user", "profile", "permissions", "access rights"]
    }

    for category, keywords in category_keywords.items():
        for keyword in keywords:
            if keyword in issue_lower:
                return category

    return TicketCategory.GENERAL.value


def create_enhanced_ticket(
    issue: str,
    created_by: str = "user",
    priority: Optional[str] = None,
    category: Optional[str] = None,
    additional_info: Optional[Dict[str, Any]] = None
) -> Dict[str, Any]:
    """
    Create an enhanced ticket with auto-categorization and priority assignment
    """
    ticket_id = generate_ticket_id()
    now = datetime.now()

    # Auto-determine priority and category if not provided
    if not priority:
        priority = determine_priority(issue)
    if not category:
        category = categorize_issue(issue)

    # Calculate estimated resolution time based on priority
    resolution_hours = {
        TicketPriority.CRITICAL.value: 2,
        TicketPriority.URGENT.value: 4,
        TicketPriority.HIGH.value: 24,
        TicketPriority.MEDIUM.value: 72,
        TicketPriority.LOW.value: 168
    }

    estimated_resolution = now + \
        timedelta(hours=resolution_hours.get(priority, 72))

    ticket = {
        "id": ticket_id,
        "issue": issue,
        "status": TicketStatus.OPEN.value,
        "priority": priority,
        "category": category,
        "created_by": created_by,
        "assigned_to": auto_assign_ticket(category),
        "created_at": now.isoformat(),
        "updated_at": now.isoformat(),
        "estimated_resolution": estimated_resolution.isoformat(),
        "comments": [],
        "resolution": None,
        "additional_info": additional_info or {}
    }

    ticket_database.append(ticket)
    return ticket


def get_ticket_status(ticket_id: str) -> Dict[str, Any]:
    """Get detailed status information for a specific ticket"""
    for ticket in ticket_database:
        if ticket["id"] == ticket_id:
            # Calculate time elapsed
            created_time = datetime.fromisoformat(ticket["created_at"])
            time_elapsed = datetime.now() - created_time

            # Check if overdue
            est_resolution = datetime.fromisoformat(
                ticket["estimated_resolution"])
            is_overdue = datetime.now() > est_resolution and ticket["status"] not in [
                TicketStatus.RESOLVED.value, TicketStatus.CLOSED.value
            ]

            return {
                "ticket": ticket,
                "time_elapsed_hours": round(time_elapsed.total_seconds() / 3600, 1),
                "is_overdue": is_overdue,
                "status_description": get_status_description(ticket["status"])
            }

    return {"error": f"Ticket {ticket_id} not found"}


def get_status_description(status: str) -> str:
    """Get human-readable status descriptions"""
    descriptions = {
        TicketStatus.OPEN.value: "Your ticket has been received and is waiting to be assigned to a technician.",
        TicketStatus.IN_PROGRESS.value: "A technician is actively working on your issue.",
        TicketStatus.PENDING_USER.value: "We need additional information from you to continue resolving this issue.",
        TicketStatus.RESOLVED.value: "The issue has been resolved. Please confirm if the solution works for you.",
        TicketStatus.CLOSED.value: "This ticket has been closed. Contact us if you need further assistance.",
        TicketStatus.CANCELLED.value: "This ticket has been cancelled at the user's request."
    }
    return descriptions.get(status, "Status unknown")


def update_ticket_status(ticket_id: str, new_status: str, comment: str = "") -> Dict[str, Any]:
    """Update ticket status with optional comment"""
    for ticket in ticket_database:
        if ticket["id"] == ticket_id:
            old_status = ticket["status"]
            ticket["status"] = new_status
            ticket["updated_at"] = datetime.now().isoformat()

            if comment:
                ticket["comments"].append({
                    "timestamp": datetime.now().isoformat(),
                    "author": "System",
                    "comment": comment
                })

            # Add status change comment
            ticket["comments"].append({
                "timestamp": datetime.now().isoformat(),
                "author": "System",
                "comment": f"Status changed from {old_status} to {new_status}"
            })

            return {"success": True, "message": f"Ticket {ticket_id} status updated to {new_status}"}

    return {"error": f"Ticket {ticket_id} not found"}


def list_user_tickets(created_by: str = "user", status_filter: Optional[str] = None) -> List[Dict[str, Any]]:
    """List tickets created by a specific user, optionally filtered by status"""
    user_tickets = [
        t for t in ticket_database if t["created_by"] == created_by]

    if status_filter:
        user_tickets = [
            t for t in user_tickets if t["status"] == status_filter]

    # Sort by creation date (newest first)
    user_tickets.sort(key=lambda x: x["created_at"], reverse=True)

    return user_tickets


def get_ticket_statistics() -> Dict[str, Any]:
    """Get statistics about all tickets"""
    if not ticket_database:
        return {"total": 0, "by_status": {}, "by_priority": {}, "by_category": {}}

    stats = {
        "total": len(ticket_database),
        "by_status": {},
        "by_priority": {},
        "by_category": {}
    }

    for ticket in ticket_database:
        # Count by status
        status = ticket["status"]
        stats["by_status"][status] = stats["by_status"].get(status, 0) + 1

        # Count by priority
        priority = ticket["priority"]
        stats["by_priority"][priority] = stats["by_priority"].get(
            priority, 0) + 1

        # Count by category
        category = ticket["category"]
        stats["by_category"][category] = stats["by_category"].get(
            category, 0) + 1

    return stats


def simulate_ticket_progress(ticket_id: str) -> Dict[str, Any]:
    """Simulate realistic ticket progress for demo purposes"""
    import random

    ticket_info = get_ticket_status(ticket_id)
    if "error" in ticket_info:
        return ticket_info

    ticket = ticket_info["ticket"]
    current_status = ticket["status"]

    # Simulate progress based on time elapsed and priority
    time_elapsed = ticket_info["time_elapsed_hours"]
    priority = ticket["priority"]

    # Define progression probability based on priority and time
    progression_chance = {
        TicketPriority.CRITICAL.value: 0.8 if time_elapsed > 1 else 0.3,
        TicketPriority.URGENT.value: 0.7 if time_elapsed > 2 else 0.2,
        TicketPriority.HIGH.value: 0.6 if time_elapsed > 12 else 0.1,
        TicketPriority.MEDIUM.value: 0.5 if time_elapsed > 24 else 0.05,
        TicketPriority.LOW.value: 0.3 if time_elapsed > 48 else 0.02
    }

    if current_status == TicketStatus.OPEN.value and random.random() < progression_chance.get(priority, 0.1):
        return update_ticket_status(ticket_id, TicketStatus.IN_PROGRESS.value,
                                    "Technician has been assigned and is reviewing the issue.")

    elif current_status == TicketStatus.IN_PROGRESS.value and random.random() < 0.4:
        if random.random() < 0.7:
            return update_ticket_status(ticket_id, TicketStatus.RESOLVED.value,
                                        "Issue has been resolved. Please test and confirm the solution works.")
        else:
            return update_ticket_status(ticket_id, TicketStatus.PENDING_USER.value,
                                        "We need additional information to continue troubleshooting.")

    return {"message": f"No status change for ticket {ticket_id} at this time."}

# Initialize with some sample tickets for demo


def initialize_sample_tickets():
    """Initialize the system with some sample tickets for demonstration"""
    if not ticket_database:  # Only initialize if empty
        sample_tickets = [
            {
                "issue": "Laptop is running very slowly after Windows update",
                "created_by": "john.doe@company.com",
                "priority": TicketPriority.HIGH.value
            },
            {
                "issue": "Cannot connect to VPN from home office",
                "created_by": "jane.smith@company.com",
                "priority": TicketPriority.URGENT.value
            },
            {
                "issue": "Printer in conference room is not working",
                "created_by": "mike.johnson@company.com"
            }
        ]

        for sample in sample_tickets:
            create_enhanced_ticket(**sample)


# Initialize sample data
initialize_sample_tickets()
