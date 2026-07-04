import asyncio
from cognee_client import remember_decision, recall_decisions, disconnect_client

async def main():
    result = await recall_decisions("Why did we kill the mobile app project?")
    print(result[0]["text"] if result else "No result")
    await disconnect_client()

asyncio.run(main())