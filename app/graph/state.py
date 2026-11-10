from typing import TypedDict


class SupportBotState(TypedDict):
    query: str
    retrieved_context: list[str]
    answer: str
