import os
import httpx
from dotenv import load_dotenv

load_dotenv()

DATASET = "decision_graveyard_v2"

COGNEE_SERVICE_URL = os.environ.get("COGNEE_SERVICE_URL", "")
COGNEE_API_KEY = os.environ.get("COGNEE_API_KEY", "")


def _headers():
    return {
        "X-API-KEY": COGNEE_API_KEY,
        "Content-Type": "application/json",
    }


async def remember_decision(text: str, dataset: str = DATASET) -> dict:
    """Ingest text into Cognee cloud via REST API."""
    async with httpx.AsyncClient(timeout=30.0) as client:
        # Step 1: add data
        add_resp = await client.post(
            f"{COGNEE_SERVICE_URL}/api/v1/add",
            headers=_headers(),
            json={"data": text, "dataset_name": dataset},
        )
        add_resp.raise_for_status()

        # Step 2: cognify (build the knowledge graph)
        cognify_resp = await client.post(
            f"{COGNEE_SERVICE_URL}/api/v1/cognify",
            headers=_headers(),
            json={"datasets": [dataset]},
        )
        cognify_resp.raise_for_status()

        return {"add": add_resp.json(), "cognify": cognify_resp.json()}


async def recall_decisions(query: str, dataset: str = DATASET, top_k: int = 10) -> list:
    """Search Cognee cloud via REST API."""
    async with httpx.AsyncClient(timeout=30.0) as client:
        resp = await client.post(
            f"{COGNEE_SERVICE_URL}/api/v1/search",
            headers=_headers(),
            json={
                "query": query,
                "datasets": [dataset],
                "top_k": top_k,
            },
        )
        resp.raise_for_status()
        data = resp.json()

        # Cognee returns: [{"dataset_id": "...", "search_result": ["text1", "text2"]}]
        results = []
        if isinstance(data, list):
            for item in data:
                if isinstance(item, dict) and "search_result" in item:
                    for text in item["search_result"]:
                        results.append({"text": text if isinstance(text, str) else str(text)})
                elif isinstance(item, str):
                    results.append({"text": item})
        elif isinstance(data, dict) and "search_result" in data:
            for text in data["search_result"]:
                results.append({"text": text if isinstance(text, str) else str(text)})
        return results


async def forget_dataset(dataset: str = DATASET) -> dict:
    """Delete a dataset from Cognee cloud."""
    async with httpx.AsyncClient(timeout=30.0) as client:
        resp = await client.delete(
            f"{COGNEE_SERVICE_URL}/api/v1/datasets/{dataset}",
            headers=_headers(),
        )
        resp.raise_for_status()
        return resp.json()