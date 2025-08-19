# 🇪🇹 Ethio Startup Advisor

A Streamlit-based RAG (Retrieval-Augmented Generation) application that provides instant, accurate answers about Ethiopian business law directly from official government proclamations and legal codes. Perfect for entrepreneurs, startup founders, and small business owners who need reliable guidance on business registration, licensing, and compliance.

## 🚀 Features

- **Official Legal Sources**: Based on Ethiopian Commercial Code, Investment Proclamations, and Trade Regulations
- **AI-Powered Legal Guidance**: Get instant answers about Ethiopian business law and regulations
- **Startup-Focused**: Tailored for entrepreneurs, startup founders, and small business owners
- **Comprehensive Coverage**: Business registration, licensing, foreign investment, and tax compliance
- **Fast & Accurate**: Powered by GROQ's Llama-3 model for reliable responses
- **User-Friendly**: Clean Streamlit interface with common question examples

## 🏗️ Architecture

The application uses a modern RAG pipeline:

```
Documents → Chunking → Vector Embeddings → Chroma DB → Retrieval → Reranking → LLM → Response
```

### Components

- **`app.py`**: Main Streamlit application and UI
- **`helpers/chunker.py`**: Document text splitting and chunking
- **`helpers/loader.py`**: PDF document loading and processing
- **`helpers/vectorstore.py`**: Chroma vector database management
- **`helpers/retriever.py`**: Advanced document retrieval with reranking
- **`helpers/chain.py`**: RAG chain construction and LLM integration

## 📋 Prerequisites

- Python 3.8+
- GROQ API key (for LLM functionality)
- PDF documents related to Ethiopian business law

## 🛠️ Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd startup-bot
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment variables**
   Create a `.env` file in the project root:
   ```bash
   GROQ_API_KEY=your_groq_api_key_here
   ```

4. **Prepare your documents**
   Place PDF files related to Ethiopian business law in the `./data` folder.

## 🚀 Usage

1. **Start the application**
   ```bash
   streamlit run app.py
   ```

2. **Load documents**
   - Click "Process Documents" in the sidebar
   - Wait for the processing to complete
   - You'll see a success message when ready

3. **Ask questions**
   - Type your question about Ethiopian business registration
   - Get instant AI-powered answers based on your documents

## 📚 Sample Questions

The application can answer questions about:

- **Business Registration**: Types of entities, requirements, process
- **Startup Ecosystem**: Incubators, funding, government support
- **Tax Compliance**: Corporate tax, VAT, withholding tax, filing requirements
- **Legal Requirements**: Permits, licenses, compliance obligations
- **Investment**: Foreign investment rules, incentives, restrictions

## 🔧 Configuration

### Environment Variables

| Variable | Description | Required |
|----------|-------------|----------|
| `GROQ_API_KEY` | Your GROQ API key for LLM access | Yes |

### Model Configuration

The application uses:
- **Embeddings**: `sentence-transformers/all-MiniLM-L6-v2`
- **LLM**: `llama3-8b-8192` (via Groq)
- **Reranker**: `cross-encoder/ms-marco-MiniLM-L-6-v2`

### Chunking Settings

- **Chunk Size**: 800 characters
- **Chunk Overlap**: 100 characters
- **Separators**: Article breaks, newlines, spaces

## 📁 Project Structure

```
ethio-startup-advisor/
├── app.py                 # Main Streamlit application
├── requirements.txt       # Python dependencies
├── .env                  # Environment variables (create this)
├── data/                 # PDF documents folder
├── helpers/              # Core functionality modules
│   ├── chain.py         # RAG chain construction
│   ├── chunker.py       # Document chunking
│   ├── loader.py        # Document loading
│   ├── retriever.py     # Document retrieval
│   └── vectorstore.py   # Vector database management
└── README.md            # This file
```

## 🧪 Testing

1. **Add sample documents** to the `./data` folder
2. **Start the application** with `streamlit run app.py`
3. **Process documents** using the sidebar button
4. **Ask test questions** about Ethiopian business topics

## 🔍 Troubleshooting

### Common Issues

1. **GROQ API Key Error**
   - Ensure your `.env` file contains the correct API key
   - Verify the API key is valid and has sufficient credits

2. **Document Processing Fails**
   - Check that PDF files are in the `./data` folder
   - Ensure PDFs are not corrupted or password-protected
   - Verify all dependencies are installed correctly

3. **Vector Database Errors**
   - Delete the `startup_db` folder if it exists
   - Restart the application and reprocess documents

4. **Memory Issues**
   - Reduce chunk size in `helpers/chunker.py`
   - Process fewer documents at once
   - Use smaller embedding models

### Performance Optimization

- **Faster Processing**: Use smaller chunk sizes
- **Better Quality**: Increase chunk overlap
- **Memory Efficiency**: Process documents in batches

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- **Streamlit** for the web application framework
- **LangChain** for the RAG pipeline components
- **Groq** for fast LLM inference
- **Chroma** for vector database functionality
- **HuggingFace** for embedding and reranking models

## 📞 Support

For issues and questions:
- Check the troubleshooting section above
- Review the error messages in the Streamlit interface
- Ensure all dependencies are correctly installed
- Verify your GROQ API key is valid

---

**Note**: This application is designed for educational and informational purposes. Always consult with legal professionals for official business advice regarding Ethiopian business law and regulations.
