import json

import motor.motor_asyncio
from app.config import settings
from app.graph.state import SupportBotState
from langchain_google_genai import ChatGoogleGenerativeAI

_mongo_client = None

_TREE_SEARCH_PROMPT = """
You are given a question and a tree structure of a support document.
Each node has a node_id, title, and summary. Find the nodes likely to contain
the answer. Reply only with JSON: {{"node_list": ["node_id"]}}.

Question: {query}

Document tree:
{tree_json}
"""


def get_mongo_database():
    global _mongo_client
    if _mongo_client is None:
        _mongo_client = motor.motor_asyncio.AsyncIOMotorClient(settings.MONGODB_URI)
    return _mongo_client[settings.MONGODB_DATABASE]


def close_mongo_client() -> None:
    global _mongo_client
    if _mongo_client is not None:
        _mongo_client.close()
        _mongo_client = None


def _build_node_map(tree: list[dict], node_map: dict[str, dict] | None = None) -> dict[str, dict]:
    if node_map is None:
        node_map = {}
    for node in tree:
        node_map[node["node_id"]] = node
        _build_node_map(node.get("nodes", []), node_map)
    return node_map


def _strip_text(tree: list[dict]) -> list[dict]:
    return [
        {
            **{key: value for key, value in node.items() if key != "text"},
            **({"nodes": _strip_text(node["nodes"])} if "nodes" in node else {}),
        }
        for node in tree
    ]


async def _search_tree(tree: list[dict], query: str) -> list[dict]:
    prompt = _TREE_SEARCH_PROMPT.format(
        query=query,
        tree_json=json.dumps(_strip_text(tree)),
    )
    llm = ChatGoogleGenerativeAI(
        model=settings.MODEL_NAME,
        google_api_key=settings.GOOGLE_API_KEY,
        temperature=0,
    )
    result = await llm.ainvoke(prompt)
    selected_ids = json.loads(result.content)["node_list"]
    node_map = _build_node_map(tree)
    return [node_map[node_id] for node_id in selected_ids if node_id in node_map]


async def context_retrieval_node(state: SupportBotState) -> dict:
    document = await get_mongo_database().document_trees.find_one(
        {"doc_id": settings.DOCUMENT_ID}
    )
    if document is None:
        raise RuntimeError(
            f"No indexed document '{settings.DOCUMENT_ID}' found. "
            "Run the document indexing command first."
        )

    nodes = await _search_tree(document["tree"], state["query"])
    return {
        "retrieved_context": [
            node["text"] for node in nodes if node.get("text")
        ]
    }
