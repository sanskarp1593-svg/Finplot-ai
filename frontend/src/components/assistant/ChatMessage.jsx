import React from "react";
import { Sparkles, User, AlertTriangle } from "lucide-react";
import { ChartWidget } from "./ChartWidget";
import { SourceCitation } from "./SourceCitation";
import { AgentTracePanel } from "./AgentTracePanel";

export function ChatMessage({ message }) {
  const isUser = message.role === "user";

  return (
    <div className={`flex gap-3 my-4 ${isUser ? "justify-end" : "justify-start"}`}>
      {!isUser && (
        <div className="w-8 h-8 rounded-xl bg-gradient-to-tr from-indigo-600 to-violet-500 flex items-center justify-center text-white shrink-0 shadow-md">
          <Sparkles className="w-4 h-4" />
        </div>
      )}

      <div
        className={`max-w-2xl rounded-2xl p-4 shadow-sm text-sm leading-relaxed ${
          isUser
            ? "bg-indigo-600 text-white rounded-br-none"
            : "border border-subtle rounded-bl-none text-slate-100"
        }`}
        style={!isUser ? { background: "var(--bg-secondary)" } : {}}
      >
        {/* Main Text Content */}
        <div className="whitespace-pre-wrap font-sans text-sm">
          {message.content}
        </div>

        {/* CA Review Banner */}
        {!isUser && message.needs_ca_review && (
          <div className="mt-3 p-3 rounded-xl bg-amber-500/10 border border-amber-500/30 flex items-start gap-2.5 text-amber-400 text-xs">
            <AlertTriangle className="w-4 h-4 shrink-0 mt-0.5 text-amber-400" />
            <div>
              <p className="font-bold">CA Verification Recommended</p>
              <p className="text-[11px] opacity-90 mt-0.5">
                This advice involves tax, legal, or statutory interpretation. Please consult with your Chartered Accountant prior to filing.
              </p>
            </div>
          </div>
        )}

        {/* Charts */}
        {!isUser && message.charts && message.charts.map((c, i) => (
          <ChartWidget key={i} chart={c} />
        ))}

        {/* Compliance Sources */}
        {!isUser && message.sources && (
          <SourceCitation sources={message.sources} />
        )}

        {/* Multi-Agent Trace */}
        {!isUser && message.traces && (
          <AgentTracePanel traces={message.traces} agentsUsed={message.agents_used} />
        )}
      </div>

      {isUser && (
        <div className="w-8 h-8 rounded-xl bg-slate-700 flex items-center justify-center text-slate-200 shrink-0">
          <User className="w-4 h-4" />
        </div>
      )}
    </div>
  );
}
