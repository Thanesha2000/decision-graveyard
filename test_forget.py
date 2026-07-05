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

    # Add a throwaway decision we'll archive
    await client.remember(
        "Decision: Killed the internal wiki redesign project\n"
        "Outcome: rejected\n"
        "Date: 2024-04-01\n"
        "People involved: Head of Ops\n"
        "Reasoning: Low usage of the existing wiki did not justify redesign investment.\n"
        "Tags: technical, low-priority",
        dataset_name=DATASET,
    )
    print("✅ Ingested throwaway decision")

    q_before = await client.recall(
        query_text="Why did we kill the wiki redesign project?",
        datasets=[DATASET],
    )
    print("\nBEFORE forget():")
    print(q_before[0]["text"] if q_before else "No result")

    # NOTE: forget() only supports dataset-level or data_id-level deletion,
    # not deleting a single fact within a dataset. For now we test dataset-level forget
    # on a THROWAWAY dataset so we don't lose real seed data.
    await client.remember(
        "Decision: Killed the internal wiki redesign project\n"
        "Outcome: rejected\nDate: 2024-04-01\nPeople involved: Head of Ops\n"
        "Reasoning: Low usage of the existing wiki did not justify redesign investment.\n"
        "Tags: technical, low-priority",
        dataset_name="throwaway_forget_test",
    )
    await client.forget(dataset="throwaway_forget_test")
    print("\n✅ forget() ran on throwaway_forget_test dataset")

    q_after = await client.recall(
        query_text="Why did we kill the wiki redesign project?",
        datasets=["throwaway_forget_test"],
    )
    print("\nAFTER forget() (querying the now-deleted dataset):")
    print(q_after[0]["text"] if q_after else "No result — dataset successfully forgotten")

    await cognee.disconnect()

asyncio.run(main())