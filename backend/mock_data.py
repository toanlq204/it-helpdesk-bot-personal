# Mock data for IT Helpdesk

faq_data = [
    {
        "question": "How do I reset my password?",
        "answer": "Go to the IT portal, click 'Forgot Password', follow the steps, then check your email for the reset link."
    },
    {
        "question": "VPN is not connecting",
        "answer": "Verify internet connectivity, then restart the VPN client and try again. If issues persist, create a ticket."
    },
    {
        "question": "How to install Outlook?",
        "answer": "Visit the Office 365 portal, download Outlook, run the installer, and sign in with your corporate account."
    },
    {
        "question": "Email not syncing",
        "answer": "Check mailbox size, ensure you are online, and re-authenticate your account in Outlook settings."
    },
]

software_list = [
    {"name": "Outlook", "version": "2024.1",
        "installer_link": "https://company.example/install/outlook"},
    {"name": "Zoom", "version": "6.5",
        "installer_link": "https://company.example/install/zoom"},
    {"name": "VSCode", "version": "1.92",
        "installer_link": "https://company.example/install/vscode"},
]

# Runtime storage (mock DB)
ticket_data = []  # [{id, issue, status, created_by}]
