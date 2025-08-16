# IT Helpdesk Bot - Enhanced Personal Assistant v2.0

A full-stack AI-powered IT helpdesk chatbot with advanced features including ChromaDB knowledge base, voice responses, and enhanced session management. Built with FastAPI backend and React frontend, powered by Azure OpenAI.

## 🌟 Enhanced Features

### Core Capabilities
- **🤖 AI-Powered Chat Assistant**: Intelligent responses using Azure OpenAI's GPT-4o-mini
- **� ChromaDB Knowledge Base**: Comprehensive IT knowledge search across FAQs, software guides, and policies
- **🔊 Voice Responses**: Text-to-speech using HuggingFace TTS models
- **🧠 Context Memory**: Multi-turn conversation awareness and session management
- **📦 Batch Processing**: Handle multiple questions in a single message

### Advanced Features
- **� Smart FAQ System**: Enhanced FAQ database with semantic search
- **🎫 Auto-Categorized Tickets**: Intelligent ticket creation with priority assignment
- **�️ Interactive Troubleshooting**: Step-by-step guided troubleshooting flows
- **📊 Real-time Statistics**: Live ticket and system statistics
- **📱 Responsive Design**: Modern UI with audio playback controls

### Knowledge Base Collections
- **❓ FAQs**: Password resets, VPN setup, email issues, WiFi troubleshooting
- **� Software Guides**: Office 365, Slack, Zoom, Git, Adobe Creative Suite
- **📋 IT Policies**: Security policies, data backup, remote work guidelines

## 🛠️ Tech Stack

### Backend
- **FastAPI**: High-performance Python web framework
- **Azure OpenAI**: GPT-4o-mini for intelligent responses
- **ChromaDB**: Vector database for semantic search
- **Sentence Transformers**: Text embeddings for knowledge retrieval
- **Uvicorn**: ASGI server for FastAPI applications
- **Pydantic**: Data validation and serialization
- **Python-dotenv**: Environment variable management

### Frontend
- **React 18**: Modern React with hooks
- **Vite**: Fast development build tool  
- **Tailwind CSS**: Utility-first CSS framework
- **Audio API**: Browser audio playback for voice responses
- **@vitejs/plugin-react**: Official React plugin for Vite

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- Node.js 16+
- Azure OpenAI API access
- VS Code (recommended for development)

### Easy Setup Script
```bash
git clone https://github.com/toanlq204/it-helpdesk-bot-personal.git
cd it-helpdesk-bot-personal
git checkout feature/updateitbot_workshop3  # Switch to the enhanced features branch
./setup_enhanced.sh
```

### Manual Setup

#### 1. Backend Setup

Create and activate virtual environment:
```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

Install dependencies:
```bash
pip install -r requirements.txt
```

#### Environment Configuration
```bash
cp env.template .env
```

Edit `.env` file with your Azure OpenAI credentials:
```env
# Azure OpenAI Configuration
AZURE_OPENAI_API_KEY=your-azure-openai-api-key
AZURE_OPENAI_ENDPOINT=https://your-resource-name.openai.azure.com/
AZURE_OPENAI_API_VERSION=2024-07-01-preview
MODEL_NAME=gpt-4o-mini

# Azure OpenAI Embedding Configuration
AZOPENAI_EMBEDDING_API_KEY=your-azure-openai-api-key
AZOPENAI_EMBEDDING_MODEL=text-embedding-3-small

# ChromaDB Configuration (Optional)
CHROMADB_PERSIST_DIR=./chromadb_data
```

### 3. Frontend Setup
```bash
cd frontend
npm install
```

### 4. Run the Application

#### Option 1: Using VS Code Tasks (Recommended)
This project includes VS Code tasks for easy development. In VS Code:
1. Press `Ctrl+Shift+P` (or `Cmd+Shift+P` on Mac)
2. Type "Tasks: Run Task"
3. Select "Run Backend (FastAPI)" and "Run Frontend (React/Vite)"

Or use the terminal commands below:

#### Option 2: Manual Terminal Commands

#### Start Backend (Terminal 1)
```bash
# From project root
source .venv/bin/activate  # Activate virtual environment
uvicorn backend.main:app --reload --port 8000
```

**Note**: The VS Code task uses the full path to the virtual environment Python interpreter, so it doesn't require manual activation.

#### Start Frontend (Terminal 2)
```bash
# From project root
cd frontend
npm run dev
```

The application will be available at:
- **Frontend**: http://localhost:5173
- **Backend API**: http://localhost:8000
- **API Documentation**: http://localhost:8000/docs

## � Development

### Current Branch
This project is currently on the `feature/updateitbot_workshop3` branch, which includes enhanced features and improvements.

### Quick Development Setup
1. Clone the repository
2. Run the setup script: `./setup_enhanced.sh`
3. Configure your `.env` file
4. Use VS Code tasks to start both services

### VS Code Integration

This project includes VS Code configuration for seamless development:

### Predefined Tasks
- **Run Backend (FastAPI)**: Starts the FastAPI server with hot reload
- **Run Frontend (React/Vite)**: Starts the Vite development server

### Using VS Code Tasks
1. Open Command Palette (`Ctrl+Shift+P` or `Cmd+Shift+P`)
2. Type "Tasks: Run Task"
3. Select the desired task:
   - "Run Backend (FastAPI)"
   - "Run Frontend (React/Vite)"

Both tasks run in the background, allowing you to start both services easily.

## 📁 Project Structure

```
```
it-helpdesk-bot-personal/
├── .vscode/                   # VS Code configuration
│   └── tasks.json            # Predefined tasks for running backend/frontend
├── backend/                   # FastAPI backend
│   ├── main.py               # Main application and chat endpoint
│   ├── models.py             # Pydantic data models
│   ├── openai_client.py      # Azure OpenAI client configuration
│   ├── functions.py          # Tool functions and ChromaDB integration
│   ├── context_manager.py    # Session and context management
│   ├── ticket_management.py  # Enhanced ticket system
│   ├── knowledge_base.py     # Legacy knowledge base
│   ├── tools/                # Enhanced feature modules
│   │   ├── __init__.py       # Package initialization
│   │   ├── faq_handler.py    # ChromaDB knowledge base handler
│   │   └── voice_handler.py  # HuggingFace TTS integration
│   └── data/                 # Knowledge base data
│       ├── __init__.py       # Package initialization
│       └── mock_data.py      # IT knowledge database
├── frontend/                  # React frontend
│   ├── src/
│   │   ├── App.jsx           # Main application with audio support
│   │   ├── api.js            # API communication layer
│   │   ├── main.jsx          # React entry point
│   │   ├── index.css         # Global styles
│   │   └── components/
│   │       ├── ChatWindow.jsx    # Chat interface with audio playback
│   │       └── MessageBubble.jsx # Message component with audio indicators
│   ├── index.html            # HTML template
│   ├── package.json          # Frontend dependencies
│   ├── postcss.config.js     # PostCSS configuration
│   ├── tailwind.config.js    # Tailwind CSS configuration
│   └── vite.config.js        # Vite build configuration
├── chromadb_data/            # ChromaDB persistent storage
│   └── chroma.sqlite3        # ChromaDB database file
├── logs/                     # Application logs directory
├── requirements.txt          # Python dependencies (enhanced)
├── setup_enhanced.sh         # Easy setup script
├── env.template             # Environment variables template
├── package.json             # Root package.json for workspace
└── README.md                # This documentation
```

## 🚀 Enhanced Features Guide

### ChromaDB Knowledge Base
The enhanced bot uses ChromaDB for semantic search across three collections:

**FAQs Collection**: Common IT questions and solutions
- Password reset procedures
- VPN setup instructions
- Email configuration
- WiFi troubleshooting

**Software Collection**: Application guides and installation
- Microsoft Office 365 setup
- Slack configuration
- Zoom installation
- Development tools (Git, VS Code)

**Policies Collection**: IT policies and procedures
- Password policies
- Software installation rules
- Data backup requirements
- Remote work guidelines

### Voice Responses
The bot can convert text responses to speech using HuggingFace TTS:
- Automatic audio generation for assistant responses
- Browser-based audio playback
- Visual indicators during audio playback
- Fallback to text-only if TTS unavailable

### Context Management
Enhanced session handling provides:
- Multi-turn conversation memory
- Context-aware follow-up questions
- Automatic session cleanup
- Conversation state tracking

### Try These Enhanced Commands
```
"Search knowledge base for VPN setup"
"How to reset password? Also start printer troubleshooting"
"What's the policy for installing new software?"
"Create a ticket for broken laptop screen"
"Show me my recent tickets"
```
```

## 🔧 API Endpoints

### Chat Endpoint
- **POST** `/chat` - Send message and get AI response
  ```json
  {
    "message": "How do I reset my password?",
    "session_id": "unique-session-id"
  }
  ```

### Health Check
- **GET** `/health` - Check server status and open tickets count

## 🤖 Available AI Tools

The bot has access to several specialized functions:

1. **FAQ Lookup** (`get_faq_answer`)
   - Searches knowledge base for common IT questions
   - Provides instant answers for password resets, email setup, etc.

2. **Ticket Creation** (`create_ticket`)
   - Creates support tickets for complex issues
   - Assigns unique ticket IDs
   - Tracks ticket status

3. **Software Information** (`get_software_info`)
   - Provides software versions and download links
   - Helps with installation guidance

## 💡 Usage Examples

**Password Reset:**
> "I forgot my password, can you help me reset it?"

**Software Installation:**
> "How do I install Microsoft Office?"

**Multiple Questions:**
> "How do I reset my password? Also, where can I download Adobe Photoshop?"

**Create Ticket:**
> "My computer keeps crashing when I open Excel files"

## 🔒 Security Features

- **CORS Protection**: Configurable for production deployment
- **Session Management**: Isolated chat sessions per user
- **Input Validation**: Pydantic models ensure data integrity
- **Error Handling**: Comprehensive error management

## 🚀 Deployment

### Backend Deployment
The FastAPI backend can be deployed to:
- **Cloud platforms**: AWS, Azure, GCP
- **Container platforms**: Docker, Kubernetes
- **Serverless**: Azure Functions, AWS Lambda

### Frontend Deployment
The React frontend can be deployed to:
- **Static hosting**: Netlify, Vercel, GitHub Pages
- **CDN**: CloudFront, Azure CDN
- **Traditional hosting**: Nginx, Apache

### Environment Variables
Update CORS settings in `backend/main.py` for production:
```python
allow_origins=["https://your-frontend-domain.com"]
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🆘 Support

For support, please:
1. Check the [API documentation](http://localhost:8000/docs) when running locally
2. Open an issue on GitHub
3. Contact the development team

### Troubleshooting

**Backend not starting?**
- Ensure Python virtual environment is activated
- Check that all dependencies are installed: `pip install -r requirements.txt`
- Verify your `.env` file has correct Azure OpenAI credentials

**Frontend not starting?**
- Ensure Node.js is installed (version 16+)
- Run `npm install` in the frontend directory
- Check for any npm error messages

**VS Code Tasks not working?**
- Ensure you're opening the project from the root directory
- Check that the `.vscode/tasks.json` file exists
- Verify the Python virtual environment path in tasks.json

## 🔮 Roadmap

- [ ] User authentication and authorization
- [ ] Advanced ticket management dashboard
- [ ] Integration with enterprise systems (LDAP, ServiceNow)
- [ ] Multi-language support
- [ ] Voice chat capabilities
- [ ] Analytics and reporting dashboard
- [ ] Mobile application

---

**Built with ❤️ for enterprise IT support**