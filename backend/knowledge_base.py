# Advanced Knowledge Base for IT Helpdesk
# Contains comprehensive IT help articles, FAQs, and troubleshooting guides

import json
from typing import List, Dict, Any
from datetime import datetime

# Comprehensive IT Knowledge Base Articles
knowledge_base_articles = [
    {
        "id": "kb001",
        "title": "Password Reset Guide",
        "category": "Authentication",
        "tags": ["password", "reset", "login", "security"],
        "content": "Step-by-step password reset process:\n1. Go to the IT portal (portal.company.com)\n2. Click 'Forgot Password' or 'Reset Password'\n3. Enter your username or email address\n4. Check your email for the reset link (may take 5-10 minutes)\n5. Click the link and create a new password\n6. Password must be 8+ characters with uppercase, lowercase, numbers, and symbols\n7. Confirm the new password\n8. Try logging in with your new credentials",
        "related_issues": ["login_failed", "account_locked", "two_factor"],
        "last_updated": "2024-01-15"
    },
    {
        "id": "kb002",
        "title": "VPN Connection Troubleshooting",
        "category": "Network",
        "tags": ["vpn", "connection", "remote", "network", "cisco"],
        "content": "VPN troubleshooting steps:\n1. Check your internet connection (try browsing other websites)\n2. Ensure VPN client is updated to the latest version\n3. Restart the VPN application completely\n4. Try connecting to a different VPN server location\n5. Disable Windows firewall temporarily to test\n6. Clear DNS cache: Open Command Prompt as admin, run 'ipconfig /flushdns'\n7. Reset network adapters: 'netsh winsock reset' and restart computer\n8. Check with network admin about server maintenance\n9. If using corporate laptop, ensure company certificates are installed",
        "related_issues": ["slow_connection", "dns_issues", "firewall_blocking"],
        "last_updated": "2024-01-20"
    },
    {
        "id": "kb003",
        "title": "Email Setup and Synchronization",
        "category": "Email",
        "tags": ["outlook", "email", "sync", "exchange", "office365"],
        "content": "Outlook email setup and sync issues:\n1. Verify internet connection and Exchange server status\n2. Check mailbox storage limits (may be full)\n3. Re-authenticate your account:\n   - File > Account Settings > Account Settings\n   - Select your account > Change > Next > Done\n4. Repair Outlook data file:\n   - Close Outlook\n   - Run scanpst.exe from Office installation folder\n5. Create new Outlook profile if corruption suspected\n6. For Office 365: Sign out and sign back in\n7. Check for Outlook updates\n8. Disable antivirus email scanning temporarily\n9. Contact IT if server settings need verification",
        "related_issues": ["slow_email", "missing_emails", "send_receive_errors"],
        "last_updated": "2024-01-18"
    },
    {
        "id": "kb004",
        "title": "Wi-Fi Connection and Speed Issues",
        "category": "Network",
        "tags": ["wifi", "wireless", "slow", "connection", "network"],
        "content": "Wi-Fi troubleshooting guide:\n1. Check signal strength (move closer to router if weak)\n2. Restart your device's Wi-Fi adapter:\n   - Disable and re-enable Wi-Fi\n   - Or restart network adapter in Device Manager\n3. 'Forget' and reconnect to the network:\n   - Settings > Network > Wi-Fi > Manage Known Networks\n   - Select network > Forget > Reconnect with password\n4. Update Wi-Fi drivers:\n   - Device Manager > Network Adapters > Right-click Wi-Fi adapter > Update driver\n5. Reset network settings (Windows): 'netsh int ip reset' and 'netsh winsock reset'\n6. Change DNS servers to 8.8.8.8 and 8.8.4.4\n7. Check for interference from other devices\n8. Contact network admin about router/access point issues",
        "related_issues": ["no_internet", "slow_browsing", "frequent_disconnects"],
        "last_updated": "2024-01-22"
    },
    {
        "id": "kb005",
        "title": "Printer Setup and Troubleshooting",
        "category": "Hardware",
        "tags": ["printer", "printing", "driver", "network", "hp", "canon"],
        "content": "Printer setup and common issues:\n1. Install printer drivers:\n   - Download latest drivers from manufacturer website\n   - Or use Windows Update to find drivers automatically\n2. Add network printer:\n   - Settings > Devices > Printers & Scanners > Add printer\n   - Select 'The printer that I want isn't listed'\n   - Enter printer IP address or name\n3. Troubleshoot print jobs:\n   - Check printer queue for stuck jobs\n   - Restart Print Spooler service\n   - Clear print queue: Cancel all documents\n4. Paper jam resolution:\n   - Turn off printer, remove all paper carefully\n   - Check for torn pieces, clean rollers\n   - Reload paper properly\n5. Print quality issues:\n   - Clean print heads\n   - Check ink/toner levels\n   - Align print heads through printer software",
        "related_issues": ["print_queue_stuck", "poor_quality", "paper_jams"],
        "last_updated": "2024-01-25"
    },
    {
        "id": "kb006",
        "title": "Software Installation and Updates",
        "category": "Software",
        "tags": ["install", "software", "update", "administrator", "permissions"],
        "content": "Software installation troubleshooting:\n1. Run installer as Administrator:\n   - Right-click installer > 'Run as administrator'\n2. Check system requirements:\n   - Verify OS compatibility, RAM, disk space\n3. Temporarily disable antivirus during installation\n4. Clear temporary files:\n   - Run Disk Cleanup or CCleaner\n   - Clear browser cache if web-based installer\n5. Use Windows troubleshooter:\n   - Settings > Update & Security > Troubleshoot > Additional troubleshooters\n6. Check Windows installer service:\n   - services.msc > Windows Installer > Start if stopped\n7. Download fresh installer if corruption suspected\n8. For corporate software, contact IT for deployment packages\n9. Check Group Policy restrictions with IT admin",
        "related_issues": ["install_failed", "permission_denied", "corrupted_installer"],
        "last_updated": "2024-01-28"
    }
]

# Enhanced FAQ data with more comprehensive coverage
enhanced_faq_data = [
    {
        "id": "faq001",
        "question": "How do I reset my password?",
        "answer": "Visit the IT portal at portal.company.com, click 'Forgot Password', enter your username, and check your email for reset instructions. The new password must be 8+ characters with mixed case, numbers, and symbols.",
        "category": "Authentication",
        "related_kb": ["kb001"]
    },
    {
        "id": "faq002",
        "question": "VPN is not connecting",
        "answer": "First check your internet connection, then restart the VPN client. If that doesn't work, try a different server location or contact IT to verify server status.",
        "category": "Network",
        "related_kb": ["kb002"]
    },
    {
        "id": "faq003",
        "question": "How to install Outlook?",
        "answer": "Download Outlook from the Office 365 portal, run the installer as administrator, and sign in with your corporate account. Contact IT if you need help with server settings.",
        "category": "Email",
        "related_kb": ["kb003"]
    },
    {
        "id": "faq004",
        "question": "Email not syncing",
        "answer": "Check if your mailbox is full, verify internet connection, and try re-authenticating your account in Outlook settings. You may also need to repair your Outlook data file.",
        "category": "Email",
        "related_kb": ["kb003"]
    },
    {
        "id": "faq005",
        "question": "Wi-Fi is slow or not working",
        "answer": "Move closer to the router, restart your Wi-Fi adapter, or 'forget' and reconnect to the network. You can also try updating your Wi-Fi drivers.",
        "category": "Network",
        "related_kb": ["kb004"]
    },
    {
        "id": "faq006",
        "question": "Printer not working",
        "answer": "Check if the printer is on and connected, clear any paper jams, and verify the printer drivers are installed. You may need to restart the Print Spooler service.",
        "category": "Hardware",
        "related_kb": ["kb005"]
    },
    {
        "id": "faq007",
        "question": "Can't install software",
        "answer": "Try running the installer as administrator, check system requirements, and temporarily disable antivirus software. Clear temporary files and download a fresh installer if needed.",
        "category": "Software",
        "related_kb": ["kb006"]
    },
    {
        "id": "faq008",
        "question": "Computer is running slow",
        "answer": "Close unnecessary programs, run disk cleanup, check for malware, and restart your computer. Consider checking Task Manager for high CPU/memory usage processes.",
        "category": "Performance",
        "related_kb": []
    },
    {
        "id": "faq009",
        "question": "How to connect to company Wi-Fi?",
        "answer": "Select the company network, enter your domain credentials (DOMAIN\\username), and contact IT if you need the Wi-Fi password or certificate installation.",
        "category": "Network",
        "related_kb": ["kb004"]
    },
    {
        "id": "faq010",
        "question": "Two-factor authentication setup",
        "answer": "Download Microsoft Authenticator app, scan the QR code from your account settings, and enter the verification code. Keep backup codes in a safe place.",
        "category": "Authentication",
        "related_kb": ["kb001"]
    }
]

# Troubleshooting flows for interactive step-by-step guidance
troubleshooting_flows = {
    "wifi_issues": {
        "title": "Wi-Fi Connection Troubleshooting",
        "steps": [
            {
                "id": 1,
                "question": "Can you see the Wi-Fi network in your available networks list?",
                "yes_next": 2,
                "no_next": "wifi_not_visible",
                "type": "yes_no"
            },
            {
                "id": 2,
                "question": "When you try to connect, what happens?",
                "options": [
                    {"text": "It asks for a password", "next": 3},
                    {"text": "It says 'Can't connect'",
                        "next": "connection_failed"},
                    {"text": "It connects but no internet",
                        "next": "connected_no_internet"},
                    {"text": "Nothing happens", "next": "no_response"}
                ],
                "type": "multiple_choice"
            },
            {
                "id": 3,
                "question": "Do you have the correct Wi-Fi password?",
                "yes_next": 4,
                "no_next": "get_password",
                "type": "yes_no"
            },
            {
                "id": 4,
                "question": "After entering the password, does it connect successfully?",
                "yes_next": "success",
                "no_next": "wrong_password",
                "type": "yes_no"
            }
        ],
        "solutions": {
            "wifi_not_visible": "The network might be hidden or your Wi-Fi adapter may need to be restarted. Try: 1) Restart Wi-Fi adapter 2) Manually add the network 3) Check if others can see it",
            "connection_failed": "Try forgetting the network and reconnecting, or restart your device. The network might be full or having issues.",
            "connected_no_internet": "This suggests a DNS or gateway issue. Try: 1) Restart router 2) Change DNS to 8.8.8.8 3) Contact network admin",
            "no_response": "Your Wi-Fi adapter might need drivers updated or the service restarted.",
            "get_password": "Contact your IT administrator or network owner for the correct Wi-Fi password.",
            "wrong_password": "Double-check the password for typos. It may be case-sensitive. Contact IT if you're sure it's correct.",
            "success": "Great! Your Wi-Fi should now be working. If you experience slow speeds, try moving closer to the router."
        }
    },
    "printer_issues": {
        "title": "Printer Troubleshooting",
        "steps": [
            {
                "id": 1,
                "question": "Is your printer powered on and showing ready status?",
                "yes_next": 2,
                "no_next": "printer_off",
                "type": "yes_no"
            },
            {
                "id": 2,
                "question": "What type of connection does your printer use?",
                "options": [
                    {"text": "USB cable", "next": 3},
                    {"text": "Wi-Fi/Wireless", "next": 4},
                    {"text": "Ethernet/Wired network", "next": 5},
                    {"text": "I'm not sure", "next": "check_connection"}
                ],
                "type": "multiple_choice"
            },
            {
                "id": 3,
                "question": "Is the USB cable firmly connected to both computer and printer?",
                "yes_next": 6,
                "no_next": "reconnect_usb",
                "type": "yes_no"
            },
            {
                "id": 4,
                "question": "Is the printer connected to the same Wi-Fi network as your computer?",
                "yes_next": 6,
                "no_next": "wifi_setup",
                "type": "yes_no"
            },
            {
                "id": 5,
                "question": "Is the ethernet cable connected and the network light on the printer lit?",
                "yes_next": 6,
                "no_next": "check_ethernet",
                "type": "yes_no"
            },
            {
                "id": 6,
                "question": "Can you see your printer in Settings > Printers & Scanners?",
                "yes_next": 7,
                "no_next": "add_printer",
                "type": "yes_no"
            },
            {
                "id": 7,
                "question": "When you try to print, what happens?",
                "options": [
                    {"text": "Nothing prints", "next": "check_queue"},
                    {"text": "Print quality is poor", "next": "quality_issues"},
                    {"text": "Paper jam error", "next": "paper_jam"},
                    {"text": "Out of ink/toner error", "next": "replace_supplies"}
                ],
                "type": "multiple_choice"
            }
        ],
        "solutions": {
            "printer_off": "Turn on your printer and wait for it to complete startup. Check if there are any error lights or messages on the display.",
            "reconnect_usb": "Disconnect and reconnect the USB cable. Try a different USB port on your computer. The cable might be faulty.",
            "wifi_setup": "Use your printer's menu to connect to Wi-Fi, or run the printer's wireless setup wizard from the manufacturer's software.",
            "check_ethernet": "Check ethernet cable connections. Try a different cable or port on your router/switch.",
            "check_connection": "Look at the back of your printer for cables, or check the printer menu for network/connection status.",
            "add_printer": "Go to Settings > Printers & Scanners > Add printer. If it doesn't appear automatically, select 'The printer that I want isn't listed'.",
            "check_queue": "Open the print queue and cancel any stuck jobs. Restart the Print Spooler service if needed.",
            "quality_issues": "Clean print heads, check ink/toner levels, and run printer alignment from the printer software.",
            "paper_jam": "Turn off printer, carefully remove jammed paper, check for torn pieces, and reload paper properly.",
            "replace_supplies": "Replace ink cartridges or toner as indicated. Make sure they're properly seated and any protective tape is removed."
        }
    },
    "email_issues": {
        "title": "Email/Outlook Troubleshooting",
        "steps": [
            {
                "id": 1,
                "question": "Can you open Outlook successfully?",
                "yes_next": 2,
                "no_next": "outlook_wont_start",
                "type": "yes_no"
            },
            {
                "id": 2,
                "question": "What specific email problem are you experiencing?",
                "options": [
                    {"text": "Can't send emails", "next": "send_issues"},
                    {"text": "Not receiving emails", "next": "receive_issues"},
                    {"text": "Emails are slow to sync", "next": "sync_slow"},
                    {"text": "Can't connect to server",
                        "next": "server_connection"}
                ],
                "type": "multiple_choice"
            }
        ],
        "solutions": {
            "outlook_wont_start": "Try starting Outlook in safe mode: Press Windows+R, type 'outlook /safe', and press Enter. If it works, disable add-ins one by one.",
            "send_issues": "Check your internet connection, verify outgoing server settings, and ensure you're not exceeding attachment size limits.",
            "receive_issues": "Check if your mailbox is full, verify incoming server settings, and check your spam/junk folder.",
            "sync_slow": "This could be due to large mailbox size. Try archiving old emails or checking with IT about server performance.",
            "server_connection": "Verify your internet connection and check with IT about server maintenance or outages."
        }
    }
}


def search_knowledge_base(query: str, max_results: int = 3) -> List[Dict[str, Any]]:
    """
    Search the knowledge base for relevant articles based on the query.
    Returns a list of matching articles with relevance scoring.
    """
    query_lower = query.lower()
    query_words = query_lower.split()

    scored_articles = []

    for article in knowledge_base_articles:
        score = 0

        # Check title relevance (higher weight)
        for word in query_words:
            if word in article["title"].lower():
                score += 3

        # Check tags relevance (high weight)
        for word in query_words:
            for tag in article["tags"]:
                if word in tag.lower():
                    score += 2

        # Check content relevance (lower weight)
        for word in query_words:
            if word in article["content"].lower():
                score += 1

        # Check category relevance
        for word in query_words:
            if word in article["category"].lower():
                score += 2

        if score > 0:
            scored_articles.append((score, article))

    # Sort by score and return top results
    scored_articles.sort(key=lambda x: x[0], reverse=True)
    return [article for score, article in scored_articles[:max_results]]


def search_enhanced_faq(query: str, max_results: int = 3) -> List[Dict[str, Any]]:
    """
    Search the enhanced FAQ database for relevant entries.
    """
    query_lower = query.lower()
    query_words = query_lower.split()

    scored_faqs = []

    for faq in enhanced_faq_data:
        score = 0

        # Check question relevance (highest weight)
        for word in query_words:
            if word in faq["question"].lower():
                score += 4

        # Check answer relevance
        for word in query_words:
            if word in faq["answer"].lower():
                score += 2

        # Check category relevance
        for word in query_words:
            if word in faq["category"].lower():
                score += 2

        if score > 0:
            scored_faqs.append((score, faq))

    # Sort by score and return top results
    scored_faqs.sort(key=lambda x: x[0], reverse=True)
    return [faq for score, faq in scored_faqs[:max_results]]


def get_troubleshooting_flow(issue_type: str) -> Dict[str, Any]:
    """
    Get a specific troubleshooting flow by issue type.
    """
    return troubleshooting_flows.get(issue_type, {})


def get_available_flows() -> List[str]:
    """
    Get list of available troubleshooting flows.
    """
    return list(troubleshooting_flows.keys())
