# helpers/memory.py

try:
    from langchain.memory import ConversationBufferWindowMemory
except ModuleNotFoundError:
    from langchain_classic.memory import ConversationBufferWindowMemory

try:
    from langchain_core.memory import BaseMemory
except ModuleNotFoundError:
    from langchain_classic.memory import BaseMemory

import streamlit as st


def create_conversation_memory(k: int = 5) -> BaseMemory:
    """
    Creates a conversation memory component that remembers the last k exchanges.
    
    Args:
        k (int): Number of conversation turns to remember (default: 5)
    
    Returns:
        BaseMemory: Conversation memory component
    """
    return ConversationBufferWindowMemory(
        k=k,
        return_messages=True,
        memory_key="chat_history"
    )


def get_memory_from_session() -> BaseMemory:
    """
    Gets or creates conversation memory from Streamlit session state.
    
    Returns:
        BaseMemory: Conversation memory component
    """
    if "conversation_memory" not in st.session_state:
        st.session_state.conversation_memory = create_conversation_memory()
    
    return st.session_state.conversation_memory


def add_to_memory(question: str, answer: str):
    """
    Adds a question-answer pair to the conversation memory.
    
    Args:
        question (str): User's question
        answer (str): AI's answer
    """
    memory = get_memory_from_session()
    if memory and hasattr(memory, 'save_context'):
        try:
            memory.save_context(
                {"input": question},
                {"output": answer}
            )
        except Exception as e:
            # If memory fails, just continue without it
            pass


def clear_memory():
    """
    Clears the conversation memory.
    """
    if "conversation_memory" in st.session_state:
        del st.session_state.conversation_memory
    st.session_state.conversation_memory = create_conversation_memory()


def get_conversation_history() -> list:
    """
    Gets the current conversation history.
    
    Returns:
        list: List of conversation messages
    """
    memory = get_memory_from_session()
    if memory and hasattr(memory, 'chat_memory') and memory.chat_memory:
        return memory.chat_memory.messages
    return []


def get_memory_summary() -> str:
    """
    Gets a summary of the conversation memory.
    
    Returns:
        str: Summary of conversation
    """
    memory = get_memory_from_session()
    if memory and hasattr(memory, 'chat_memory') and memory.chat_memory and memory.chat_memory.messages:
        return f"Memory contains {len(memory.chat_memory.messages)} messages"
    return "No conversation history"
