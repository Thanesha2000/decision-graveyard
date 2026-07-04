# Decision Graveyard

> Every abandoned idea deserves a memory.

Organizations repeatedly make the same mistakes because the reasoning behind 
past decisions was never preserved. Decision Graveyard fixes this — a 
graph-native institutional memory that stores not just outcomes but objections, 
tradeoffs, and reasoning chains, and answers whether history is about to repeat itself.

## Cognee Memory Lifecycle APIs Used

| API | How it's used |
|---|---|
| `remember()` | Every decision log entry ingested into Cognee's knowledge graph |
| `recall()` | Natural language queries traverse the graph to retrieve reasoning chains |
| `improve()` | Corrections fed back in via /correct endpoint, generalization tested automatically |
| `forget()` | Archive a decision — pruned from active graph, future queries no longer pull it |

## Features

- Decision graph visualization — nodes colored by outcome (rejected/paused/pivoted/approved)
- Natural language query — "Why did we kill Project X?" answered from graph traversal
- "Would it still apply today?" — historical objection cross-referenced against current context
- Repeat alert — warns when a new decision matches a past one automatically
- Archive — formally retire a decision, graph updates live
- Dashboard — counts, top objection tags, most active decision-makers, timeline

## Tech Stack

- **Backend:** Python, FastAPI, Cognee
- **Frontend:** React (Vite), react-force-graph-2d, Tailwind CSS
- **LLM:** Groq (llama-3.3-70b-versatile)
- **Memory Layer:** Cognee (graph-vector hybrid retrieval)

## Setup

### Backend
```bash
cd decision-graveyard
python -m venv .venv
.venv\Scripts\activate
pip install cognee fastapi uvicorn groq python-dotenv
```

Create `.env`:
```
LLM_API_KEY=your_groq_key
GROQ_API_KEY=your_groq_key
LLM_PROVIDER=openai
LLM_MODEL=groq/llama-3.3-70b-versatile
LLM_ENDPOINT=https://api.groq.com/openai/v1
EMBEDDING_PROVIDER=openai
EMBEDDING_MODEL=text-embedding-ada-002
EMBEDDING_ENDPOINT=https://generativelanguage.googleapis.com/v1beta/openai/
GEMINI_API_KEY=your_gemini_key
ENABLE_BACKEND_ACCESS_CONTROL=false
```

```bash
uvicorn main:app --reload
```

### Frontend
```bash
cd decision-graveyard-frontend
npm install
npm run dev
```

## AI Disclosure

Built with assistance from Claude (Anthropic) for code generation and debugging. 
All architecture decisions, feature design, and system design were made by the developer.

## Demo

1. Add decisions via the form
2. Ask "Why did we kill X?" in Query
3. Toggle "Would it apply today?" with current context
4. Click any node to see full reasoning + archive it
5. Check Dashboard for patterns across all decisions