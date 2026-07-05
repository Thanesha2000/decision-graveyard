from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from cognee_client import remember_decision, recall_decisions, forget_dataset
from llm_client import reason_about_relevance


from graph_store import add_decision, get_graph_data, find_matching_node_ids, get_dashboard_stats, remove_decision

app = FastAPI(title="Decision Graveyard API")
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "https://decision-graveyard-ruddy.vercel.app",
    ],
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---- Request/response schemas ----

class DecisionIn(BaseModel):
    title: str
    outcome: str          # rejected / paused / pivoted / approved
    date: str
    people: str
    reasoning: str
    tags: str

class QueryIn(BaseModel):
    question: str

class ApplyTodayIn(BaseModel):
    question: str
    current_context: str

class CorrectionIn(BaseModel):
    correction_text: str
    generalization_question: str


# ---- Endpoints ----

@app.post("/ingest")
async def ingest_decision(decision: DecisionIn):
    """Turns a structured decision into text and stores it via remember(),
    and also saves a small local copy for the graph visualization."""
    text = (
        f"Decision: {decision.title}\n"
        f"Outcome: {decision.outcome}\n"
        f"Date: {decision.date}\n"
        f"People involved: {decision.people}\n"
        f"Reasoning: {decision.reasoning}\n"
        f"Tags: {decision.tags}"
    )
    try:
        result = await remember_decision(text)
    except Exception as e:
        raise HTTPException(status_code=502, detail=f"Cognee error: {e}")

    add_decision(decision.title, decision.outcome, decision.people, decision.tags)

    return {"status": "ingested", "title": decision.title, "cognee_result": result}


@app.post("/query")
async def query_decisions(query: QueryIn):
    """Natural-language question against the decision graph."""
    try:
        results = await recall_decisions(query.question)
    except Exception as e:
        raise HTTPException(status_code=502, detail=f"Cognee error: {e}")
    if not results:
        return {"answer": "No relevant decisions found.", "raw": [], "matched_node_ids": []}

    answer_text = results[0]["text"]
    matched_ids = find_matching_node_ids(answer_text)

    return {"answer": answer_text, "raw": results, "matched_node_ids": matched_ids}


@app.post("/query/apply-today")
async def apply_today(payload: ApplyTodayIn):
    """
    Step 1: recall() the historical reasoning behind the objection.
    Step 2: ask the LLM whether that reasoning still holds given current_context.
    """
    try:
        historical = await recall_decisions(payload.question)
    except Exception as e:
        raise HTTPException(status_code=502, detail=f"Cognee error: {e}")

    if not historical:
        return {"verdict": "No historical decision found to evaluate.", "historical_context": None}

    historical_text = historical[0]["text"]

    try:
        verdict = reason_about_relevance(
            historical_context=historical_text,
            current_context=payload.current_context,
            question=payload.question,
        )
    except Exception as e:
        raise HTTPException(status_code=502, detail=f"LLM error: {e}")

    return {
        "verdict": verdict,
        "historical_context": historical_text,
    }


@app.post("/correct")
async def correct_decision(payload: CorrectionIn):
    """
    Feeds a correction into the graph via remember(), then immediately
    re-queries with a related-but-different question to prove it generalized.
    """
    try:
        await remember_decision(payload.correction_text)
    except Exception as e:
        raise HTTPException(status_code=502, detail=f"Cognee error on correction: {e}")

    try:
        generalization_result = await recall_decisions(payload.generalization_question)
    except Exception as e:
        raise HTTPException(status_code=502, detail=f"Cognee error on generalization check: {e}")

    return {
        "status": "correction applied",
        "generalization_question": payload.generalization_question,
        "generalization_answer": generalization_result[0]["text"] if generalization_result else "No result",
    }
class RepeatCheckIn(BaseModel):
    description: str   # a draft description of the new decision being considered

@app.post("/alerts/repeat")
async def check_repeat(payload: RepeatCheckIn):
    """
    Checks if a similar decision already exists in the graveyard.
    """
    search_question = f"Has a decision similar to this been made before: {payload.description}"

    try:
        results = await recall_decisions(search_question, top_k=1)
    except Exception as e:
        raise HTTPException(status_code=502, detail=f"Cognee error: {e}")

    if not results:
        return {"warning": False, "message": "No similar past decision found."}

    return {
        "warning": True,
        "message": "A similar decision may already exist in the graveyard.",
        "matched_context": results[0]["text"],
    }

@app.get("/graph")
async def get_graph():
    """Returns nodes and edges for the frontend's graph visualization."""
    return get_graph_data()

@app.get("/dashboard/stats")
async def dashboard_stats():
    """Returns summary stats for the dashboard."""
    return get_dashboard_stats()
@app.delete("/decisions/{decision_id}")
async def archive_decision(decision_id: str):
    remove_decision(decision_id)
    return {"status": "archived", "id": decision_id}
@app.get("/health")
async def health():
    return {"status": "ok"}