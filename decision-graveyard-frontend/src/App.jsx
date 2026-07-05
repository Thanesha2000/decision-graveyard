import { useState } from "react";
import GraphView from "./GraphView";
import QueryView from "./QueryView";
import AddDecisionView from "./AddDecisionView";
import DashboardView from "./DashboardView";

const SECTIONS = ["Graph", "Query", "Add Decision", "Dashboard"];

function App() {
  const [activeSection, setActiveSection] = useState("Graph");
  const [highlightedIds, setHighlightedIds] = useState([]);

  return (
    <div className="min-h-screen bg-black text-white flex">
      <aside className="w-56 border-r border-neutral-800 p-4">
        <h1 className="text-xl font-bold mb-6">Decision Graveyard</h1>
        <nav className="flex flex-col gap-2">
          {SECTIONS.map((section) => (
            <button
              key={section}
              onClick={() => setActiveSection(section)}
              className={`text-left px-3 py-2 rounded ${
                activeSection === section
                  ? "bg-neutral-800 text-white"
                  : "text-neutral-400 hover:bg-neutral-900"
              }`}
            >
              {section}
            </button>
          ))}
        </nav>
      </aside>

      <main className="flex-1 p-6">
        <h2 className="text-2xl font-semibold mb-4">{activeSection}</h2>
        {activeSection === "Graph" && (
          <GraphView highlightedIds={highlightedIds} />
        )}
        {activeSection === "Query" && (
          <QueryView onAnswer={(ids) => setHighlightedIds(ids)} />
        )}
        {activeSection === "Add Decision" && <AddDecisionView />}
        {activeSection === "Dashboard" && <DashboardView />}
      </main>
    </div>
  );
}

export default App;
