import asyncio
import os
import json
from dotenv import load_dotenv
import cognee

load_dotenv()

async def main():
    cl = await cognee.serve(
        url=os.environ["COGNEE_SERVICE_URL"],
        api_key=os.environ["COGNEE_API_KEY"],
    )
    res = await cl.recall(
        query_text="Why did we kill the mobile app project?",
        datasets=["decision_graveyard_v2"],
    )
    with open("res.json", "w", encoding="utf-8") as f:
        json.dump(res, f, indent=2)
    print("Test recall complete! Results written to res.json.")
    await cognee.disconnect()

if __name__ == "__main__":
    if os.name == 'nt':
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    asyncio.run(main())
