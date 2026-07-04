import { useState } from "react";
import axios from "axios";

function QueryView({ onAnswer }) {
  const [question, setQuestion] = useState("");
  const [answer, setAnswer] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const [applyTodayMode, setApplyTodayMode] = useState(false);
  const [currentContext, setCurrentContext] = useState("");

  const handleAsk = async () => {
    if (!question.trim()) return;
    setLoading(true);
    setError(null);
    setAnswer("");

    try {
      if (applyTodayMode) {
        const res = await axios.post(
          "http://127.0.0.1:8000/query/apply-today",
          {
            question,
            current_context: currentContext,
          },
        );
        setAnswer(res.data.verdict);
      } else {
        const res = await axios.post("http://127.0.0.1:8000/query", {
          question,
        });
        setAnswer(res.data.answer);
        if (onAnswer) onAnswer(res.data.matched_node_ids || []);
      }
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="max-w-2xl">
      <div className="flex items-center gap-2 mb-4">
        <input
          type="checkbox"
          id="applyToday"
          checked={applyTodayMode}
          onChange={(e) => setApplyTodayMode(e.target.checked)}
        />
        <label htmlFor="applyToday" className="text-sm text-neutral-400">
          Would it still apply today?
        </label>
      </div>

      <textarea
        value={question}
        onChange={(e) => setQuestion(e.target.value)}
        placeholder="Ask a question about past decisions..."
        className="w-full bg-neutral-900 border border-neutral-800 rounded p-3 text-white mb-3"
        rows={3}
      />

      {applyTodayMode && (
        <textarea
          value={currentContext}
          onChange={(e) => setCurrentContext(e.target.value)}
          placeholder="What's the current context? (e.g. 'we now have $2M in funding')"
          className="w-full bg-neutral-900 border border-neutral-800 rounded p-3 text-white mb-3"
          rows={2}
        />
      )}

      <button
        onClick={handleAsk}
        disabled={loading}
        className="bg-white text-black font-medium px-4 py-2 rounded hover:bg-neutral-200 disabled:opacity-50"
      >
        {loading ? "Thinking..." : "Ask"}
      </button>

      {error && <p className="text-red-500 mt-4">Error: {error}</p>}

      {answer && (
        <div className="mt-6 bg-neutral-950 border border-neutral-800 rounded p-4 whitespace-pre-wrap text-neutral-200">
          {answer}
        </div>
      )}
    </div>
  );
}

export default QueryView;
