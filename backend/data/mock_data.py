# Mock IT Knowledge Base Data for ChromaDB
from typing import List, Dict, Any


def get_faq_data() -> List[Dict[str, Any]]:
    """Get FAQ data for the knowledge base"""
    return [
        {
            "id": "faq_001",
            "content": "How to reset your password: 1) Go to the company login page 2) Click 'Forgot Password' 3) Enter your work email 4) Check your email for reset instructions 5) Follow the link and create a new password. Your new password must be at least 12 characters with uppercase, lowercase, numbers, and special characters.",
            "category": "authentication",
            "priority": "high",
            "keywords": ["password", "reset", "forgot", "login", "authentication"]
        },
        {
            "id": "faq_002",
            "content": "VPN Setup Instructions: 1) Download Cisco AnyConnect from the company portal 2) Install the application 3) Connect to vpn.company.com 4) Enter your work credentials 5) Accept the security certificate. If you experience connection issues, try connecting to the backup server vpn-backup.company.com",
            "category": "network",
            "priority": "high",
            "keywords": ["vpn", "cisco", "anyconnect", "remote", "connection"]
        },
        {
            "id": "faq_003",
            "content": "Email not syncing on mobile device: 1) Check your internet connection 2) Verify email settings: Server: mail.company.com, Port: 993 (IMAP) or 995 (POP3) 3) Update your mobile email app 4) Remove and re-add your work account 5) Contact IT if the issue persists after 24 hours.",
            "category": "email",
            "priority": "medium",
            "keywords": ["email", "mobile", "sync", "imap", "settings"]
        },
        {
            "id": "faq_004",
            "content": "Printer troubleshooting: 1) Check if printer is powered on and connected to network 2) Clear any paper jams 3) Check ink/toner levels 4) Restart the printer 5) Update printer drivers from the company software center 6) Try printing a test page. For network printers, the default IP range is 192.168.1.100-200.",
            "category": "hardware",
            "priority": "medium",
            "keywords": ["printer", "printing", "drivers", "network", "troubleshoot"]
        },
        {
            "id": "faq_005",
            "content": "Two-factor authentication setup: 1) Download Microsoft Authenticator app 2) Log into company portal 3) Go to Security Settings > Two-Factor Authentication 4) Scan the QR code with your authenticator app 5) Enter the verification code to confirm setup. Backup codes will be provided for emergency access.",
            "category": "security",
            "priority": "high",
            "keywords": ["2fa", "authentication", "microsoft", "authenticator", "security"]
        },
        {
            "id": "faq_006",
            "content": "WiFi connection issues: 1) Forget and reconnect to CompanyWiFi network 2) Check if you're in range of access points 3) Restart your device's WiFi adapter 4) Use WiFi password: CompanySecure2024! 5) For guest access, connect to CompanyGuest (no password required). Contact IT if you still cannot connect after trying these steps.",
            "category": "network",
            "priority": "high",
            "keywords": ["wifi", "wireless", "connection", "network", "access"]
        }
    ]


def get_software_data() -> List[Dict[str, Any]]:
    """Get software guides data for the knowledge base"""
    return [
        {
            "id": "soft_001",
            "content": "Microsoft Office 365 Installation: 1) Go to portal.office.com 2) Sign in with your work account 3) Click 'Install Office' > 'Office 365 apps' 4) Download and run the installer 5) Sign in when prompted during installation. Your license includes Word, Excel, PowerPoint, Outlook, Teams, and OneDrive with 1TB storage.",
            "category": "productivity",
            "software": "Microsoft Office 365",
            "version": "2024",
            "keywords": ["office", "365", "microsoft", "word", "excel", "installation"]
        },
        {
            "id": "soft_002",
            "content": "Slack Setup and Best Practices: 1) Download Slack from company.slack.com 2) Join using your work email 3) Set your status and profile 4) Join relevant channels (#general, #it-support, #your-department) 5) Enable notifications for direct messages and mentions only. Use threads for discussions and @channel sparingly.",
            "category": "communication",
            "software": "Slack",
            "version": "latest",
            "keywords": ["slack", "communication", "chat", "channels", "notifications"]
        },
        {
            "id": "soft_003",
            "content": "Zoom Installation and Configuration: 1) Download Zoom client from zoom.us/download 2) Sign in with SSO using company domain 3) Configure audio/video settings in preferences 4) Set up virtual backgrounds if needed 5) Install Zoom Outlook plugin for meeting integration. Default meeting room: company.zoom.us/my/yourname",
            "category": "communication",
            "software": "Zoom",
            "version": "5.17+",
            "keywords": ["zoom", "video", "meetings", "conference", "outlook"]
        },
        {
            "id": "soft_004",
            "content": "Antivirus Software (CrowdStrike): Automatically installed on all company devices. Do not disable or uninstall. If you see alerts: 1) Do not ignore security warnings 2) Report suspicious activity immediately 3) Do not click links in suspicious emails 4) Keep software updated. Contact IT immediately if CrowdStrike is not running.",
            "category": "security",
            "software": "CrowdStrike",
            "version": "current",
            "keywords": ["antivirus", "crowdstrike", "security", "malware", "protection"]
        },
        {
            "id": "soft_005",
            "content": "Git and Development Tools Setup: 1) Install Git from git-scm.com 2) Configure with: git config --global user.name 'Your Name' and git config --global user.email 'your.email@company.com' 3) Set up SSH keys for GitHub/GitLab 4) Install VS Code from company software center 5) Required extensions: GitLens, ESLint, Prettier",
            "category": "development",
            "software": "Git/VS Code",
            "version": "latest",
            "keywords": ["git", "vscode", "development", "ssh", "github"]
        },
        {
            "id": "soft_006",
            "content": "Adobe Creative Suite Access: Available through Adobe Admin Console. 1) Go to creativecloud.adobe.com 2) Sign in with your company Adobe ID 3) Download Creative Cloud desktop app 4) Install required applications (Photoshop, Illustrator, InDesign, etc.) 5) License allows installation on up to 2 devices. Contact IT for additional licenses.",
            "category": "creative",
            "software": "Adobe Creative Suite",
            "version": "2024",
            "keywords": ["adobe", "photoshop", "illustrator", "creative", "license"]
        }
    ]


def get_policy_data() -> List[Dict[str, Any]]:
    """Get IT policies data for the knowledge base"""
    return [
        {
            "id": "policy_001",
            "content": "Password Policy: Passwords must be at least 12 characters long, contain uppercase and lowercase letters, numbers, and special characters. Passwords must be changed every 90 days. Cannot reuse last 12 passwords. No dictionary words or personal information. Use password manager for unique passwords.",
            "category": "security",
            "policy_type": "authentication",
            "enforcement": "mandatory",
            "keywords": ["password", "policy", "security", "requirements", "change"]
        },
        {
            "id": "policy_002",
            "content": "Software Installation Policy: Only install software from the approved company software center. Personal software installations require IT approval. No pirated or unlicensed software allowed. Business-critical software must be approved by department head and IT security team. Contact IT for software requests.",
            "category": "software",
            "policy_type": "installation",
            "enforcement": "mandatory",
            "keywords": ["software", "installation", "approval", "licensed", "policy"]
        },
        {
            "id": "policy_003",
            "content": "Data Backup and Storage Policy: All work data must be stored on company-approved cloud services (OneDrive, SharePoint). Local backups are encouraged but not sufficient alone. Personal cloud services (Dropbox, Google Drive) prohibited for work data. Automatic backups run nightly for all company devices.",
            "category": "data",
            "policy_type": "backup",
            "enforcement": "mandatory",
            "keywords": ["backup", "storage", "onedrive", "sharepoint", "data"]
        },
        {
            "id": "policy_004",
            "content": "Remote Work IT Policy: VPN required for all remote connections. Keep devices updated and secure. Use company-provided devices when possible. Personal devices must be enrolled in Mobile Device Management (MDM). Report lost or stolen devices immediately. No public WiFi for sensitive work.",
            "category": "remote_work",
            "policy_type": "access",
            "enforcement": "mandatory",
            "keywords": ["remote", "vpn", "mdm", "devices", "security"]
        },
        {
            "id": "policy_005",
            "content": "Incident Reporting Policy: Report security incidents within 1 hour. Report hardware failures within 4 hours during business hours. Use IT ticketing system for all requests. Provide detailed descriptions and screenshots when possible. Critical incidents: call IT emergency line at ext. 911.",
            "category": "incident",
            "policy_type": "reporting",
            "enforcement": "mandatory",
            "keywords": ["incident", "reporting", "security", "hardware", "tickets"]
        },
        {
            "id": "policy_006",
            "content": "Email and Communication Policy: Use company email for business communications only. No personal use of company email accounts. Email retention: 7 years for business emails, auto-delete after retention period. Large attachments (>25MB) should use OneDrive sharing. External email marked with warning banner.",
            "category": "communication",
            "policy_type": "usage",
            "enforcement": "mandatory",
            "keywords": ["email", "communication", "retention", "attachments", "business"]
        }
    ]


def get_all_knowledge_data() -> Dict[str, List[Dict[str, Any]]]:
    """Get all knowledge base data organized by collection"""
    return {
        "faqs": get_faq_data(),
        "software": get_software_data(),
        "policies": get_policy_data()
    }
