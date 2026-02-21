"""
Retriever with cross-encoder reranking. Uses langchain_classic (stable on LangChain 1.x).
"""
from langchain_classic.retrievers import ContextualCompressionRetriever
from langchain_classic.retrievers.document_compressors import CrossEncoderReranker
from langchain_community.cross_encoders import HuggingFaceCrossEncoder
from langchain_community.vectorstores import FAISS


def create_retriever(
    vectorstore: FAISS,
    search_k: int = 10,
    reranker_top_n: int = 3,
    model_name: str = "cross-encoder/ms-marco-MiniLM-L-6-v2"
):
    """
    Create a retriever with cross-encoder reranking for higher-quality search.

    Args:
        vectorstore (FAISS): The FAISS vectorstore instance.
        search_k (int): Number of candidates to fetch from vectorstore.
        reranker_top_n (int): Number of top documents to keep after reranking.
        model_name (str): HuggingFace cross-encoder model for reranking.

    Returns:
        ContextualCompressionRetriever: Enhanced retriever with reranking.
    """
    base_retriever = vectorstore.as_retriever(search_kwargs={"k": search_k})
    cross_encoder_model = HuggingFaceCrossEncoder(model_name=model_name)
    reranker = CrossEncoderReranker(
        model=cross_encoder_model,
        top_n=reranker_top_n
    )
    compression_retriever = ContextualCompressionRetriever(
        base_compressor=reranker,
        base_retriever=base_retriever
    )
    return compression_retriever
