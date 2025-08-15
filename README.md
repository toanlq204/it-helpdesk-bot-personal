# IT Helpdesk Bot - Personal Assistant

A full-stack AI-powered IT helpdesk chatbot that provides instant support for common IT issues, FAQs, software information, and ticket management. Built with FastAPI backend and React frontend, powered by Azure OpenAI.

## 🌟 Features

- **🤖 AI-Powered Chat Assistant**: Intelligent responses using Azure OpenAI's GPT-4o-mini
- **💡 FAQ Lookup**: Instant answers to frequently asked IT questions
- **🎫 Ticket Management**: Create and track support tickets
- **📦 Software Catalog**: Get information about available software and installation links
- **💬 Multi-Query Support**: Handle multiple questions in a single message
- **📱 Responsive Design**: Modern UI built with React and Tailwind CSS
- **🔄 Real-time Updates**: Live chat interface with session management

## 🛠️ Tech Stack

### Backend
- **FastAPI**: High-performance Python web framework
- **Azure OpenAI**: GPT-4o-mini for intelligent responses
- **Pydantic**: Data validation and serialization
- **Uvicorn**: ASGI server for production

### Frontend
- **React 18**: Modern React with hooks
- **Vite**: Fast development build tool
- **Tailwind CSS**: Utility-first CSS framework
- **JavaScript ES6+**: Modern JavaScript features

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- Node.js 16+
- Azure OpenAI API access

### 1. Clone the Repository
```bash
git clone https://github.com/toanlq204/it-helpdesk-bot-personal.git
cd it-helpdesk-bot-personal
```

### 2. Backend Setup

#### Create Virtual Environment
```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

#### Install Dependencies
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
│   ├── functions.py           # Tool functions (FAQ, tickets, software)
│   └── mock_data.py           # Sample data for testing
├── frontend/                   # React frontend
│   ├── src/
│   │   ├── App.jsx           # Main application component
│   │   ├── api.js            # API communication layer
│   │   └── components/
│   │       ├── ChatWindow.jsx    # Chat interface component
│   │       └── MessageBubble.jsx # Individual message component
│   ├── index.html            # HTML template
│   ├── package.json          # Frontend dependencies
│   ├── tailwind.config.js    # Tailwind CSS configuration
│   └── vite.config.js        # Vite build configuration
├── requirements.txt           # Python dependencies
├── package.json              # Root package configuration
├── env.template              # Environment variables template
└── README.md                 # Project documentation
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