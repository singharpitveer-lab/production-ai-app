from app.graph.state import SupportBotState


def test_state_contains_rag_workflow_fields():
    assert set(SupportBotState.__annotations__) == {
        "query",
        "retrieved_context",
        "answer",
    }
