# Advanced IT Helpdesk Bot - AI-Powered Assistant v3.0

A sophisticated full-stack AI-powered IT helpdesk chatbot with cutting-edge features including vector database search, advanced conversational AI, intelligent function calling, and comprehensive knowledge management. Built with FastAPI backend and React frontend, powered by Azure OpenAI and advanced AI frameworks.

## 🌟 Advanced AI Features

### Core AI Capabilities
- **🤖 Intelligent Chat Assistant**: Advanced responses using Azure OpenAI's GPT-4o-mini
- **🧠 Vector Database Search**: Lightning-fast semantic search with Pinecone vector store
- **💬 Advanced Conversational AI**: LangChain-powered RAG workflows with memory
- **🛠️ Intelligent Function Calling**: AI agents for dynamic capability selection
- **📊 Multi-Modal Integration**: Seamless combination of all AI features

### Enhanced Knowledge Management
- **🔍 Semantic Search**: ChromaDB and Pinecone vector databases for comprehensive IT knowledge
- **🔊 Voice Responses**: Text-to-speech using HuggingFace TTS models
- **🧠 Context Memory**: Multi-turn conversation awareness and session management
- **📦 Batch Processing**: Handle multiple questions in a single message

### Smart IT Support Features
- **❓ Smart FAQ System**: Enhanced FAQ database with semantic search
- **🎫 Auto-Categorized Tickets**: Intelligent ticket creation with priority assignment
- **🛠️ Interactive Troubleshooting**: Step-by-step guided troubleshooting flows
- **📊 Real-time Statistics**: Live ticket and system statistics
- **📱 Responsive Design**: Modern UI with audio playback controls

### Knowledge Base Collections
- **❓ FAQs**: Password resets, VPN setup, email issues, WiFi troubleshooting
- **📖 Software Guides**: Office 365, Slack, Zoom, Git, Adobe Creative Suite
- **📋 IT Policies**: Security policies, data backup, remote work guidelines
- **🔧 Troubleshooting**: Hardware diagnostics, software issues, network problems

## 🏗️ Architecture Overview

```
Frontend (React/Vite) ←→ Backend (FastAPI) ←→ Advanced AI Components
                                           ├── Vector Store Manager (Pinecone)
                                           ├── Conversation Manager (LangChain)
                                           ├── Intelligent Function Agent
                                           ├── Voice Handler (TTS)
                                           └── ChromaDB (Legacy Support)
```

## 🛠️ Tech Stack

### Backend (Python)
- **FastAPI**: High-performance Python web framework
- **Azure OpenAI**: GPT-4o-mini for intelligent responses
- **Pinecone**: Cloud vector database for fast similarity search
- **LangChain**: Advanced AI workflow framework with RAG capabilities
- **ChromaDB**: Vector database for semantic search (fallback)
- **Sentence Transformers**: Text embeddings for knowledge retrieval
- **Uvicorn**: ASGI server for FastAPI applications
- **Pydantic**: Data validation and serialization

### Frontend (JavaScript)
- **React 18**: Modern React with hooks
- **Vite**: Fast development build tool  
- **Tailwind CSS**: Utility-first CSS framework
- **Audio API**: Browser audio playback for voice responses

### AI & ML Libraries
- **LangChain**: Conversational AI and RAG workflows
- **Pinecone**: Vector database integration
- **OpenAI Functions**: Advanced function calling capabilities
- **HuggingFace**: Text-to-speech and transformer models

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- Node.js 16+
- Azure OpenAI API access
- Pinecone API key (for vector search)
- VS Code (recommended for development)

### Automated Setup (Recommended)
```bash
git clone https://github.com/toanlq204/it-helpdesk-bot-personal.git
cd it-helpdesk-bot-personal
chmod +x setup_enhanced.sh
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

#### 2. Environment Configuration
```bash
cp env.template .env
```

Edit `.env` file with your API credentials:
```env
# Azure OpenAI Configuration
AZURE_OPENAI_API_KEY=your-azure-openai-api-key
AZURE_OPENAI_ENDPOINT=https://your-resource-name.openai.azure.com/
AZURE_OPENAI_API_VERSION=2024-07-01-preview
AZURE_OPENAI_DEPLOYMENT=gpt-4o-mini

# Azure OpenAI Embedding Configuration
AZOPENAI_EMBEDDING_API_KEY=your-azure-openai-api-key
AZOPENAI_EMBEDDING_MODEL=text-embedding-3-large

# Pinecone Configuration (for advanced AI features)
PINECONE_API_KEY=your-pinecone-api-key
PINECONE_INDEX_NAME=it-helpdesk-kb

# ChromaDB Configuration (fallback support)
CHROMADB_PERSIST_DIR=./chromadb_data
```

#### 3. Initialize Advanced AI Features
```bash
# Initialize vector database and AI components
python -c "
from backend.tools.pinecone_handler import get_vector_store_manager
from backend.tools.langchain_manager import get_conversation_manager
print('Initializing advanced AI features...')
manager = get_vector_store_manager()
conversation = get_conversation_manager()
print('Advanced AI features initialized successfully!')
"
```

#### 4. Frontend Setup
```bash
cd frontend
npm install
```

#### 5. Run the Application

##### Option 1: Using VS Code Tasks (Recommended)
This project includes VS Code tasks for easy development. In VS Code:
1. Press `Ctrl+Shift+P` (or `Cmd+Shift+P` on Mac)
2. Type "Tasks: Run Task"
3. Select "Run Backend (FastAPI)" and "Run Frontend (React/Vite)"

##### Option 2: Manual Terminal Commands

Start Backend (Terminal 1):
```bash
# From project root
source .venv/bin/activate  # Activate virtual environment
uvicorn backend.main:app --reload --port 8000
```

Start Frontend (Terminal 2):
```bash
# From project root
cd frontend
npm run dev
```

The application will be available at:
- **Frontend**: http://localhost:5173
- **Backend API**: http://localhost:8000
- **API Documentation**: http://localhost:8000/docs
- **System Status**: http://localhost:8000/system/status

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

### Chat Endpoints
- **POST** `/chat` - Standard chat with ChromaDB knowledge base
- **POST** `/chat/enhanced` - Advanced AI chat with vector search and intelligent agents

#### Enhanced Chat Request
```json
{
  "message": "How do I reset my password and set up VPN?",
  "session_id": "user123",
  "include_audio": true
}
```

#### Enhanced Chat Response
```json
{
  "reply": "AI response with advanced features",
  "messages": [...],
  "session_id": "user123",
  "processing_mode": "auto",
  "features_used": ["advanced_conversation_ai", "vector_database_search"],
  "fallback_used": false
}
```

### System Management Endpoints
- **GET** `/system/status` - Check AI system availability and component status
- **GET** `/system/demo` - Run system demonstration of all features
- **GET** `/system/report` - Generate detailed system capability report
- **POST** `/system/initialize` - Initialize advanced AI features

### Traditional Endpoints
- **GET** `/health` - Check server status and open tickets count
- **GET** `/tickets/stats` - Get ticket statistics
- **POST** `/tickets` - Create new support ticket

## 🤖 Available AI Tools & Capabilities

The advanced AI system includes specialized tools and capabilities:

### Intelligent Function Agent Tools
1. **Knowledge Base Search** - Semantic search across all IT documentation
2. **Ticket Management** - Create, update, and track support tickets
3. **Software Information** - Provide software versions and installation guidance
4. **Troubleshooting Flows** - Step-by-step problem resolution
5. **Policy Lookup** - Access IT policies and procedures
6. **Voice Synthesis** - Convert responses to speech

### Vector Database Features
- **Multi-namespace Search**: FAQs, policies, software guides, troubleshooting
- **Semantic Similarity**: Advanced embedding-based search
- **Relevance Scoring**: Intelligent result ranking
- **Real-time Updates**: Dynamic knowledge base updates

### Conversational AI Features
- **Memory Management**: Context-aware multi-turn conversations
- **Session Persistence**: Maintain conversation state across interactions
- **Intelligent Routing**: Automatic feature selection based on query type
- **Fallback Support**: Graceful degradation to basic features

## 💡 Advanced Usage Examples

**Vector Search:**
> "Search knowledge base for VPN setup procedures"

**Intelligent Conversation:**
> "I'm having trouble with my laptop screen flickering, can you help troubleshoot this step by step?"

**Function Calling:**
> "Create a high-priority ticket for broken printer in conference room"

**Multi-modal Query:**
> "How do I reset my password and also set up two-factor authentication?"
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