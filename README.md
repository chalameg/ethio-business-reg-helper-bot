# 🇪🇹 Ethio Startup Advisor

> **AI-powered Ethiopian business law advisor with dual architecture support**

This project provides an intelligent assistant for Ethiopian entrepreneurs, offering guidance on business registration, licensing, and investment rules. Built with RAG (Retrieval-Augmented Generation) technology, it draws from official government proclamations and legal codes.

## 🏗️ **Project Architecture**

This project now supports **two different architectures**:

### **🚀 Option 1: Streamlit App (Original)**
- **Single-file application** with integrated UI and AI
- **Easy deployment** on Streamlit Cloud
- **Quick setup** for prototyping and testing
- **File**: `app.py`

### **⚡ Option 2: Next.js + FastAPI (Modern)**
- **Separated frontend and backend** for scalability
- **Modern web interface** with responsive design
- **Professional deployment** options (Vercel, Railway, etc.)
- **Files**: `frontend/` and `backend/` directories

## 🎯 **Choose Your Setup**

| Feature | Streamlit | Next.js + FastAPI |
|---------|-----------|-------------------|
| **Setup Speed** | ⚡ Fast (1 file) | 🚀 Moderate (2 directories) |
| **UI Quality** | 🟡 Good | 🟢 Excellent |
| **Mobile Experience** | 🟡 Basic | 🟢 Responsive |
| **Deployment** | 🟢 Streamlit Cloud | 🟢 Vercel + Railway |
| **Scalability** | 🟡 Limited | 🟢 High |
| **Customization** | 🟡 Limited | 🟢 Unlimited |

## 🚀 **Quick Start - Choose Your Path**
<!-- conda activate youtube-rag -->
### **Path A: Streamlit (Recommended for Quick Start)**
```bash
# Install dependencies
pip install -r requirements.txt

# Run the app
streamlit run app.py
```

### **Path B: Next.js + FastAPI (Recommended for Production)**
```bash
# Backend
cd backend
pip install -r requirements.txt
python main.py

# Frontend (in new terminal)
cd frontend
npm install
npm run dev
```

## 📁 **Project Structure**

```
ethio-startup-advisor/
├── 📱 app.py                    # Streamlit app (Option 1)
├── 🐍 requirements.txt          # Python dependencies
├── 📚 helpers/                  # AI/RAG components
│   ├── chain.py                # RAG chain logic
│   ├── chunker.py              # Document chunking
│   ├── loader.py               # PDF document loading
│   ├── memory.py               # Conversation memory
│   ├── retriever.py            # Document retrieval
│   └── vectorstore.py          # FAISS vector database
├── 📁 data/                    # Legal documents (PDFs)
├── 🆕 backend/                 # FastAPI server (Option 2)
│   ├── main.py                 # FastAPI application
│   ├── requirements.txt        # Backend dependencies
│   └── README.md               # Backend setup guide
├── 🆕 frontend/                # Next.js app (Option 2)
│   ├── src/app/                # React components
│   ├── package.json            # Frontend dependencies
│   └── README.md               # Frontend setup guide
├── 📖 README.md                # This file
└── 🚫 .gitignore               # Git ignore rules
```

## 🌟 **Key Features**

- **🤖 AI-Powered Q&A**: Get instant answers about Ethiopian business law
- **📚 Legal Source Integration**: Based on official government documents
- **💬 Conversation Memory**: Context-aware responses
- **📱 Responsive Design**: Works on desktop, tablet, and mobile
- **🔍 Smart Document Search**: FAISS-based vector search with reranking
- **🌍 Ethiopian Focus**: Specialized for Ethiopian business environment

## 🎯 **Target Users**

- **Entrepreneurs** starting businesses in Ethiopia
- **Startup founders** seeking legal guidance
- **Small business owners** needing compliance information
- **Foreign investors** exploring Ethiopian opportunities
- **Legal professionals** requiring quick reference

## 📋 **Supported Topics**

- **🏢 Business Registration**: Private Limited Company, Share Company, Sole Proprietorship
- **📋 Licensing & Permits**: Trade licenses, business permits
- **💰 Minimum Capital Requirements**: Financial requirements for different business types
- **🌍 Foreign Investment Rules**: Investment regulations and restrictions
- **💸 Tax Obligations**: High-level tax information from proclamations

## 🛠️ **Technology Stack**

### **AI & RAG Components**
- **LangChain**: RAG pipeline orchestration
- **GROQ**: Fast LLM inference (Llama-3 model)
- **FAISS**: Vector database for document search
- **HuggingFace**: Document embeddings and reranking

### **Frontend Options**
- **Streamlit**: Python-based UI (Option 1)
- **Next.js**: React-based modern UI (Option 2)
- **Tailwind CSS**: Utility-first styling (Option 2)

### **Backend Options**
- **Streamlit**: Integrated backend (Option 1)
- **FastAPI**: Modern Python API (Option 2)

## 🚀 **Deployment Options**

### **Streamlit App**
- **Streamlit Cloud**: Free hosting with automatic deployment
- **Heroku**: Traditional Python hosting
- **Railway**: Modern Python hosting

### **Next.js + FastAPI**
- **Frontend**: Vercel, Netlify, or any static hosting
- **Backend**: Railway, Render, or any Python hosting
- **Database**: FAISS files stored in cloud storage

## 🔧 **Environment Setup**

### **Required Environment Variables**
```bash
GROQ_API_KEY=your_groq_api_key_here
```

### **Document Requirements**
Place your Ethiopian legal documents (PDFs) in the `data/` folder:
- Ethiopian Commercial Code (2021)
- Investment Proclamation No. 1180/2020
- Trade Registration Proclamation No. 980/2016
- Tax Proclamations

## 📚 **Documentation**

- **[Streamlit App Guide](app.py)**: Single-file application
- **[Backend API Guide](backend/README.md)**: FastAPI server setup
- **[Frontend Guide](frontend/README.md)**: Next.js application setup

## 🤝 **Contributing**

1. **Choose your architecture** (Streamlit or Next.js+FastAPI)
2. **Fork the repository**
3. **Create a feature branch**
4. **Make your changes**
5. **Submit a pull request**

## 📄 **License**

This project is open source and available under the [MIT License](LICENSE).

## 🆘 **Support**

- **Issues**: Report bugs and feature requests
- **Discussions**: Ask questions and share ideas
- **Wiki**: Detailed setup and usage guides

---

**🇪🇹 Empowering Ethiopian entrepreneurs with AI-powered legal guidance**
