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
- **HuggingFace TTS**: Text-to-speech capabilities
- **Pydantic**: Data validation and serialization

### Frontend
- **React 18**: Modern React with hooks
- **Vite**: Fast development build tool
- **Tailwind CSS**: Utility-first CSS framework
- **Audio API**: Browser audio playback for voice responses

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- Node.js 16+
- Azure OpenAI API access
- HuggingFace API token (optional, for TTS)

### Easy Setup Script
```bash
git clone https://github.com/toanlq204/it-helpdesk-bot-personal.git
cd it-helpdesk-bot-personal
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
AZURE_OPENAI_API_KEY=your-azure-openai-api-key
AZURE_OPENAI_ENDPOINT=https://your-resource-name.openai.azure.com/
AZURE_OPENAI_API_VERSION=2024-07-01-preview
MODEL_NAME=gpt-4o-mini
```

### 3. Frontend Setup
```bash
cd frontend
npm install
```

### 4. Run the Application

#### Start Backend (Terminal 1)
```bash
# From project root
uvicorn backend.main:app --reload --port 8000
```

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

## 📁 Project Structure

```
it-helpdesk-bot-personal/
├── backend/                    # FastAPI backend
│   ├── main.py                # Main application and chat endpoint
│   ├── models.py              # Pydantic data models
│   ├── openai_client.py       # Azure OpenAI client configuration
│   ├── functions.py           # Tool functions and ChromaDB integration
│   ├── context_manager.py     # Session and context management
│   ├── ticket_management.py   # Enhanced ticket system
│   ├── knowledge_base.py      # Legacy knowledge base
│   ├── tools/                 # Enhanced feature modules
│   │   ├── faq_handler.py     # ChromaDB knowledge base handler
│   │   └── voice_handler.py   # HuggingFace TTS integration
│   └── data/                  # Knowledge base data
│       └── mock_data.py       # IT knowledge database
├── frontend/                   # React frontend
│   ├── src/
│   │   ├── App.jsx           # Main application with audio support
│   │   ├── api.js            # API communication layer
│   │   └── components/
│   │       ├── ChatWindow.jsx    # Chat interface with audio playback
│   │       └── MessageBubble.jsx # Message component with audio indicators
│   ├── index.html            # HTML template
│   ├── package.json          # Frontend dependencies
│   ├── tailwind.config.js    # Tailwind CSS configuration
│   └── vite.config.js        # Vite build configuration
├── chromadb_data/             # ChromaDB persistent storage
├── requirements.txt           # Python dependencies (enhanced)
├── setup_enhanced.sh          # Easy setup script
├── env.template              # Environment variables (updated)
└── README.md                 # This documentation

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