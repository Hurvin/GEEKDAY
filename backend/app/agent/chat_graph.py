from __future__ import annotations

from langgraph.graph import END, StateGraph

from app.agent.chat_nodes import generate_chat_reply_node, persist_context_node, prepare_context_node
from app.agent.chat_state import ChatState


def build_chat_graph():
    graph = StateGraph(ChatState)
    graph.add_node("prepareContextNode", prepare_context_node)
    graph.add_node("generateChatReplyNode", generate_chat_reply_node)
    graph.add_node("persistContextNode", persist_context_node)
    graph.set_entry_point("prepareContextNode")
    graph.add_edge("prepareContextNode", "generateChatReplyNode")
    graph.add_edge("generateChatReplyNode", "persistContextNode")
    graph.add_edge("persistContextNode", END)
    return graph.compile()
