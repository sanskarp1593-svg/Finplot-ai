import React from "react";
import { BookOpen, ExternalLink } from "lucide-react";

export function SourceCitation({ sources = [] }) {
  if (!sources || sources.length === 0) return null;

  return (
    <div className="mt-3 pt-3 border-t border-slate-700/50">
      <div className="flex items-center gap-1.5 text-xs font-semibold text-slate-400 mb-2">
        <BookOpen className="w-3.5 h-3.5 text-indigo-400" />
        <span>Grounded Compliance Citations</span>
      </div>
      <div className="grid grid-cols-1 sm:grid-cols-2 gap-2">
        {sources.map((src, i) => (
          <div
            key={i}
            className="p-2.5 rounded-lg border border-slate-800 bg-slate-900/50 text-xs hover:border-indigo-500/40 transition-colors"
          >
            <div className="flex items-center justify-between font-semibold text-indigo-300 mb-1">
              <span className="truncate">{src.title}</span>
              {src.similarity && (
                <span className="text-[10px] px-1 py-0.5 rounded bg-indigo-500/20 text-indigo-300">
                  {Math.round(src.similarity * 100)}% match
                </span>
              )}
            </div>
            {src.excerpt && (
              <p className="text-[11px] text-slate-400 line-clamp-2 leading-relaxed">
                {src.excerpt}
              </p>
            )}
          </div>
        ))}
      </div>
    </div>
  );
}
