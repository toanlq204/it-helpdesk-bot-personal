# AI-Powered IT Helpdesk Assistant

A comprehensive full-stack AI-powered IT helpdesk chatbot with advanced capabilities including vector database search, intelligent function calling, context-aware conversations, and smart prompt processing. Built with FastAPI backend and React frontend, powered by Azure OpenAI, PineCone, and LangChain.

## 🚀 Core AI Features

Based on 4 fundamental AI capabilities that power modern IT support:

### 🔍 **PineCone Fast Vector Search**
- **Lightning-fast semantic search** across comprehensive IT knowledge base
- **Multi-namespace support**: FAQs, knowledge articles, policies, troubleshooting guides
- **Intelligent query understanding** that goes beyond keyword matching
- **Real-time search results** with contextual relevance scoring

### ⚡ **Function Calling Dynamic Capabilities**
- **AI Agent with 8+ tools**: Automated task execution and workflow management
- **Smart ticket creation**: Auto-categorized support tickets with priority assignment
- **System information retrieval**: Real-time helpdesk statistics and health monitoring
- **Multi-tool workflows**: Chained actions like "search + create ticket"

### 🤖 **LangChain Prompt & Chain Management**
- **Advanced RAG (Retrieval-Augmented Generation)**: Context-aware knowledge retrieval
- **Conversation memory**: Multi-turn conversation awareness across sessions
- **Intelligent conversation chains**: Guided troubleshooting workflows
- **Context preservation**: Maintains discussion history for follow-up questions

### 🎯 **Handle Prompts Effectively**
- **Multi-query processing**: Handle multiple requests in a single message
- **Context detection**: Understands follow-up questions and references
- **Processing mode selection**: Auto, vector-only, RAG-only, or agent-only modes
- **Batch request handling**: Efficiently processes complex multi-part queries

## 🏗️ System Architecture

```
┌─────────────────────┐    ┌─────────────────────┐    ┌─────────────────────┐
│   Frontend (React)  │    │  Backend (FastAPI)  │    │   AI Components     │
│                     │    │                     │    │                     │
│ • Smart UI          │◄──►│ • Chat Endpoints    │◄──►│ • PineCone Vector   │
│ • Quick Actions     │    │ • Enhanced Mode     │    │ • LangChain RAG     │
│ • Voice Controls    │    │ • Session Mgmt      │    │ • Function Agent    │
│ • Real-time Status  │    │ • Context Manager   │    │ • Azure OpenAI     │
└─────────────────────┘    └─────────────────────┘    └─────────────────────┘
```

## 🛠️ Technology Stack

### **Backend (Python)**
- **FastAPI**: High-performance async web framework
- **Azure OpenAI**: GPT-4o-mini for intelligent responses and embeddings
- **PineCone**: Cloud vector database for semantic search
- **LangChain**: AI workflow framework with RAG capabilities
- **Pydantic**: Data validation and API models

### **Frontend (JavaScript/React)**
- **React 18**: Modern React with hooks and functional components
- **Vite**: Fast development build tool with HMR
- **Tailwind CSS**: Utility-first CSS framework for responsive design
- **Audio API**: Browser audio for text-to-speech responses

### **AI & ML Integration**
- **Vector Embeddings**: text-embedding-3-large for semantic search
- **Function Calling**: OpenAI Functions for dynamic tool execution
- **Memory Management**: LangChain conversation memory
- **Voice Synthesis**: Text-to-speech for accessibility

## 🚀 Quick Start

### Prerequisites
- **Python 3.10+** (recommended for best compatibility)
- **Node.js 18+** (for modern React features)
- **Azure OpenAI API access** (GPT-4o-mini & text-embedding-3-large)
- **PineCone API key** (for vector database operations)
- **VS Code** (recommended IDE with extensions)

### 🎯 Automated Setup (Recommended)
```bash
# Clone repository
git clone <your-repo-url>
cd it-helpdesk-bot-personal

# Make setup script executable and run
chmod +x setup_enhanced.sh
./setup_enhanced.sh
```

The automated script will:
- ✅ Create Python virtual environment
- ✅ Install all backend dependencies
- ✅ Set up frontend Node.js environment
- ✅ Configure environment variables
- ✅ Initialize vector database
- ✅ Validate all AI components

### 🔧 Manual Setup

#### **Step 1: Python Backend Environment**

```bash
# Create and activate virtual environment
python3 -m venv .venv
source .venv/bin/activate  # macOS/Linux
# or .venv\Scripts\activate  # Windows

# Install Python dependencies
pip install -r requirements.txt
```

#### **Step 2: Environment Configuration**

Copy and configure environment file:
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

# PineCone Configuration (for vector search)
PINECONE_API_KEY=your-pinecone-api-key
PINECONE_INDEX_NAME=it-helpdesk-kb
```

#### **Step 3: Frontend Environment**

```bash
cd frontend
npm install
```

#### **Step 4: Initialize AI Components**

```bash
# Test AI integration
python -c "
from backend.tools.pinecone_handler import get_vector_store_manager
from backend.tools.langchain_manager import get_conversation_manager
print('✅ Initializing AI components...')
manager = get_vector_store_manager()
conversation = get_conversation_manager()
print('✅ AI components ready!')
"
```

### 🚀 Running the Application

#### **Option A: VS Code Tasks (Recommended)**

This project includes VS Code tasks for seamless development:

1. **Open VS Code**: `code .`
2. **Open Command Palette**: `Ctrl+Shift+P` (Windows/Linux) or `Cmd+Shift+P` (macOS)
3. **Run Tasks**: Type "Tasks: Run Task" and select:
   - "Run Backend (FastAPI)" - Starts API server with hot reload
   - "Run Frontend (React/Vite)" - Starts development server

#### **Option B: Manual Terminal Commands**

**Terminal 1 - Backend:**
```bash
# From project root
source .venv/bin/activate
uvicorn backend.main:app --reload --port 8000
```

**Terminal 2 - Frontend:**
```bash
# From project root
cd frontend
npm run dev
```

### 🌐 Application URLs

- **🎨 Frontend UI**: http://localhost:5173
- **⚡ Backend API**: http://localhost:8000
- **📖 API Documentation**: http://localhost:8000/docs
- **📊 System Health**: http://localhost:8000/system/status

## 💡 How to Use

### **Smart Chat Interface**

1. **Open the application** at http://localhost:5173
2. **Choose processing mode**:
   - **🤖 Auto**: AI selects best approach automatically
   - **🔍 Vector**: Pure semantic search responses
   - **🧠 RAG**: Enhanced retrieval with conversation context
   - **⚡ Agent**: Function calling with tool execution

3. **Try sample queries**:
   ```
   "My VPN connection keeps dropping"
   "How do I reset my Office 365 password?"
   "Create a ticket for printer not working in Room 205"
   "What's our company's backup policy?"
   ```

### **Quick Action Buttons**

- **🔍 Knowledge Search**: Search IT policies and guides
- **🎫 Support Tickets**: Create and manage support requests
- **🛠️ Troubleshooting**: Guided problem-solving workflows
- **🤖 AI-Powered Help**: Advanced AI assistance with multiple tools

### **Voice Features**

- **🔊 Audio Responses**: Toggle text-to-speech for accessibility
- **🎧 Background Mode**: Listen while working

## 🔧 API Endpoints

### **Core Chat API**

| Endpoint | Method | Description | Key Features |
|----------|--------|-------------|--------------|
| `/chat` | POST | Standard chat | Basic AI responses |
| `/chat/enhanced` | POST | Enhanced chat | All 4 AI features integrated |
| `/chat/vector-search` | POST | Vector search | PineCone semantic search |
| `/chat/rag` | POST | RAG mode | LangChain + memory |
| `/chat/agent` | POST | Function agent | Tool calling & automation |

### **System & Health**

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/system/status` | GET | System health check |
| `/system/tools` | GET | Available AI tools |
| `/tickets/stats` | GET | Support ticket statistics |

### **Example API Usage**

```javascript
// Enhanced chat with all AI features
const response = await fetch('http://localhost:8000/chat/enhanced', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    message: "My laptop won't connect to WiFi",
    session_id: "user-123",
    use_vector_search: true,
    use_rag: true,
    use_agent: true
  })
});
```

## 🧪 Testing & Validation

### **Feature Testing Guide**

We've included a comprehensive testing guide: [IT_Feature_Testing_Guide.md](./IT_Feature_Testing_Guide.md)

**Quick Validation Tests:**

```bash
# Test 1: Vector Search
curl -X POST "http://localhost:8000/chat/vector-search" \
  -H "Content-Type: application/json" \
  -d '{"message": "VPN troubleshooting", "session_id": "test"}'

# Test 2: Function Calling
curl -X POST "http://localhost:8000/chat/agent" \
  -H "Content-Type: application/json" \
  -d '{"message": "Create ticket for printer issue", "session_id": "test"}'

# Test 3: RAG with Memory
curl -X POST "http://localhost:8000/chat/rag" \
  -H "Content-Type: application/json" \
  -d '{"message": "What is our backup policy?", "session_id": "test"}'

# Test 4: Enhanced Mode (All Features)
curl -X POST "http://localhost:8000/chat/enhanced" \
  -H "Content-Type: application/json" \
  -d '{"message": "Help me with email setup and create a ticket", "session_id": "test"}'
```

## 🎯 Core Features Validation

### ✅ **PineCone Vector Search**
- **Status**: ✅ Implemented & Tested
- **Capabilities**: Multi-namespace semantic search, real-time knowledge retrieval
- **Test**: Search for "VPN setup" returns relevant configuration guides

### ✅ **Function Calling Agent**
- **Status**: ✅ Implemented & Tested  
- **Capabilities**: 8+ tools including ticket creation, system info, batch processing
- **Test**: "Create ticket for printer issue" automatically creates categorized ticket

### ✅ **LangChain RAG Management**
- **Status**: ✅ Implemented & Tested
- **Capabilities**: Conversation memory, retrieval-augmented responses, context chains
- **Test**: Follow-up questions maintain conversation context across turns

### ✅ **Enhanced Prompt Handling**
- **Status**: ✅ Implemented & Tested
- **Capabilities**: Multi-query processing, mode detection, batch request handling
- **Test**: "Help with email AND create a ticket" processes both requests intelligently

## 📂 Project Structure

```
it-helpdesk-bot-personal/
├── 📁 backend/                    # FastAPI backend application
│   ├── 📄 main.py                 # FastAPI app with all endpoints
│   ├── 📄 models.py               # Pydantic data models
│   ├── 📄 context_manager.py      # Session & conversation management
│   ├── 📁 tools/                  # AI component modules
│   │   ├── 📄 pinecone_handler.py     # Vector database manager
│   │   ├── 📄 langchain_manager.py    # RAG & conversation chains
│   │   ├── 📄 enhanced_function_handler.py # Function calling agent
│   │   └── 📄 voice_handler.py         # Text-to-speech integration
│   └── 📁 data/                   # Mock data & initialization
├── 📁 frontend/                   # React frontend application
│   ├── 📁 src/
│   │   ├── 📄 App.jsx             # Main application component
│   │   ├── 📄 api.js              # API integration functions
│   │   └── 📁 components/         # React UI components
│   │       ├── 📄 ChatWindow.jsx      # Chat interface
│   │       ├── 📄 MessageBubble.jsx   # Message display
│   │       └── 📄 SmartQuickActions.jsx # Quick action buttons
│   ├── 📄 package.json            # Frontend dependencies
│   └── 📄 vite.config.js          # Vite configuration
├── 📄 requirements.txt            # Python dependencies
├── 📄 setup_enhanced.sh          # Automated setup script
├── 📄 env.template               # Environment variables template
└── 📄 IT_Feature_Testing_Guide.md # Comprehensive testing documentation
```

## 🔧 Development & Troubleshooting

### **Common Issues & Solutions**

**❌ PineCone Connection Issues**
```bash
# Check API key and index name
python -c "from backend.tools.pinecone_handler import get_vector_store_manager; get_vector_store_manager()"
```

**❌ Azure OpenAI API Errors**
```bash
# Verify API credentials
python -c "from backend.openai_client import get_openai_client; get_openai_client()"
```

**❌ Frontend Build Issues**
```bash
cd frontend
rm -rf node_modules package-lock.json
npm install
```

### **Development Tips**

- **Hot Reload**: Both backend (uvicorn) and frontend (Vite) support hot reload
- **API Testing**: Use the interactive docs at http://localhost:8000/docs
- **Debugging**: Check browser console and FastAPI logs for errors
- **Performance**: Monitor vector search response times in system status

## 🚀 Deployment

### **Production Considerations**

1. **Environment Security**: Use production API keys and secure endpoints
2. **Vector Database**: Configure PineCone for production scale
3. **Monitoring**: Implement logging and health checks
4. **Performance**: Optimize vector search and API response times

### **Docker Deployment** (Optional)

```bash
# Build and run with Docker Compose
docker-compose up --build
```

## 🤝 Contributing

1. **Fork the repository**
2. **Create feature branch**: `git checkout -b feature/amazing-feature`
3. **Follow the project structure** and coding conventions
4. **Test all AI features** using the testing guide
5. **Submit pull request** with comprehensive description

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 📞 Support

For issues, questions, or feature requests:
- **Create an issue** in the repository
- **Check the testing guide** for validation steps
- **Review API documentation** at `/docs` endpoint

---

**🎯 Ready to revolutionize IT support with AI? Get started in 5 minutes with our automated setup!**

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
│   ├── functions.py          # Tool functions and vector store integration
│   ├── context_manager.py    # Session and context management
│   ├── ticket_management.py  # Enhanced ticket system
│   ├── knowledge_base.py     # Legacy knowledge base
│   ├── tools/                # Enhanced feature modules
│   │   ├── __init__.py       # Package initialization
│   │   ├── knowledge_handler.py # Unified knowledge base handler
│   │   ├── pinecone_handler.py  # Pinecone vector store handler
│   │   ├── langchain_manager.py # LangChain RAG integration
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
├── logs/                     # Application logs directory
├── requirements.txt          # Python dependencies (enhanced)
├── setup_enhanced.sh         # Easy setup script
├── env.template             # Environment variables template
├── package.json             # Root package.json for workspace
└── README.md                # This documentation
```

## 🚀 Enhanced Features Guide

### Pinecone Vector Knowledge Base
The enhanced bot uses Pinecone vector store for semantic search across organized namespaces:

**FAQs Namespace**: Common IT questions and solutions
- Password reset procedures
- VPN setup instructions
- Email configuration
- WiFi troubleshooting

**KB Articles Namespace**: Comprehensive software guides and procedures
- Microsoft Office 365 setup
- Slack configuration
- Zoom installation
- Development tools (Git, VS Code)

**Policies Namespace**: IT policies and procedures
- Password policies
- Software installation rules
- Data backup requirements
- Remote work guidelines

**Troubleshooting Namespace**: Advanced diagnostic procedures
- System diagnostics
- Network troubleshooting
- Hardware issue resolution
- Performance optimization

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
- **POST** `/chat` - Standard chat with Pinecone vector knowledge base
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