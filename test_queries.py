import asyncio
import os
from dotenv import load_dotenv
import cognee

load_dotenv()

async def main():
    cl = await cognee.serve(
        url=os.environ["COGNEE_SERVICE_URL"],
        api_key=os.environ["COGNEE_API_KEY"],
    )
    queries = [
        "Killed mobile app project",
        "Why did we make the decision: Killed mobile app project",
        "Reasoning behind Killed mobile app project",
        "Why did we kill the mobile app project?"
    ]
    for q in queries:
        res = await cl.recall(query_text=q, datasets=["decision_graveyard_v2"])
        print(f"QUERY: {q}")
        print("ANSWER:", res[0]["text"] if res else "None")
        print("-" * 40)
    await cognee.disconnect()

if __name__ == "__main__":
    if os.name == 'nt':
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    asyncio.run(main())
