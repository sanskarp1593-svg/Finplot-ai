import React from "react";

export function BudgetProgressBar({ items = [], title = "Budget Tracking & Burn Rate" }) {
  if (!items || items.length === 0) {
    return (
      <div className="bg-slate-900 border border-slate-800 rounded-xl p-6 flex items-center justify-center h-64 text-sm text-slate-500">
        No budgets configured. Set limits in Settings.
      </div>
    );
  }

  const overLimitCount = items.filter((i) => i.over_budget).length;

  return (
    <div className="bg-slate-900 border border-slate-800 rounded-xl p-6">
      <div className="flex items-center justify-between mb-4">
        <h3 className="text-base font-semibold text-white tracking-tight">
          {title}
        </h3>
        <span className="text-xs font-medium text-slate-400">
          {overLimitCount > 0 ? (
            <span className="text-rose-400 font-medium">{overLimitCount} over limit</span>
          ) : (
            <span className="text-emerald-400 font-medium">All within budget</span>
          )}
        </span>
      </div>

      <ul className="divide-y divide-slate-800/50 max-h-80 overflow-y-auto pr-1">
        {items.map((b, idx) => {
          const pct = b.percentage || (b.limit > 0 ? (b.spent / b.limit) * 100 : 0);
          const isOver = b.over_budget || pct > 100;

          return (
            <li key={idx} className="flex justify-between items-center py-3 border-b border-slate-800/50 last:border-0">
              <div className="flex items-center gap-2">
                <span className="font-medium text-slate-200 text-sm">
                  {b.category}
                </span>
                {isOver ? (
                  <span className="px-2 py-0.5 rounded-md bg-rose-500/10 text-rose-400 text-xs font-medium border border-rose-500/20">
                    Over Budget
                  </span>
                ) : (
                  <span className="px-2 py-0.5 rounded-md bg-emerald-500/10 text-emerald-400 text-xs font-medium">
                    On Track
                  </span>
                )}
              </div>

              <div className="flex items-center gap-4">
                <div className="w-24 hidden sm:block">
                  <div className="h-1.5 w-full bg-slate-800 rounded-full overflow-hidden">
                    <div
                      className="h-full rounded-full transition-all duration-500"
                      style={{
                        width: `${Math.min(100, pct)}%`,
                        backgroundColor: isOver ? "#f43f5e" : pct > 80 ? "#f59e0b" : "#10b981",
                      }}
                    />
                  </div>
                </div>

                <div className="text-right text-xs">
                  <span className={`font-semibold tabular-nums ${isOver ? "text-rose-400" : "text-white"}`}>
                    ₹{Number(b.spent).toLocaleString("en-IN")}
                  </span>
                  <span className="text-slate-500 tabular-nums">
                    {" "}
                    / ₹{Number(b.limit).toLocaleString("en-IN")}
                  </span>
                </div>
              </div>
            </li>
          );
        })}
      </ul>
    </div>
  );
}
