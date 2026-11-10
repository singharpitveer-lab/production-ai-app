from pathlib import Path

from app.config import settings
from app.graph.state import SupportBotState
from langchain_google_genai import ChatGoogleGenerativeAI

_GENERATION_PROMPT = (
    Path(__file__).resolve().parents[3] / "prompts" / "generation.txt"
).read_text(encoding="utf-8")


async def generate_answer_node(state: SupportBotState) -> dict:
    context = "\n\n".join(state["retrieved_context"])
    prompt = _GENERATION_PROMPT.format(
        query=state["query"],
        context=context or "No relevant support documentation was found.",
        history="No conversation history.",
    )
    model = ChatGoogleGenerativeAI(
        model=settings.MODEL_NAME,
        google_api_key=settings.GOOGLE_API_KEY,
    )
    result = await model.ainvoke(prompt)
    return {"answer": result.content}
