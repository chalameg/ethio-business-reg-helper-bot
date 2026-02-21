"""
Session-based conversation memory. No LangChain memory dependency; works on all environments.
"""
from typing import List, Any
import streamlit as st

# Message-like object for sidebar compatibility (.content, .type)
class _Message:
    def __init__(self, content: str, type: str):
        self.content = content
        self.type = type  # "human" or "ai"

_SESSION_KEY = "chat_history"
_MEMORY_KEY = "conversation_memory"
_DEFAULT_K = 5


def _ensure_chat_history():
    if _SESSION_KEY not in st.session_state:
        st.session_state[_SESSION_KEY] = []


def create_conversation_memory(k: int = _DEFAULT_K) -> Any:
    """
    Creates a conversation memory component (session-based). Remembers last k exchanges.
    Returns a thin wrapper for compatibility with existing code.
    """
    _ensure_chat_history()
    # Store k in session for the wrapper
    if "chat_memory_k" not in st.session_state:
        st.session_state["chat_memory_k"] = k
    return _SessionMemoryWrapper()


class _SessionMemoryWrapper:
    """Wrapper that provides save_context and chat_memory.messages using session state."""

    @property
    def chat_memory(self):
        _ensure_chat_history()
        k = st.session_state.get("chat_memory_k", _DEFAULT_K)
        messages = st.session_state[_SESSION_KEY][-(2 * k):]
        return type("ChatMemory", (), {"messages": messages})()


def get_memory_from_session() -> _SessionMemoryWrapper:
    """Gets or creates conversation memory from Streamlit session state."""
    _ensure_chat_history()
    if _MEMORY_KEY not in st.session_state:
        st.session_state[_MEMORY_KEY] = _SessionMemoryWrapper()
    return st.session_state[_MEMORY_KEY]


def add_to_memory(question: str, answer: str):
    """Adds a question-answer pair to the conversation memory."""
    _ensure_chat_history()
    st.session_state[_SESSION_KEY].append(_Message(question, "human"))
    st.session_state[_SESSION_KEY].append(_Message(answer, "ai"))
    k = st.session_state.get("chat_memory_k", _DEFAULT_K)
    st.session_state[_SESSION_KEY] = st.session_state[_SESSION_KEY][-(2 * k):]


def clear_memory():
    """Clears the conversation memory."""
    st.session_state[_SESSION_KEY] = []
    st.session_state[_MEMORY_KEY] = _SessionMemoryWrapper()


def get_conversation_history() -> List[_Message]:
    """Returns the current conversation history (message-like objects with .content and .type)."""
    _ensure_chat_history()
    return st.session_state[_SESSION_KEY]


def get_memory_summary() -> str:
    """Returns a short summary of the conversation memory."""
    _ensure_chat_history()
    n = len(st.session_state[_SESSION_KEY])
    return f"Memory contains {n} messages" if n else "No conversation history"
