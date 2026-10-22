import React from "react";

export function CategoryPieChart({ data = [], title = "Expenses by Category" }) {
  if (!data || data.length === 0) {
    return (
      <div className="glass-panel p-6 flex items-center justify-center h-64 text-sm" style={{ color: "var(--text-muted)" }}>
        No category expenses recorded for this month.
      </div>
    );
  }

  const colors = [
    "#6366f1", // indigo
    "#a855f7", // purple
    "#ec4899", // pink
    "#f59e0b", // amber
    "#10b981", // emerald
    "#06b6d4", // cyan
    "#3b82f6", // blue
    "#f97316", // orange
    "#84cc16", // lime
    "#64748b", // slate
  ];

  const total = data.reduce((acc, curr) => acc + (curr.amount || 0), 0);

  return (
    <div className="glass-panel p-6">
      <div className="flex items-center justify-between mb-4">
        <h3 className="font-bold text-sm tracking-wide" style={{ color: "var(--text-primary)" }}>
          {title}
        </h3>
        <span className="text-xs font-semibold px-2 py-0.5 rounded-md" style={{ background: "var(--primary-subtle)", color: "var(--primary)" }}>
          Total: ₹{total.toLocaleString("en-IN")}
        </span>
      </div>

      {/* Stacked Progress Bar */}
      <div className="h-3 w-full rounded-full overflow-hidden flex my-4 bg-slate-800/40">
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
              className="h-full transition-all hover:opacity-80 cursor-pointer"
            />
          );
        })}
      </div>

      {/* Legend list */}
      <div className="space-y-2 mt-4 max-h-52 overflow-y-auto pr-1">
        {data.map((cat, idx) => {
          const pct = total > 0 ? ((cat.amount / total) * 100).toFixed(1) : "0";
          return (
            <div key={idx} className="flex items-center justify-between text-xs py-1 border-b border-subtle last:border-0">
              <div className="flex items-center gap-2 truncate max-w-[65%]">
                <span
                  className="w-2.5 h-2.5 rounded-sm shrink-0"
                  style={{ backgroundColor: colors[idx % colors.length] }}
                />
                <span className="truncate" style={{ color: "var(--text-primary)" }}>
                  {cat.category}
                </span>
              </div>
              <div className="flex items-center gap-2 text-right">
                <span className="font-semibold" style={{ color: "var(--text-primary)" }}>
                  ₹{Number(cat.amount).toLocaleString("en-IN")}
                </span>
                <span className="text-[11px] w-9 text-right" style={{ color: "var(--text-muted)" }}>
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
