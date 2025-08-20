# Ethio Startup Advisor - FastAPI Backend

This is the FastAPI backend for the Ethio Startup Advisor application. It provides the AI/RAG functionality for processing documents and answering questions about Ethiopian business law.

## 🚀 Features

- **Document Processing**: Load and process PDF documents from the data folder
- **RAG System**: AI-powered question answering using LangChain
- **Memory System**: Conversation memory for contextual responses
- **Vector Search**: FAISS-based document retrieval
- **RESTful API**: Clean endpoints for frontend integration

## 🛠️ Setup

### 1. Install Dependencies
```bash
cd backend
pip install -r requirements.txt
```

### 2. Environment Variables
Create a `.env` file in the backend directory:
```bash
GROQ_API_KEY=your_groq_api_key_here
```

### 3. Run the Server
```bash
python main.py
```

The server will start on `http://localhost:8000`

## 📡 API Endpoints

### Health Check
- `GET /` - Root endpoint
- `GET /health` - Health check
- `GET /status` - System status

### Document Processing
- `POST /process-documents` - Process documents from data folder
- `POST /reprocess-documents` - Reprocess documents

### Q&A
- `POST /ask-question` - Ask a question and get an answer

## 🔧 Usage

### 1. Start the Backend
```bash
cd backend
python main.py
```

### 2. Process Documents
```bash
curl -X POST "http://localhost:8000/process-documents"
```

### 3. Ask a Question
```bash
curl -X POST "http://localhost:8000/ask-question" \
  -H "Content-Type: application/json" \
  -d '{"question": "What are the requirements for registering a private limited company?"}'
```

## 📁 Project Structure

```
backend/
├── main.py              # FastAPI application
├── requirements.txt     # Python dependencies
└── README.md           # This file
```

## 🔗 Frontend Integration

This backend is designed to work with the Next.js frontend. The frontend will call these API endpoints to:

- Process documents
- Ask questions
- Get system status
- Manage the RAG system

## 🚨 Important Notes

- **Data Folder**: The backend expects a `../data` folder with PDF documents
- **Helpers**: Uses the existing helpers from the parent directory
- **Memory**: Conversation memory is stored in memory (not persistent)
- **State**: Uses global variables (not suitable for production with multiple users)

## 🔮 Future Enhancements

- Database integration for persistent storage
- User authentication and authorization
- Document upload endpoints
- Chat history storage
- Multiple user support
