import { useEffect, useState } from "react";
import axios from "axios";

const API_URL = import.meta.env.VITE_API_URL || "http://127.0.0.1:8000";

const OUTCOME_COLORS = {
  rejected: "#ef4444",
  paused: "#eab308",
  pivoted: "#3b82f6",
  approved: "#22c55e",
};

function DashboardView() {
  const [stats, setStats] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    axios
      .get(API_URL + "/dashboard/stats")
      .then((res) => {
        setStats(res.data);
        setLoading(false);
      })
      .catch((err) => {
        setError(err.message);
        setLoading(false);
      });
  }, []);

  if (loading) return <p className="text-neutral-500">Loading dashboard...</p>;
  if (error)
    return <p className="text-red-500">Failed to load dashboard: {error}</p>;

  return (
    <div className="max-w-3xl">
      <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mb-8">
        <div className="bg-neutral-950 border border-neutral-800 rounded p-4">
          <p className="text-neutral-500 text-sm mb-1">Total Decisions</p>
          <p className="text-3xl font-bold">{stats.total_decisions}</p>
        </div>
        {Object.entries(stats.by_outcome).map(([outcome, count]) => (
          <div
            key={outcome}
            className="bg-neutral-950 border border-neutral-800 rounded p-4"
          >
            <p className="text-neutral-500 text-sm mb-1 capitalize">
              {outcome}
            </p>
            <p
              className="text-3xl font-bold"
              style={{ color: OUTCOME_COLORS[outcome] }}
            >
              {count}
            </p>
          </div>
        ))}
      </div>

      <div className="grid grid-cols-2 gap-6 mb-8">
        <div>
          <h3 className="text-lg font-semibold mb-3">Top Objection Tags</h3>
          <div className="flex flex-col gap-2">
            {stats.top_tags.map((t) => (
              <div
                key={t.tag}
                className="flex justify-between bg-neutral-950 border border-neutral-800 rounded px-3 py-2"
              >
                <span className="text-neutral-300">{t.tag}</span>
                <span className="text-neutral-500">{t.count}</span>
              </div>
            ))}
          </div>
        </div>
        <div>
          <h3 className="text-lg font-semibold mb-3">
            Most Active Decision-Makers
          </h3>
          <div className="flex flex-col gap-2">
            {stats.top_people.map((p) => (
              <div
                key={p.person}
                className="flex justify-between bg-neutral-950 border border-neutral-800 rounded px-3 py-2"
              >
                <span className="text-neutral-300">{p.person}</span>
                <span className="text-neutral-500">{p.count}</span>
              </div>
            ))}
          </div>
        </div>
      </div>

      <div>
        <h3 className="text-lg font-semibold mb-3">Timeline</h3>
        <div className="flex flex-col gap-2">
          {stats.timeline.map((d) => (
            <div
              key={d.id}
              className="flex items-center gap-3 bg-neutral-950 border border-neutral-800 rounded px-3 py-2"
            >
              <span
                className="w-2 h-2 rounded-full"
                style={{ backgroundColor: OUTCOME_COLORS[d.outcome] }}
              ></span>
              <span className="text-neutral-300">{d.title}</span>
              <span className="text-neutral-600 text-xs ml-auto capitalize">
                {d.outcome}
              </span>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}

export default DashboardView;
