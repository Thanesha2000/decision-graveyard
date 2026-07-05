
import asyncio
import httpx

DECISIONS = [
    {"title": "Killed mobile app project", "outcome": "rejected", "date": "2024-03-15",
     "people": "CTO, Head of Product",
     "reasoning": "No engineering bandwidth to support both web and mobile simultaneously. Team was already stretched thin on the core platform rebuild.",
     "tags": "team, bandwidth"},
    {"title": "Paused Project Atlas", "outcome": "paused", "date": "2023-08-02",
     "people": "CFO, VP Engineering",
     "reasoning": "Budget too high relative to expected ROI in the first year. Estimated $400K spend with no clear revenue attribution model.",
     "tags": "budget, roi"},
    {"title": "Rejected pricing change to usage-based model", "outcome": "rejected", "date": "2024-01-10",
     "people": "Head of Sales, CEO",
     "reasoning": "Sales team objected strongly - usage-based pricing would complicate enterprise deals already in the pipeline and confuse existing customers mid-contract.",
     "tags": "pricing, sales"},
    {"title": "Pivoted from B2C to B2B focus", "outcome": "pivoted", "date": "2023-11-20",
     "people": "CEO, Head of Growth",
     "reasoning": "B2C acquisition costs were unsustainable - CAC exceeded LTV. B2B pilot showed 3x better unit economics.",
     "tags": "market, strategy"},
    {"title": "Approved migration to microservices", "outcome": "approved", "date": "2024-05-01",
     "people": "VP Engineering, Principal Engineer",
     "reasoning": "Monolith was blocking independent team deployment cadence. Approved despite short-term velocity hit because long-term scaling need was clear.",
     "tags": "technical, architecture"},
    {"title": "Rejected outsourcing QA to third party", "outcome": "rejected", "date": "2023-06-14",
     "people": "VP Engineering, Head of QA",
     "reasoning": "Quality concerns with prior outsourcing attempts in a different org. Preferred to hire in-house QA engineers instead.",
     "tags": "team, quality"},
    {"title": "Killed the AI chatbot support feature", "outcome": "rejected", "date": "2024-02-28",
     "people": "Head of Support, CTO",
     "reasoning": "Market not ready - customer research showed strong preference for human support for this product category. Technical feasibility was not the blocker.",
     "tags": "market, technical"},
    {"title": "Paused international expansion to EU", "outcome": "paused", "date": "2023-09-05",
     "people": "CEO, CFO, Head of Legal",
     "reasoning": "GDPR compliance costs and legal complexity were underestimated. Budget not allocated for dedicated compliance hire.",
     "tags": "budget, legal"},
]

async def main():
    async with httpx.AsyncClient(timeout=60) as client:
        for d in DECISIONS:
            resp = await client.post("http://127.0.0.1:8000/ingest", json=d)
            print(d["title"], "->", resp.status_code)

asyncio.run(main())
