import logging
import uuid
from contextlib import asynccontextmanager

from app.config import settings
from app.graph.graph import build_graph
from app.graph.nodes.context_retrieval import close_mongo_client, get_mongo_database
from fastapi import FastAPI, HTTPException, Request
from pydantic import BaseModel, Field

logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    try:
        await get_mongo_database().command("ping")
        app.state.graph = build_graph()
        yield
    finally:
        close_mongo_client()


app = FastAPI(title="Support Bot API", lifespan=lifespan)


class QueryRequest(BaseModel):
    query: str = Field(min_length=1)


class QueryResponse(BaseModel):
    answer: str
    request_id: str


@app.post("/query", response_model=QueryResponse)
async def query_endpoint(body: QueryRequest, request: Request):
    if not body.query.strip():
        raise HTTPException(status_code=400, detail="Query cannot be empty")

    request_id = str(uuid.uuid4())
    if len(body.query) > settings.MAX_INPUT_CHARS:
        raise HTTPException(
            status_code=400,
            detail=f"Query cannot exceed {settings.MAX_INPUT_CHARS} characters",
        )

    try:
        result = await request.app.state.graph.ainvoke(
            {"query": body.query, "retrieved_context": [], "answer": ""}
        )
    except Exception as exc:
        logger.exception("Query processing failed (request_id=%s)", request_id)
        raise HTTPException(
            status_code=503,
            detail="Unable to process the query. Check the API, model, and indexed documents.",
        ) from exc

    return QueryResponse(answer=result["answer"], request_id=request_id)


@app.get("/health")
async def health():
    return {"status": "ok"}
