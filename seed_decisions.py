import asyncio
import os
from dotenv import load_dotenv
import cognee

load_dotenv()

DATASET = "decision_graveyard_v2"

DECISIONS = [
    {
        "title": "Killed mobile app project",
        "outcome": "rejected",
        "date": "2024-03-15",
        "people": "CTO, Head of Product",
        "reasoning": "No engineering bandwidth to support both web and mobile simultaneously. Team was already stretched thin on the core platform rebuild.",
        "tags": "team, bandwidth"
    },
    {
        "title": "Paused Project Atlas",
        "outcome": "paused",
        "date": "2023-08-02",
        "people": "CFO, VP Engineering",
        "reasoning": "Budget too high relative to expected ROI in the first year. Estimated $400K spend with no clear revenue attribution model.",
        "tags": "budget, roi"
    },
    {
        "title": "Rejected pricing change to usage-based model",
        "outcome": "rejected",
        "date": "2024-01-10",
        "people": "Head of Sales, CEO",
        "reasoning": "Sales team objected strongly — usage-based pricing would complicate enterprise deals already in the pipeline and confuse existing customers mid-contract.",
        "tags": "pricing, sales"
    },
    {
        "title": "Pivoted from B2C to B2B focus",
        "outcome": "pivoted",
        "date": "2023-11-20",
        "people": "CEO, Head of Growth",
        "reasoning": "B2C acquisition costs were unsustainable — CAC exceeded LTV. B2B pilot showed 3x better unit economics.",
        "tags": "market, strategy"
    },
    {
        "title": "Approved migration to microservices",
        "outcome": "approved",
        "date": "2024-05-01",
        "people": "VP Engineering, Principal Engineer",
        "reasoning": "Monolith was blocking independent team deployment cadence. Approved despite short-term velocity hit because long-term scaling need was clear.",
        "tags": "technical, architecture"
    },
    {
        "title": "Rejected outsourcing QA to third party",
        "outcome": "rejected",
        "date": "2023-06-14",
        "people": "VP Engineering, Head of QA",
        "reasoning": "Quality concerns with prior outsourcing attempts in a different org. Preferred to hire in-house QA engineers instead.",
        "tags": "team, quality"
    },
    {
        "title": "Killed the AI chatbot support feature",
        "outcome": "rejected",
        "date": "2024-02-28",
        "people": "Head of Support, CTO",
        "reasoning": "Market not ready — customer research showed strong preference for human support for this product category. Technical feasibility was not the blocker.",
        "tags": "market, technical"
    },
    {
        "title": "Paused international expansion to EU",
        "outcome": "paused",
        "date": "2023-09-05",
        "people": "CEO, CFO, Head of Legal",
        "reasoning": "GDPR compliance costs and legal complexity were underestimated. Budget not allocated for dedicated compliance hire.",
        "tags": "budget, legal"
    },
]

async def main():
    print("[OK] Initializing local Cognee")

    for d in DECISIONS:
        text = (
            f"Decision: {d['title']}\n"
            f"Outcome: {d['outcome']}\n"
            f"Date: {d['date']}\n"
            f"People involved: {d['people']}\n"
            f"Reasoning: {d['reasoning']}\n"
            f"Tags: {d['tags']}"
        )
        await cognee.remember(text, dataset_name=DATASET)
        print(f"[OK] Ingested: {d['title']}")

    print("\n--- Running test queries ---\n")

    q1 = await cognee.recall(
        query_text="Why did we kill the mobile app project?",
        datasets=[DATASET],
    )
    print("Q1:", q1[0]["text"] if q1 else "No result")

    q2 = await cognee.recall(
        query_text="Who objected to the pricing change?",
        datasets=[DATASET],
    )
    print("\nQ2:", q2[0]["text"] if q2 else "No result")

    q3 = await cognee.recall(
        query_text="Have we tried anything like microservices migration before?",
        datasets=[DATASET],
    )
    print("\nQ3:", q3[0]["text"] if q3 else "No result")

if __name__ == "__main__":
    if os.name == 'nt':
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    asyncio.run(main())