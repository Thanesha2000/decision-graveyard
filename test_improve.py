import asyncio, os
from dotenv import load_dotenv
import cognee

load_dotenv()

DATASET = "decision_graveyard"

async def main():
    client = await cognee.serve(
        url=os.environ["COGNEE_SERVICE_URL"],
        api_key=os.environ["COGNEE_API_KEY"],
    )
    print("✅ Connected to Cognee Cloud")

    q_before = await client.recall(
        query_text="Was Project Atlas paused permanently or could it be revisited?",
        datasets=[DATASET],
    )
    print("BEFORE correction:")
    print(q_before[0]["text"] if q_before else "No result")

    await client.remember(
        "Correction regarding Project Atlas: the pause was explicitly NOT permanent. "
        "The CFO stated in the original decision meeting that Project Atlas should be "
        "revisited if the company secures $1M or more in additional funding, since that "
        "would resolve the original ROI attribution concern.",
        dataset_name=DATASET,
    )
    print("\n✅ Correction remembered (no separate improve() call)")

    q_after = await client.recall(
        query_text="Was Project Atlas paused permanently or could it be revisited?",
        datasets=[DATASET],
    )
    print("\nAFTER correction (same question):")
    print(q_after[0]["text"] if q_after else "No result")

    q_related = await client.recall(
        query_text="Under what conditions would Project Atlas be reconsidered?",
        datasets=[DATASET],
    )
    print("\nGENERALIZATION TEST (different question):")
    print(q_related[0]["text"] if q_related else "No result")

    await cognee.disconnect()

asyncio.run(main())