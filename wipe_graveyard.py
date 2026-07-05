import asyncio, os
from dotenv import load_dotenv
import cognee

load_dotenv()

async def main():
    client = await cognee.serve(
        url=os.environ["COGNEE_SERVICE_URL"],
        api_key=os.environ["COGNEE_API_KEY"],
    )
    await client.forget(dataset="decision_graveyard")
    print("Wiped decision_graveyard clean")
    await cognee.disconnect()

asyncio.run(main())
