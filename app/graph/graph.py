from app.graph.nodes.context_retrieval import context_retrieval_node
from app.graph.nodes.execution import generate_answer_node
from app.graph.state import SupportBotState
from langgraph.graph import END, START, StateGraph


def build_graph():
    graph = StateGraph(SupportBotState)
    graph.add_node("retrieve_context", context_retrieval_node)
    graph.add_node("generate_answer", generate_answer_node)
    graph.add_edge(START, "retrieve_context")
    graph.add_edge("retrieve_context", "generate_answer")
    graph.add_edge("generate_answer", END)
    return graph.compile()
