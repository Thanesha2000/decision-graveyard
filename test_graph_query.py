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
        query_text="MATCH (n)-[r]->(m) RETURN n, r, m LIMIT 50",
        datasets=["decision_graveyard_v2"],
        query_type="CYPHER",
    )
    print(json.dumps(result, indent=2, default=str)[:4000])
    await cognee.disconnect()

asyncio.run(main())
