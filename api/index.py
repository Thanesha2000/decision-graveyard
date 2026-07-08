import os
import sys

# Ensure the api/ directory is in path so local imports work
sys.path.insert(0, os.path.dirname(__file__))

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from mangum import Mangum

# Local module imports (copied alongside this file in api/)
from cognee_client import remember_decision, recall_decisions, forget_dataset
from llm_client import reason_about_relevance
from graph_store import add_decision, get_graph_data, find_matching_node_ids, get_dashboard_stats, remove_decision

app = FastAPI(title="Decision Graveyard API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---- Request/response schemas ----

class DecisionIn(BaseModel):
    title: str
    outcome: str
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

class RepeatCheckIn(BaseModel):
    description: str


# ---- Endpoints ----

@app.post("/api/ingest")
async def ingest_decision(decision: DecisionIn):
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


@app.post("/api/query")
async def query_decisions(query: QueryIn):
    try:
        results = await recall_decisions(query.question)
    except Exception as e:
        print(f"Fallback due to Cognee error: {e}")
        return {
            "answer": "This is the documented context/reasoning (Fallback - local database offline or unconfigured).",
            "raw": [],
            "matched_node_ids": []
        }

    if not results:
        return {"answer": "No relevant decisions found.", "raw": [], "matched_node_ids": []}

    answer_text = results[0]["text"]
    matched_ids = find_matching_node_ids(answer_text)
    return {"answer": answer_text, "raw": results, "matched_node_ids": matched_ids}


@app.post("/api/query/apply-today")
async def apply_today(payload: ApplyTodayIn):
    try:
        historical = await recall_decisions(payload.question)
    except Exception as e:
        historical = []

    if not historical:
        return {"verdict": "No historical decision found to evaluate. (Local DB Fallback)", "historical_context": None}

    historical_text = historical[0]["text"]

    try:
        verdict = reason_about_relevance(
            historical_context=historical_text,
            current_context=payload.current_context,
            question=payload.question,
        )
    except Exception as e:
        verdict = f"Failed to reason securely: {e}"

    return {"verdict": verdict, "historical_context": historical_text}


@app.post("/api/correct")
async def correct_decision(payload: CorrectionIn):
    return {
        "status": "correction applied (mocked locally)",
        "generalization_question": payload.generalization_question,
        "generalization_answer": "Mocked answer for local setup",
    }


@app.post("/api/alerts/repeat")
async def check_repeat(payload: RepeatCheckIn):
    search_question = f"Has a decision similar to this been made before: {payload.description}"

    try:
        results = await recall_decisions(search_question, top_k=1)
    except Exception as e:
        return {"warning": False, "message": f"Could not check for duplicates: {e}"}

    if not results:
        return {"warning": False, "message": "No similar past decision found."}

    return {
        "warning": True,
        "message": "A similar decision may already exist in the graveyard.",
        "matched_context": results[0]["text"],
    }


@app.get("/api/graph")
async def get_graph():
    return get_graph_data()


@app.get("/api/dashboard/stats")
async def dashboard_stats():
    return get_dashboard_stats()


@app.delete("/api/decisions/{decision_id}")
async def archive_decision(decision_id: str):
    remove_decision(decision_id)
    return {"status": "archived", "id": decision_id}


@app.get("/api/health")
async def health():
    return {"status": "ok"}

@app.get("/health")
async def health_no_api():
    return {"status": "ok_no_api"}

@app.get("/")
async def root():
    return {"status": "ok_root"}

# Vercel serverless handler
handler = Mangum(app, lifespan="off")
