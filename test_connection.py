import asyncio
import os
from dotenv import load_dotenv
import cognee

load_dotenv()

async def main():
    client = await cognee.serve(
        url=os.environ["COGNEE_SERVICE_URL"],
        api_key=os.environ["COGNEE_API_KEY"],
    )
    print("✅ Connected to Cognee Cloud")

    # Quick smoke test
    await client.remember(
        "Decision Graveyard connection test successful.",
        dataset_name="connection_test",
    )
    print("✅ remember() worked")

    results = await client.recall(query_text="What was the connection test?")
    print("✅ recall() worked. Result:")
    for r in results:
        print(r)

    await cognee.disconnect()

asyncio.run(main())