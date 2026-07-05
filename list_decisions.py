import asyncio, os, json
from dotenv import load_dotenv
import cognee

load_dotenv()

async def main():
    client = await cognee.serve(
        url=os.environ["COGNEE_SERVICE_URL"],
        api_key=os.environ["COGNEE_API_KEY"],
    )
    result = await client.recall(
        query_text="List every decision in the graveyard with its title and outcome.",
        datasets=["decision_graveyard_v2"],
        top_k=20,
    )
    print(result[0]["text"] if result else "No result")
    await cognee.disconnect()

asyncio.run(main())