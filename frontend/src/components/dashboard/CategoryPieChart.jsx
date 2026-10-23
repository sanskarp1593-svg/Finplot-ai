import React from "react";

export function CategoryPieChart({ data = [], title = "Expenses by Category" }) {
  if (!data || data.length === 0) {
    return (
      <div className="bg-slate-900 border border-slate-800 rounded-xl p-6 flex items-center justify-center h-64 text-sm text-slate-500">
        No category expenses recorded for this month.
      </div>
    );
  }

  const colors = [
    "#10b981", // emerald
    "#6366f1", // indigo
    "#f59e0b", // amber
    "#f43f5e", // rose
    "#06b6d4", // cyan
    "#a855f7", // purple
    "#ec4899", // pink
    "#3b82f6", // blue
    "#84cc16", // lime
    "#64748b", // slate
  ];

  const total = data.reduce((acc, curr) => acc + (curr.amount || 0), 0);

  return (
    <div className="bg-slate-900 border border-slate-800 rounded-xl p-6">
      <div className="flex items-center justify-between mb-4">
        <h3 className="text-base font-semibold text-white tracking-tight">
          {title}
        </h3>
        <span className="text-xs font-medium px-2.5 py-1 rounded-md bg-slate-800 text-slate-300 tabular-nums border border-slate-700/60">
          Total: ₹{total.toLocaleString("en-IN")}
        </span>
      </div>

      {/* Stacked Progress Bar */}
      <div className="h-2.5 w-full bg-slate-800 rounded-full overflow-hidden flex my-4">
        {data.map((cat, idx) => {
          const pct = total > 0 ? (cat.amount / total) * 100 : 0;
          return (
            <div
              key={idx}
              title={`${cat.category}: ₹${cat.amount.toLocaleString("en-IN")} (${pct.toFixed(1)}%)`}
              style={{
                width: `${pct}%`,
                backgroundColor: colors[idx % colors.length],
              }}
              className="h-full transition-all hover:opacity-85 cursor-pointer"
            />
          );
        })}
      </div>

      {/* Category list */}
      <div className="space-y-1.5 mt-4 max-h-72 overflow-y-auto pr-1">
        {data.map((cat, idx) => {
          const pct = total > 0 ? ((cat.amount / total) * 100).toFixed(1) : "0";
          return (
            <div
              key={idx}
              className="flex items-center justify-between text-xs py-2 border-b border-slate-800/50 last:border-0"
            >
              <div className="flex items-center gap-2.5 truncate max-w-[65%]">
                <span
                  className="w-2.5 h-2.5 rounded-sm shrink-0"
                  style={{ backgroundColor: colors[idx % colors.length] }}
                />
                <span className="truncate text-slate-300 font-medium">
                  {cat.category}
                </span>
              </div>
              <div className="flex items-center gap-3 text-right">
                <span className="font-semibold text-white tabular-nums">
                  ₹{Number(cat.amount).toLocaleString("en-IN")}
                </span>
                <span className="text-[11px] w-10 text-right text-slate-500 tabular-nums">
                  {pct}%
                </span>
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );
}
