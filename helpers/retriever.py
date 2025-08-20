from langchain.retrievers import ContextualCompressionRetriever
from langchain.retrievers.document_compressors import CrossEncoderReranker
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
    
    # 1. Base retriever (dense retrieval from FAISS)
    base_retriever = vectorstore.as_retriever(search_kwargs={"k": search_k})

    # 2. Load HuggingFace cross-encoder for reranking
    cross_encoder_model = HuggingFaceCrossEncoder(model_name=model_name)

    # 3. Create reranker
    reranker = CrossEncoderReranker(
        model=cross_encoder_model,
        top_n=reranker_top_n
    )

    # 4. Wrap base retriever with reranker
    compression_retriever = ContextualCompressionRetriever(
        base_compressor=reranker, 
        base_retriever=base_retriever
    )

    return compression_retriever
