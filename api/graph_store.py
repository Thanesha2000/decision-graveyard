import json
import os
import shutil
from pathlib import Path
from collections import Counter

# On Vercel, the deployed filesystem is read-only.
# We use /tmp for mutable state (ephemeral per cold start).
# The seed file lives alongside this module, bundled at deploy time.

SEED_FILE = Path(os.path.dirname(__file__)) / "decisions_store.json"
TMP_STORE = Path("/tmp") / "decisions_store.json"

STOPWORDS = {
    "project", "decision", "killed", "kill", "rejected", "reject",
    "paused", "pause", "approved", "approve", "pivoted", "pivot",
    "outcome", "team", "from", "with", "into", "that", "this",
}


def _load():
    # On first call per cold start: copy seed into /tmp if not already there
    if not TMP_STORE.exists():
        if SEED_FILE.exists():
            shutil.copy(SEED_FILE, TMP_STORE)
        else:
            TMP_STORE.write_text("[]")
    with open(TMP_STORE, "r") as f:
        return json.load(f)


def _save(decisions):
    with open(TMP_STORE, "w") as f:
        json.dump(decisions, f, indent=2)


def add_decision(title, outcome, people, tags):
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
    decisions = _load()
    decisions = [d for d in decisions if d["id"] != decision_id]
    _save(decisions)
