import os
from dotenv import load_dotenv
import cognee

load_dotenv()

DATASET = "decision_graveyard_v2"

_client = None

async def get_client():
    """Returns a connected Cognee Cloud client, connecting once and reusing it."""
    global _client
    if _client is None:
        _client = await cognee.serve(
            url=os.environ["COGNEE_SERVICE_URL"],
            api_key=os.environ["COGNEE_API_KEY"],
        )
    return _client


async def remember_decision(text: str, dataset: str = DATASET) -> dict:
    client = await get_client()
    return await client.remember(text, dataset_name=dataset)


async def recall_decisions(query: str, dataset: str = DATASET, top_k: int = 10) -> list:
    client = await get_client()
    return await client.recall(
        query_text=query,
        datasets=[dataset],
        top_k=top_k,
    )


async def forget_dataset(dataset: str = DATASET) -> dict:
    client = await get_client()
    return await client.forget(dataset=dataset)


async def disconnect_client():
    global _client
    if _client is not None:
        await cognee.disconnect()
        _client = None