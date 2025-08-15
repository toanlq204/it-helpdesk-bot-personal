# Enhanced IT Helpdesk Bot - Advanced Edition

A sophisticated IT helpdesk chatbot built with **FastAPI**, **React**, and **Azure OpenAI SDK** featuring advanced capabilities for enterprise IT support.

## 🚀 New Enhanced Features

### 1. **Dynamic Knowledge Base Search**
- Comprehensive IT knowledge base with detailed troubleshooting guides
- Smart search algorithms with relevance scoring
- Categories: Authentication, Network, Email, Hardware, Software, Performance, Security
- Auto-summarization and related article suggestions

### 2. **Multi-Turn Context Memory**
- Preserves conversation history and context between interactions
- Intelligent follow-up detection ("That didn't work", "What else can I try?")
- Context-aware responses based on previous interactions
- Session management with automatic cleanup

### 3. **Interactive Troubleshooting Flows**
- Step-by-step guided troubleshooting for common issues:
  - Wi-Fi connection problems
  - Printer troubleshooting
  - Email/Outlook issues
- Interactive decision trees with multiple choice and yes/no questions
- Context-aware flow progression

### 4. **Enhanced Ticket Management**
- Auto-categorization based on issue description
- Intelligent priority assignment (Critical, Urgent, High, Medium, Low)
- Auto-assignment to appropriate IT staff based on specialties
- Ticket status tracking with realistic progression simulation
- Comprehensive ticket history and comments

### 5. **Batch Request Processing**
- Handle multiple questions in a single request
- Smart query splitting and processing
- Consolidated responses for related questions
- Improved efficiency for complex user requests

## 🛠️ Technical Architecture

### Backend (Python + FastAPI)
```
backend/
├── main.py                 # Enhanced FastAPI app with context management
├── functions.py            # Extended function calling with new tools
├── knowledge_base.py       # Dynamic knowledge base search engine
├── ticket_management.py    # Advanced ticket creation and tracking
├── context_manager.py      # Multi-turn conversation context
├── models.py              # Enhanced data models
├── openai_client.py       # Azure OpenAI SDK integration
└── mock_data.py           # Sample data for testing
```

### Frontend (React + Tailwind)
```
frontend/src/
├── App.jsx                # Enhanced UI with new features display
├── components/
│   ├── ChatWindow.jsx     # Chat interface
│   └── MessageBubble.jsx  # Message display component
└── api.js                 # API client
```

## 🎯 Core Capabilities

### Knowledge Base Search
```javascript
// Example: Search for VPN troubleshooting
"Search knowledge base for VPN connection issues"
```
- Returns detailed troubleshooting guides
- Includes step-by-step instructions
- Provides related articles and estimated resolution time

### Interactive Troubleshooting
```javascript
// Example: Start guided troubleshooting
"Start Wi-Fi troubleshooting" 
"Help me troubleshoot printer problems"
"Guide me through email setup"
```

### Advanced Ticket Management
```javascript
// Example: Create prioritized tickets
"Create a ticket: Server is down and entire team can't work"  // → Critical
"Create a ticket: Laptop screen flickering"                   // → Medium
"My printer won't print anything"                            // → Auto-categorized
```

### Context-Aware Follow-ups
```javascript
// Initial query
"How do I reset my password?"

// Follow-up (remembers context)
"That didn't work"           // → Provides alternative solutions
"What else can I try?"       // → Suggests escalation or ticket creation
"Can you clarify step 3?"    // → Provides detailed explanation
```

### Batch Processing
```javascript
// Multiple questions at once
"How to reset my password? Also, how do I connect to VPN? And where can I download Outlook?"
```

## 🔧 New Tool Functions

| Function | Description | Example Usage |
|----------|-------------|---------------|
| `search_knowledge_base_articles` | Search comprehensive knowledge base | Password reset guides, VPN troubleshooting |
| `get_enhanced_faq_answer` | Smart FAQ search with multiple results | Quick answers to common questions |
| `create_ticket` | Enhanced ticket creation with auto-categorization | IT support requests with priority assignment |
| `check_ticket_status` | Get detailed ticket status and progress | Track ticket resolution progress |
| `list_my_tickets` | List user's tickets with filtering options | View all open, resolved, or specific status tickets |
| `start_troubleshooting_flow` | Begin interactive troubleshooting | Guided problem resolution workflows |
| `get_helpdesk_stats` | System statistics and metrics | Dashboard information for IT teams |

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- Node.js 16+
- Azure OpenAI API key

### Backend Setup
1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd it-helpdesk-bot-personal
   ```

2. **Create virtual environment**
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment**
   ```bash
   cp env.template .env
   # Edit .env with your Azure OpenAI credentials
   ```

5. **Run the backend**
   ```bash
   uvicorn backend.main:app --reload --port 8000
   ```

### Frontend Setup
1. **Navigate to frontend directory**
   ```bash
   cd frontend
   ```

2. **Install dependencies**
   ```bash
   npm install
   ```

3. **Start development server**
   ```bash
   npm run dev
   ```

4. **Access the application**
   Open `http://localhost:5173` in your browser

## 📊 API Endpoints

### Enhanced Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/chat` | POST | Enhanced chat with context management |
| `/health` | GET | System health with feature status |
| `/stats` | GET | Comprehensive system statistics |

### Chat Request Format
```json
{
  "session_id": "user-session-123",
  "message": "How to fix slow Wi-Fi? Also create a ticket for broken printer"
}
```

### Enhanced Response Format
```json
{
  "reply": "AI response text",
  "messages": [{"role": "user|assistant", "content": "..."}],
  "tickets": [...],
  "stats": {
    "total": 15,
    "by_status": {"Open": 5, "In Progress": 3},
    "by_priority": {"High": 2, "Medium": 8}
  },
  "context": {
    "conversation_state": "troubleshooting",
    "last_issue": "Wi-Fi connectivity"
  }
}
```

## 🧪 Testing the Enhanced Features

### Manual Testing Examples

1. **Knowledge Base Search**
   ```
   "Search for VPN troubleshooting guides"
   "How to fix Outlook sync issues?"
   ```

2. **Context Memory**
   ```
   User: "My printer won't print"
   Bot: [provides solution]
   User: "That didn't work"
   Bot: [remembers context, suggests alternatives]
   ```

3. **Interactive Troubleshooting**
   ```
   "Start printer troubleshooting"
   "Help me fix Wi-Fi issues step by step"
   ```

4. **Batch Processing**
   ```
   "How to reset password? Also how to install Outlook? And what's the VPN server address?"
   ```

5. **Ticket Management**
   ```
   "Create urgent ticket: Email server is down"
   "Check status of ticket INC20240130001"
   "Show me all my open tickets"
   ```

### Automated Testing
```bash
# Run the comprehensive test suite
python test_enhanced_features.py
```

## 🎨 UI Enhancements

### New Visual Features
- **Enhanced welcome message** with feature overview
- **Ticket counter** in header showing active tickets
- **Context indicators** showing current conversation state
- **Enhanced status display** showing system capabilities
- **Improved placeholders** with example queries

### Responsive Design
- Mobile-optimized chat interface
- Adaptive layouts for different screen sizes
- Enhanced accessibility features

## 🔐 Security Features

- **Session isolation** - Each user session is completely isolated
- **Input validation** - All user inputs are validated and sanitized
- **Rate limiting** - Built-in protection against abuse
- **Context cleanup** - Automatic cleanup of old session data

## 📈 Performance Optimizations

- **Intelligent batching** - Reduced API calls through smart query batching
- **Context trimming** - Automatic management of conversation history
- **Cached responses** - Improved response times for common queries
- **Async processing** - Non-blocking operations for better scalability

## 🔄 Configuration

### Environment Variables
```bash
# Azure OpenAI Configuration
AZURE_OPENAI_ENDPOINT=https://your-resource.openai.azure.com/
AZURE_OPENAI_API_KEY=your-api-key
AZURE_OPENAI_API_VERSION=2024-02-15-preview
AZURE_OPENAI_DEPLOYMENT_NAME=your-deployment-name

# Application Configuration
MAX_CONVERSATION_LENGTH=40
SESSION_CLEANUP_HOURS=24
MAX_BATCH_QUERIES=4
```

### Customization Options
- **Knowledge base content** - Add/modify articles in `knowledge_base.py`
- **Troubleshooting flows** - Customize workflows in the knowledge base
- **Ticket categories** - Modify categories in `ticket_management.py`
- **Context behavior** - Adjust context settings in `context_manager.py`

## 🚀 Deployment

### Production Checklist
- [ ] Configure proper CORS origins
- [ ] Set up environment variables
- [ ] Configure database for persistent storage (replace in-memory storage)
- [ ] Set up logging and monitoring
- [ ] Configure authentication and authorization
- [ ] Set up backup and recovery procedures

### Docker Deployment
```dockerfile
# Build and run with Docker
docker build -t enhanced-helpdesk-bot .
docker run -p 8000:8000 enhanced-helpdesk-bot
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **Azure OpenAI SDK** for powerful AI capabilities
- **FastAPI** for the robust backend framework
- **React + Tailwind** for the modern frontend
- **VS Code** for the excellent development environment

---

**Enhanced IT Helpdesk Bot** - Revolutionizing IT support with AI-powered assistance, context awareness, and intelligent automation. 🚀✨
