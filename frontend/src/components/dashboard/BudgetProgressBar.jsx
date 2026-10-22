import React from "react";
import { AlertCircle, CheckCircle2 } from "lucide-react";

export function BudgetProgressBar({ items = [], title = "Budget Tracking & Burn Rate" }) {
  if (!items || items.length === 0) {
    return (
      <div className="glass-panel p-6 flex items-center justify-center h-64 text-sm" style={{ color: "var(--text-muted)" }}>
        No budgets configured. Set limits in Settings.
      </div>
    );
  }

  return (
    <div className="glass-panel p-6">
      <div className="flex items-center justify-between mb-4">
        <h3 className="font-bold text-sm tracking-wide" style={{ color: "var(--text-primary)" }}>
          {title}
        </h3>
        <span className="text-xs font-medium" style={{ color: "var(--text-muted)" }}>
          {items.filter((i) => i.over_budget).length} over limit
        </span>
      </div>

      <div className="space-y-4 max-h-72 overflow-y-auto pr-1">
        {items.map((b, idx) => {
          const pct = b.percentage || (b.limit > 0 ? (b.spent / b.limit) * 100 : 0);
          const isOver = b.over_budget || pct > 100;

          return (
            <div key={idx} className="space-y-1.5">
              <div className="flex items-center justify-between text-xs">
                <div className="flex items-center gap-1.5">
                  <span className="font-semibold" style={{ color: "var(--text-primary)" }}>
                    {b.category}
                  </span>
                  {isOver ? (
                    <span className="badge badge-danger text-[10px] py-0 px-1.5 flex items-center gap-1">
                      <AlertCircle className="w-2.5 h-2.5" /> Over Budget
                    </span>
                  ) : (
                    <span className="badge badge-success text-[10px] py-0 px-1.5 flex items-center gap-1">
                      <CheckCircle2 className="w-2.5 h-2.5" /> On Track
                    </span>
                  )}
                </div>
                <div className="text-right">
                  <span className="font-bold" style={{ color: isOver ? "var(--danger)" : "var(--text-primary)" }}>
                    ₹{Number(b.spent).toLocaleString("en-IN")}
                  </span>
                  <span className="text-[11px]" style={{ color: "var(--text-muted)" }}>
                    {" "}
                    / ₹{Number(b.limit).toLocaleString("en-IN")}
                  </span>
                </div>
              </div>

              {/* Progress track */}
              <div className="h-2 w-full rounded-full overflow-hidden bg-slate-800/40">
                <div
                  className="h-full rounded-full transition-all duration-500"
                  style={{
                    width: `${Math.min(100, pct)}%`,
                    background: isOver
                      ? "linear-gradient(90deg, #f87171, #ef4444)"
                      : pct > 80
                      ? "linear-gradient(90deg, #fbbf24, #f59e0b)"
                      : "linear-gradient(90deg, #6366f1, #34d399)",
                  }}
                />
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );
}
