import { useEffect, useState } from "react";
import ForceGraph2D from "react-force-graph-2d";
import axios from "axios";

const API_URL = import.meta.env.VITE_API_URL || "http://127.0.0.1:8000";

const OUTCOME_COLORS = {
  rejected: "#ef4444",
  paused: "#eab308",
  pivoted: "#3b82f6",
  approved: "#22c55e",
};

function GraphView({ highlightedIds = [] }) {
  const [graphData, setGraphData] = useState({ nodes: [], links: [] });
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [selectedNode, setSelectedNode] = useState(null);
  const [detailText, setDetailText] = useState("");
  const [detailLoading, setDetailLoading] = useState(false);
  const [archiving, setArchiving] = useState(false);

  const fetchGraph = () => {
    setLoading(true);
    axios
      .get(API_URL + "/graph")
      .then((res) => {
        const nodes = res.data.nodes.map((n) => ({
          id: n.id,
          label: n.label,
          outcome: n.outcome,
          color: OUTCOME_COLORS[n.outcome] || "#888888",
        }));
        const links = res.data.edges.map((e) => ({
          source: e.from,
          target: e.to,
          label: e.label,
        }));
        setGraphData({ nodes, links });
        setLoading(false);
      })
      .catch((err) => {
        setError(err.message);
        setLoading(false);
      });
  };

  useEffect(() => {
    fetchGraph();
  }, []);

  const handleNodeClick = (node) => {
    setSelectedNode(node);
    setDetailLoading(true);
    setDetailText("");
    axios
      .post(API_URL + "/query", { question: node.label })
      .then((res) => {
        setDetailText(res.data.answer);
        setDetailLoading(false);
      })
      .catch(() => {
        setDetailText("Failed to load detail.");
        setDetailLoading(false);
      });
  };

  const handleArchive = () => {
    setArchiving(true);
    axios
      .delete(API_URL + "/decisions/" + selectedNode.id)
      .then(() => {
        setSelectedNode(null);
        setArchiving(false);
        fetchGraph();
      })
      .catch(() => setArchiving(false));
  };

  if (loading) return <p className="text-neutral-500">Loading graph...</p>;
  if (error)
    return <p className="text-red-500">Failed to load graph: {error}</p>;
  if (graphData.nodes.length === 0)
    return (
      <p className="text-neutral-500">
        No decisions yet. Add one to get started.
      </p>
    );

  const graphWidth = selectedNode ? 700 : 1100;

  return (
    <div className="flex gap-4">
      <div
        className="border border-neutral-800 rounded"
        style={{ height: "600px" }}
      >
        <ForceGraph2D
          width={graphWidth}
          height={580}
          graphData={graphData}
          nodeLabel="label"
          nodeColor={(node) =>
            highlightedIds.includes(node.id) ? "#ffffff" : node.color
          }
          nodeCanvasObjectMode={() => "after"}
          nodeCanvasObject={(node, ctx) => {
            if (highlightedIds.includes(node.id)) {
              ctx.beginPath();
              ctx.arc(node.x, node.y, 8, 0, 2 * Math.PI);
              ctx.strokeStyle = "#ffffff";
              ctx.lineWidth = 2;
              ctx.stroke();
            }
          }}
          linkLabel="label"
          linkColor={() => "#555555"}
          backgroundColor="#000000"
          onNodeClick={handleNodeClick}
        />
      </div>

      {selectedNode && (
        <div className="w-80 border border-neutral-800 rounded p-4 bg-neutral-950 flex-shrink-0">
          <div className="flex justify-between items-start mb-2">
            <h3 className="font-semibold text-lg">{selectedNode.label}</h3>
            <button
              onClick={() => setSelectedNode(null)}
              className="text-neutral-500 hover:text-white"
            >
              ✕
            </button>
          </div>
          <span
            className="inline-block px-2 py-1 rounded text-xs font-medium mb-3"
            style={{ backgroundColor: selectedNode.color, color: "#000" }}
          >
            {selectedNode.outcome}
          </span>
          {detailLoading ? (
            <p className="text-neutral-500 text-sm">Loading detail...</p>
          ) : (
            <p className="text-neutral-300 text-sm whitespace-pre-wrap">
              {detailText}
            </p>
          )}
          <button
            onClick={handleArchive}
            disabled={archiving}
            className="mt-4 w-full bg-red-950 border border-red-800 text-red-300 rounded px-3 py-2 text-sm hover:bg-red-900 disabled:opacity-50"
          >
            {archiving ? "Archiving..." : "Archive this decision"}
          </button>
        </div>
      )}
    </div>
  );
}

export default GraphView;
