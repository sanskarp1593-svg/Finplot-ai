import React from "react";

export function TrendChart({ data = [], title = "Financial Trend (6 Months)" }) {
  if (!data || data.length === 0) {
    return (
      <div className="glass-panel p-6 flex items-center justify-center h-64 text-sm" style={{ color: "var(--text-muted)" }}>
        No historical data available.
      </div>
    );
  }

  // Find max value for scaling
  const maxVal = Math.max(
    ...data.map((d) => Math.max(d.revenue || 0, d.expenses || 0, Math.abs(d.profit || 0))),
    1000
  );

  return (
    <div className="glass-panel p-6">
      <div className="flex items-center justify-between mb-6">
        <h3 className="font-bold text-sm tracking-wide" style={{ color: "var(--text-primary)" }}>
          {title}
        </h3>
        <div className="flex items-center gap-4 text-xs font-semibold">
          <div className="flex items-center gap-1.5">
            <span className="w-2.5 h-2.5 rounded-full bg-emerald-500" />
            <span style={{ color: "var(--text-secondary)" }}>Revenue</span>
          </div>
          <div className="flex items-center gap-1.5">
            <span className="w-2.5 h-2.5 rounded-full bg-rose-500" />
            <span style={{ color: "var(--text-secondary)" }}>Expenses</span>
          </div>
          <div className="flex items-center gap-1.5">
            <span className="w-2.5 h-2.5 rounded-full bg-indigo-500" />
            <span style={{ color: "var(--text-secondary)" }}>Profit</span>
          </div>
        </div>
      </div>

      <div className="h-56 flex items-end gap-3 sm:gap-6 pt-6 pb-2 border-b" style={{ borderColor: "var(--border-subtle)" }}>
        {data.map((item, idx) => {
          const revHeight = Math.max(6, (item.revenue / maxVal) * 160);
          const expHeight = Math.max(6, (item.expenses / maxVal) * 160);
          const profHeight = Math.max(4, (Math.abs(item.profit || 0) / maxVal) * 160);
          const isProfPositive = (item.profit || 0) >= 0;

          return (
            <div key={idx} className="flex-1 flex flex-col items-center gap-1 group relative">
              {/* Tooltip */}
              <div className="absolute -top-16 opacity-0 group-hover:opacity-100 transition-opacity pointer-events-none z-20 px-3 py-1.5 rounded-lg shadow-xl text-xs whitespace-nowrap" style={{ background: "var(--bg-secondary)", border: "1px solid var(--border-strong)", color: "var(--text-primary)" }}>
                <p className="font-bold">{item.month}</p>
                <p className="text-emerald-400">Rev: ₹{Number(item.revenue).toLocaleString("en-IN")}</p>
                <p className="text-rose-400">Exp: ₹{Number(item.expenses).toLocaleString("en-IN")}</p>
                <p className={isProfPositive ? "text-indigo-400" : "text-amber-400"}>
                  Net: ₹{Number(item.profit).toLocaleString("en-IN")}
                </p>
              </div>

              {/* Grouped Bars */}
              <div className="w-full flex items-end justify-center gap-1 h-44">
                <div
                  className="w-1/3 max-w-[14px] bg-emerald-500/80 hover:bg-emerald-400 rounded-t-sm transition-all"
                  style={{ height: `${revHeight}px` }}
                />
                <div
                  className="w-1/3 max-w-[14px] bg-rose-500/80 hover:bg-rose-400 rounded-t-sm transition-all"
                  style={{ height: `${expHeight}px` }}
                />
                <div
                  className={`w-1/3 max-w-[14px] rounded-t-sm transition-all ${
                    isProfPositive ? "bg-indigo-500 hover:bg-indigo-400" : "bg-amber-500 hover:bg-amber-400"
                  }`}
                  style={{ height: `${profHeight}px` }}
                />
              </div>

              <span className="text-[11px] font-medium mt-2" style={{ color: "var(--text-muted)" }}>
                {item.month ? item.month.substring(5) : ""}
              </span>
            </div>
          );
        })}
      </div>
    </div>
  );
}
