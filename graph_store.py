
import json
import os
from pathlib import Path
from collections import Counter

STORE_FILE = Path("decisions_store.json")

STOPWORDS = {
    "project", "decision", "killed", "kill", "rejected", "reject",
    "paused", "pause", "approved", "approve", "pivoted", "pivot",
    "outcome", "team", "from", "with", "into", "that", "this",
}


def _load():
    if not STORE_FILE.exists():
        return []
    with open(STORE_FILE, "r") as f:
        return json.load(f)


def _save(decisions):
    with open(STORE_FILE, "w") as f:
        json.dump(decisions, f, indent=2)


def add_decision(title, outcome, people, tags):
    """Saves a small record locally, just enough to draw the graph."""
    decisions = _load()
    decisions.append({
        "id": str(len(decisions) + 1),
        "title": title,
        "outcome": outcome,
        "people": [p.strip() for p in people.split(",")],
        "tags": [t.strip() for t in tags.split(",")],
    })
    _save(decisions)


def get_graph_data():
    """Builds nodes and edges for the graph visualization."""
    decisions = _load()

    nodes = [
        {"id": d["id"], "label": d["title"], "outcome": d["outcome"]}
        for d in decisions
    ]

    edges = []
    for i, d1 in enumerate(decisions):
        for d2 in decisions[i + 1:]:
            shared_tags = set(d1["tags"]) & set(d2["tags"])
            shared_people = set(d1["people"]) & set(d2["people"])
            if shared_tags or shared_people:
                reason = ", ".join(shared_tags | shared_people)
                edges.append({"from": d1["id"], "to": d2["id"], "label": reason})

    return {"nodes": nodes, "edges": edges}


def find_matching_node_ids(text):
    """
    Given a text (like an answer from Cognee), find which decision(s)
    it's actually about - using only distinctive (non-generic) words,
    and only returning the strongest match(es), not loose partial hits.
    """
    decisions = _load()
    text_lower = text.lower()

    scored = []
    for d in decisions:
        words = [w.lower().strip(".,!?") for w in d["title"].split()]
        meaningful_words = [w for w in words if len(w) > 3 and w not in STOPWORDS]
        if not meaningful_words:
            continue
        hits = sum(1 for w in meaningful_words if w in text_lower)
        ratio = hits / len(meaningful_words)
        if hits > 0:
            scored.append((d["id"], hits, ratio))

    if not scored:
        return []

    strong_matches = [s for s in scored if s[2] >= 0.6]

    if not strong_matches:
        return []

    return [s[0] for s in strong_matches]


def get_dashboard_stats():
    """Summary counts for the dashboard: totals, outcome breakdown, top tags/people."""
    decisions = _load()

    outcome_counts = Counter(d["outcome"] for d in decisions)

    all_tags = [tag for d in decisions for tag in d["tags"]]
    tag_counts = Counter(all_tags).most_common(5)

    all_people = [person for d in decisions for person in d["people"]]
    people_counts = Counter(all_people).most_common(5)

    return {
        "total_decisions": len(decisions),
        "by_outcome": dict(outcome_counts),
        "top_tags": [{"tag": t, "count": c} for t, c in tag_counts],
        "top_people": [{"person": p, "count": c} for p, c in people_counts],
        "timeline": [
            {"id": d["id"], "title": d["title"], "outcome": d["outcome"]}
            for d in decisions
        ],
    }
def remove_decision(decision_id):
    """Soft-deletes a decision from the local graph store (archive)."""
    decisions = _load()
    decisions = [d for d in decisions if d["id"] != decision_id]
    _save(decisions)