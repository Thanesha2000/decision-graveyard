import asyncio
import os
import cognee
from dotenv import load_dotenv

load_dotenv()

async def main():
    # Connect
    cl = await cognee.serve(
        url=os.environ["COGNEE_SERVICE_URL"],
        api_key=os.environ["COGNEE_API_KEY"],
    )
    print("Connected to Cognee. Running cognify...")
    # call cognify
    try:
        await cl.cognify(datasets=["decision_graveyard_v2"])
        print("Cognify basic complete!")
    except Exception as e:
        print("Cognify failed:", e)
    
    # Try semantic recall to test
    try:
        result = await cl.recall(
            query_text="Why did we kill the mobile app project?",
            datasets=["decision_graveyard_v2"],
        )
        print("Recall result:", result)
    except Exception as e:
        print("Recall query failed:", e)
        
    await cognee.disconnect()

if __name__ == "__main__":
    if os.name == 'nt':
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    asyncio.run(main())
