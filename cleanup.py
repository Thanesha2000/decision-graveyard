import asyncio, os
from dotenv import load_dotenv
import cognee

load_dotenv()

async def main():
    client = await cognee.serve(
        url=os.environ["COGNEE_SERVICE_URL"],
        api_key=os.environ["COGNEE_API_KEY"],
    )
    await client.forget(dataset="connection_test")
    print("✅ Forgot connection_test")
    await client.forget(dataset="default_dataset")
    print("✅ Forgot default_dataset")
    await cognee.disconnect()

asyncio.run(main())