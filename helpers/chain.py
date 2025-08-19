# helpers/chain.py

from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser
from langchain_groq import ChatGroq
from langchain.retrievers import ContextualCompressionRetriever


def _format_docs(docs: list) -> str:
    """
    Formats the retrieved documents into a single string for the LLM.
    """
    if not docs:
        return "No relevant context found."
    return "\n\n".join(doc.page_content for doc in docs)


def create_rag_chain(retriever: ContextualCompressionRetriever):
    """
    Creates the full RAG chain for question answering using Groq.

    Args:
        retriever (ContextualCompressionRetriever): Retriever with reranking.

    Returns:
        Runnable: A runnable RAG pipeline.
    """

    # 1. Initialize Groq LLM (Llama-3 is super fast here)
    llm = ChatGroq(
        temperature=0,   # deterministic answers
        model_name="llama3-8b-8192"  # Groq's recommended fast model
    )

    # 2. Define the system prompt
    prompt_template = """
    You are an assistant specialized in Ethiopian startup and business registration law.
    Use ONLY the following context to answer the user's question.
    If the answer is not in the context, say:
    "The answer is not available in the provided documents."

    Context:
    {context}

    Question:
    {question}

    Answer:
    """

    prompt = ChatPromptTemplate.from_template(prompt_template)

    # 3. Define the chain
    rag_chain = (
        {
            "context": retriever | _format_docs, 
            "question": RunnablePassthrough()
        }
        | prompt
        | llm
        | StrOutputParser()
    )

    return rag_chain
