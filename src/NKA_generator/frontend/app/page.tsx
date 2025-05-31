"use client";

import React, { useState } from "react";
import ReactFlow, { Background, Controls, Node, Edge } from "reactflow";
import "reactflow/dist/style.css";
import BlackNode from "./components/BlackNode";
import { FaTrashAlt } from "react-icons/fa";
const nodeTypes = { black: BlackNode };


interface DerivationTreeNode {
  label: string;
  children?: DerivationTreeNode[];
}

function convertTreeToReactFlow(
    tree: DerivationTreeNode,
    parent: string | null = null,
    nodes: Node[] = [],
    edges: Edge[] = [],
    path: string = "0",
    depth: number = 0,
    x: number = 0
): { nodes: Node[]; edges: Edge[]; width: number } {
  const id = path;


  let childrenWidths: number[] = [];
  let totalWidth = 0;
  if (tree.children && tree.children.length > 0) {
    for (let i = 0; i < tree.children.length; ++i) {
      const child = tree.children[i];
      const res = convertTreeToReactFlow(child, null, [], [], "", 0, 0);
      childrenWidths.push(res.width);
      totalWidth += res.width;
    }
  }
  if (totalWidth === 0) totalWidth = 1;

  nodes.push({
    id,
    data: { label: tree.label },
    position: { x: x + totalWidth * 120 / 2, y: depth * 120 },
    type: "black",
  });

  if (parent) {
    edges.push({
      id: `${parent}-${id}`,
      source: parent,
      target: id,
      type: "straight",
    });
  }

  let childX = x;
  if (tree.children && tree.children.length > 0) {
    for (let i = 0; i < tree.children.length; ++i) {
      const child = tree.children[i];
      const w = childrenWidths[i];
      convertTreeToReactFlow(
          child,
          id,
          nodes,
          edges,
          `${path}-${i}`,
          depth + 1,
          childX
      );
      childX += w * 120;
    }
  }

  return { nodes, edges, width: totalWidth };
}

export default function Home() {
  const [word, setWord] = useState("");
  const [testResult, setTestResult] = useState<boolean | null>(null);


  const [regex, setRegex] = useState("");
  const [flow, setFlow] = useState<{ nodes: Node[]; edges: Edge[] }>({
    nodes: [],
    edges: [],
  });
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [history, setHistory] = useState<string[]>([]);

  const backendUrl =
      process.env.NEXT_PUBLIC_BACKEND_URL || "http://localhost:8000";


  const addToHistory = (expr: string) => {
    setHistory((prev) => {
      const newHistory = [expr, ...prev.filter((e) => e !== expr)];
      return newHistory.slice(0, 10);
    });
  };

  const handleFetchTree = async (customExpr?: string) => {
    setLoading(true);
    setError(null);
    setFlow({ nodes: [], edges: [] });
    const expr = customExpr ?? regex;
    try {
      const res = await fetch(`${backendUrl}/tree`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ regex: expr }),
      });
      if (!res.ok) throw new Error(await res.text());
      const tree: DerivationTreeNode = await res.json();
      const { nodes, edges } = convertTreeToReactFlow(tree);
      setFlow({ nodes, edges });
      setRegex(expr);
      addToHistory(expr);
    } catch (e: any) {
      setError(e.message || "Chyba pri načítaní stromu.");
    }
    setLoading(false);
  };

  const handleTestWord = async () => {
    setTestResult(null);
    if (!regex.trim() || !word.trim()) return;
    try {
      const res = await fetch(`${backendUrl}/simulate`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ regex, word }),
      });
      if (!res.ok) throw new Error(await res.text());
      const { accepted } = await res.json();
      setTestResult(accepted);
    } catch {
      setTestResult(false);
    }
  };
  return (
      <main className="min-h-screen bg-black flex flex-col items-center py-8">
        <h1 className="text-3xl font-bold mb-6 text-center text-white tracking-wider">
          NKA GENERATOR
        </h1>

        <div className="w-full max-w-6xl mb-6">
          <div className="flex gap-2">
            <input
                className="flex-1 px-4 py-2 border border-2 border-white text-white bg-black rounded text-lg"
                value={regex}
                onChange={(e) => setRegex(e.target.value)}
                placeholder="Zadaj regulárny výraz (napr. {ab|c})"
                onKeyDown={(e) => { if (e.key === "Enter") handleFetchTree(); }}
            />
            <button
                onClick={() => handleFetchTree()}
                className="px-6 py-2 bg-white text-black rounded font-semibold text-lg hover:bg-neutral-400 transition"
            >
              Vykresli strom
            </button>
          </div>
        </div>

        <div className="flex w-full max-w-6xl gap-6">
          <div className="flex-1">
            {loading && <div className="text-center text-lg text-white">Načítavam...</div>}
            {error && (
                <div className="text-red-500 font-semibold text-center mb-2">
                  {error}
                </div>
            )}
            <div className="w-full h-[70vh] rounded-[20px] border border-3 border-white bg-none">
              <ReactFlow
                  nodeTypes={nodeTypes}
                  nodes={flow.nodes}
                  edges={flow.edges}
                  fitView
              >
                <Background />
                <Controls />
              </ReactFlow>
            </div>
          </div>

          <div className="w-[300px] h-[70vh] flex flex-col gap-4">

            <div className="bg-black border-3 border-white rounded-xl px-4 py-3 flex-1 flex flex-col min-h-[0]">
              <h2 className="text-lg font-bold text-white mb-3 text-center">História výrazov</h2>
              <ul className="flex-1 flex flex-col gap-3 overflow-y-auto">
                {history.length === 0 && (
                    <li className="text-gray-400 text-center"></li>
                )}
                {history.map((expr, idx) => (
                    <li key={idx} className="flex items-center group">
                      <button
                          onClick={() => handleFetchTree(expr)}
                          className={`flex-1 text-left px-3 py-2 rounded-lg font-mono text-white border border-white hover:scale-[99%] duration-300 cursor-pointer transition ${
                              regex === expr ? "bg-black" : ""
                          }`}
                      >
                        {expr}
                      </button>
                      <button
                          onClick={() =>
                              setHistory((prev) =>
                                  prev.filter((_, i) => i !== idx)
                              )
                          }
                          className="ml-2 p-1 rounded  transition"
                          title="Odstrániť z histórie"
                      >
                        <FaTrashAlt className="text-white hover:text-red-500 duration-300 cursor-pointer transition" />
                      </button>
                    </li>
                ))}
              </ul>
            </div>

            <div className="bg-black border-3 border-white rounded-xl px-4 py-3 flex flex-col items-center">
              <h2 className="text-lg font-bold text-white mb-3 text-center">Testovanie slova</h2>
              <input
                  className="w-full px-3 py-2 border border-white rounded-lg mb-3 text-white bg-black"
                  placeholder="Zadaj slovo"
                  value={word}
                  onChange={e => setWord(e.target.value)}
                  onKeyDown={e => { if (e.key === "Enter") handleTestWord(); }}
              />
              <button
                  className="w-full bg-white text-black px-4 py-2 rounded-lg font-semibold hover:bg-neutral-400 transition mb-2"
                  onClick={handleTestWord}
              >
                Otestuj
              </button>
              {testResult !== null && (
                  <div className={`font-semibold mt-2 ${testResult ? "text-green-400" : "text-red-400"}`}>
                    {testResult ? "Slovo je akceptované!" : "Slovo NIE JE akceptované."}
                  </div>
              )}
            </div>
          </div>
        </div>
      </main>
  );
}
