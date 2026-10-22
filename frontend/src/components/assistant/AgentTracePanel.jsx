import React, { useState } from "react";
import { ChevronDown, ChevronRight, Cpu, Clock } from "lucide-react";

export function AgentTracePanel({ traces = [], agentsUsed = [] }) {
  const [isOpen, setIsOpen] = useState(false);

  if (!traces || traces.length === 0) return null;

  return (
    <div className="mt-3 border border-indigo-500/20 rounded-xl bg-indigo-950/20 overflow-hidden text-xs">
      <button
        onClick={() => setIsOpen(!isOpen)}
        className="w-full flex items-center justify-between px-3 py-2 text-indigo-300 hover:bg-indigo-900/20 transition-colors"
      >
        <div className="flex items-center gap-2 font-medium">
          <Cpu className="w-3.5 h-3.5 text-indigo-400" />
          <span>Multi-Agent Workflow Trace ({agentsUsed.join(" → ")})</span>
        </div>
        <div className="flex items-center gap-1.5 text-[11px] text-slate-400">
          <span>{traces.length} steps</span>
          {isOpen ? <ChevronDown className="w-3.5 h-3.5" /> : <ChevronRight className="w-3.5 h-3.5" />}
        </div>
      </button>

      {isOpen && (
        <div className="p-3 border-t border-indigo-500/20 space-y-2 bg-slate-950/50">
          {traces.map((trace, idx) => (
            <div key={idx} className="p-2 rounded-lg bg-slate-900/70 border border-slate-800 text-[11px] space-y-1">
              <div className="flex items-center justify-between font-bold text-slate-300">
                <span className="capitalize text-indigo-400">Agent: {trace.agent}</span>
                <span className="flex items-center gap-1 text-slate-500 font-mono">
                  <Clock className="w-2.5 h-2.5" /> {trace.duration_ms}ms
                </span>
              </div>
              {trace.input_summary && (
                <div className="text-slate-400 truncate">
                  <span className="text-slate-500">In:</span> {trace.input_summary}
                </div>
              )}
              {trace.output_summary && (
                <div className="text-slate-300 truncate">
                  <span className="text-slate-500">Out:</span> {trace.output_summary}
                </div>
              )}
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
