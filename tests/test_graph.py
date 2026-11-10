import pytest
from app.graph import graph as graph_module


@pytest.mark.asyncio
async def test_graph_retrieves_context_then_generates_answer(monkeypatch):
    async def retrieve(state):
        return {"retrieved_context": ["Reset instructions"]}

    async def generate(state):
        return {"answer": f"{state['query']}: {state['retrieved_context'][0]}"}

    monkeypatch.setattr(graph_module, "context_retrieval_node", retrieve)
    monkeypatch.setattr(graph_module, "generate_answer_node", generate)
    graph = graph_module.build_graph()

    result = await graph.ainvoke(
        {"query": "How do I reset?", "retrieved_context": [], "answer": ""}
    )

    assert result["answer"] == "How do I reset?: Reset instructions"
