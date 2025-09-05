from fastapi import FastAPI, HTTPException, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel
import os
import sys
from pathlib import Path
from dotenv import load_dotenv
from datetime import datetime

# Load environment variables first
load_dotenv("../.env")

# Add parent directory to path to import helpers
sys.path.append(str(Path(__file__).parent.parent))

from helpers.chunker import chunk_documents
from helpers.loader import load_documents
from helpers.vectorstore import create_or_load_vectorstore, load_vectorstore
from helpers.retriever import create_retriever
from helpers.chain import create_rag_chain
from helpers.memory import create_conversation_memory, add_to_memory

app = FastAPI(
    title="Ethio Startup Advisor API",
    description="AI-powered Ethiopian business law advisor",
    version="1.0.0"
)

# CORS middleware for frontend communication
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:3001"],  # Next.js default ports
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global state (in production, use proper state management)
vector_store = None
retriever = None
rag_chain = None
memory = None
docs_processed = False
chat_history = []  # Add chat history storage

class QuestionRequest(BaseModel):
    question: str

class ProcessResponse(BaseModel):
    message: str
    success: bool
    document_count: int = None

class AnswerResponse(BaseModel):
    answer: str
    success: bool

@app.get("/")
async def root():
    return {"message": "Ethio Startup Advisor API is running!"}

@app.get("/health")
async def health_check():
    return {"status": "healthy", "docs_processed": docs_processed}

@app.post("/process-documents", response_model=ProcessResponse)
async def process_documents():
    """Process documents from the data folder"""
    global vector_store, retriever, rag_chain, memory, docs_processed
    
    try:
        # Check if data folder exists
        data_path = Path("../data")
        if not data_path.exists():
            raise HTTPException(status_code=400, detail="Data folder not found")
        
        # Load and process documents
        docs = load_documents(str(data_path))
        if not docs:
            raise HTTPException(status_code=400, detail="No documents found in data folder")
        
        # Chunk documents
        chunks = chunk_documents(docs)
        
        # Create or load vector store
        vector_store = create_or_load_vectorstore(chunks)
        
        # Create retriever
        retriever = create_retriever(vector_store)
        
        # Create memory
        memory = create_conversation_memory()
        
        # Create RAG chain
        rag_chain = create_rag_chain(retriever)
        
        docs_processed = True
        
        return ProcessResponse(
            message="Documents processed successfully!",
            success=True,
            document_count=len(chunks)
        )
        
    except Exception as e:
        import traceback
        print(f"Error processing documents: {str(e)}")
        print(f"Traceback: {traceback.format_exc()}")
        raise HTTPException(status_code=500, detail="Failed to process documents. Please try again.")

@app.post("/ask-question", response_model=AnswerResponse)
async def ask_question(request: QuestionRequest):
    """Ask a question and get an answer"""
    global rag_chain, memory, docs_processed, chat_history
    
    if not docs_processed or not rag_chain:
        raise HTTPException(status_code=400, detail="Please process documents first.")
    
    try:
        # Get answer from RAG chain
        answer = rag_chain.invoke(request.question)
        
        # Add to chat history
        chat_history.append({
            "question": request.question,
            "answer": answer,
            "timestamp": str(datetime.now())
        })
        
        # Keep only last 10 conversations
        if len(chat_history) > 10:
            chat_history.pop(0)
        
        # Add to memory
        if memory:
            add_to_memory(request.question, answer)
        
        return AnswerResponse(
            answer=answer,
            success=True
        )
        
    except Exception as e:
        import traceback
        print(f"Error processing question: {str(e)}")
        print(f"Traceback: {traceback.format_exc()}")
        raise HTTPException(status_code=500, detail="Failed to process question. Please try again.")

@app.get("/chat-history")
async def get_chat_history():
    """Get chat history"""
    return {"chat_history": chat_history}

@app.delete("/chat-history")
async def clear_chat_history():
    """Clear chat history"""
    global chat_history
    chat_history = []
    return {"message": "Chat history cleared"}

@app.get("/status")
async def get_status():
    """Get current system status"""
    return {
        "docs_processed": docs_processed,
        "vector_store_ready": vector_store is not None,
        "retriever_ready": retriever is not None,
        "rag_chain_ready": rag_chain is not None,
        "memory_ready": memory is not None
    }

@app.post("/reprocess-documents", response_model=ProcessResponse)
async def reprocess_documents():
    """Reprocess documents (useful for updates)"""
    global vector_store, retriever, rag_chain, memory, docs_processed
    
    try:
        # Reset state
        vector_store = None
        retriever = None
        rag_chain = None
        memory = None
        docs_processed = False
        
        # Process documents again
        return await process_documents()
        
    except Exception as e:
        import traceback
        print(f"Error reprocessing documents: {str(e)}")
        print(f"Traceback: {traceback.format_exc()}")
        raise HTTPException(status_code=500, detail=f"Error reprocessing documents: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
