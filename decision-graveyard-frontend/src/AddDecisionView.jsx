import { useState, useEffect, useRef } from "react";
import axios from "axios";

const API_URL = import.meta.env.VITE_API_URL || "http://127.0.0.1:8000";

const OUTCOMES = ["rejected", "paused", "pivoted", "approved"];

function AddDecisionView() {
  const [form, setForm] = useState({
    title: "",
    outcome: "rejected",
    date: "",
    people: "",
    reasoning: "",
    tags: "",
  });
  const [submitting, setSubmitting] = useState(false);
  const [successMsg, setSuccessMsg] = useState("");
  const [errorMsg, setErrorMsg] = useState("");

  const [repeatWarning, setRepeatWarning] = useState(null);
  const debounceTimer = useRef(null);

  const handleChange = (field) => (e) => {
    setForm({ ...form, [field]: e.target.value });
  };

  useEffect(() => {
    const titleReady = form.title.trim().length >= 10;
    const reasoningReady = form.reasoning.trim().length >= 10;

    // Need at least a meaningful title to check for duplicates
    if (!titleReady) {
      setRepeatWarning(null);
      return;
    }

    if (debounceTimer.current) clearTimeout(debounceTimer.current);

    debounceTimer.current = setTimeout(() => {
      const description = reasoningReady
        ? form.title + ". " + form.reasoning
        : form.title;

      axios
        .post(API_URL + "/alerts/repeat", { description })
        .then((res) => {
          if (res.data.warning) {
            setRepeatWarning(res.data.matched_context);
          } else {
            setRepeatWarning(null);
          }
        })
        .catch(() => setRepeatWarning(null));
    }, 800);

    return () => clearTimeout(debounceTimer.current);
  }, [form.reasoning, form.title]);

  const handleSubmit = async () => {
    setSubmitting(true);
    setSuccessMsg("");
    setErrorMsg("");
    try {
      await axios.post(API_URL + "/ingest", form);
      setSuccessMsg('"' + form.title + '" added to the graveyard.');
      setForm({
        title: "",
        outcome: "rejected",
        date: "",
        people: "",
        reasoning: "",
        tags: "",
      });
      setRepeatWarning(null);
    } catch (err) {
      setErrorMsg(err.message);
    } finally {
      setSubmitting(false);
    }
  };

  const isValid =
    form.title && form.date && form.people && form.reasoning && form.tags;

  return (
    <div className="max-w-xl">
      {repeatWarning && (
        <div className="bg-amber-950 border border-amber-700 text-amber-200 rounded p-3 mb-4 text-sm">
          <strong>⚠ Warning:</strong> A similar decision may already exist.
          <p className="mt-1 text-amber-300">{repeatWarning}</p>
        </div>
      )}

      <label className="block text-sm text-neutral-400 mb-1">Title</label>
      <input
        value={form.title}
        onChange={handleChange("title")}
        className="w-full bg-neutral-900 border border-neutral-800 rounded p-2 mb-3 text-white"
        placeholder="e.g. Killed the Q3 rebrand initiative"
      />

      <label className="block text-sm text-neutral-400 mb-1">Outcome</label>
      <select
        value={form.outcome}
        onChange={handleChange("outcome")}
        className="w-full bg-neutral-900 border border-neutral-800 rounded p-2 mb-3 text-white"
      >
        {OUTCOMES.map((o) => (
          <option key={o} value={o}>
            {o}
          </option>
        ))}
      </select>

      <label className="block text-sm text-neutral-400 mb-1">Date</label>
      <input
        type="date"
        value={form.date}
        onChange={handleChange("date")}
        className="w-full bg-neutral-900 border border-neutral-800 rounded p-2 mb-3 text-white"
      />

      <label className="block text-sm text-neutral-400 mb-1">
        People involved (comma-separated)
      </label>
      <input
        value={form.people}
        onChange={handleChange("people")}
        className="w-full bg-neutral-900 border border-neutral-800 rounded p-2 mb-3 text-white"
        placeholder="e.g. CTO, Head of Product"
      />

      <label className="block text-sm text-neutral-400 mb-1">Reasoning</label>
      <textarea
        value={form.reasoning}
        onChange={handleChange("reasoning")}
        rows={4}
        className="w-full bg-neutral-900 border border-neutral-800 rounded p-2 mb-3 text-white"
        placeholder="Why was this decision made?"
      />

      <label className="block text-sm text-neutral-400 mb-1">
        Tags (comma-separated)
      </label>
      <input
        value={form.tags}
        onChange={handleChange("tags")}
        className="w-full bg-neutral-900 border border-neutral-800 rounded p-2 mb-4 text-white"
        placeholder="e.g. budget, technical"
      />

      <button
        onClick={handleSubmit}
        disabled={!isValid || submitting}
        className="bg-white text-black font-medium px-4 py-2 rounded hover:bg-neutral-200 disabled:opacity-50"
      >
        {submitting ? "Adding..." : "Add Decision"}
      </button>

      {successMsg && <p className="text-green-400 mt-4">{successMsg}</p>}
      {errorMsg && <p className="text-red-500 mt-4">Error: {errorMsg}</p>}
    </div>
  );
}

export default AddDecisionView;
