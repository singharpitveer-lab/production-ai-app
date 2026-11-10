from app.graph.nodes.context_retrieval import _build_node_map, _strip_text


def test_build_node_map_includes_nested_nodes():
    tree = [
        {
            "node_id": "1",
            "text": "parent",
            "nodes": [{"node_id": "1.1", "text": "child"}],
        }
    ]

    assert set(_build_node_map(tree)) == {"1", "1.1"}


def test_strip_text_keeps_tree_structure_and_summaries():
    tree = [
        {
            "node_id": "1",
            "text": "long passage",
            "summary": "short summary",
            "nodes": [{"node_id": "1.1", "text": "nested passage"}],
        }
    ]

    assert _strip_text(tree) == [
        {
            "node_id": "1",
            "summary": "short summary",
            "nodes": [{"node_id": "1.1"}],
        }
    ]
