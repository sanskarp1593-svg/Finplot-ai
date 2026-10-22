import React from "react";

export function ChartWidget({ chart }) {
  if (!chart || !chart.labels || chart.labels.length === 0) return null;

  const dataset = chart.datasets && chart.datasets[0] ? chart.datasets[0] : { data: [] };
  const values = dataset.data || [];
  const maxVal = Math.max(...values, 100);

  const colors = ["#6366f1", "#a855f7", "#ec4899", "#f59e0b", "#10b981", "#06b6d4", "#3b82f6"];

  return (
    <div className="my-3 p-4 rounded-xl border border-subtle bg-slate-900/60 shadow-inner">
      {chart.title && (
        <h4 className="text-xs font-bold uppercase tracking-wider mb-3 text-slate-300">
          {chart.title}
        </h4>
      )}

      {chart.chart_type === "bar" || chart.chart_type === "pie" ? (
        <div className="space-y-2">
          {chart.labels.map((label, i) => {
            const val = values[i] || 0;
            const pct = maxVal > 0 ? (val / maxVal) * 100 : 0;
            const color = colors[i % colors.length];

            return (
              <div key={i} className="space-y-1">
                <div className="flex items-center justify-between text-xs">
                  <span className="text-slate-300 truncate max-w-[60%]">{label}</span>
                  <span className="font-semibold text-slate-200">
                    ₹{Number(val).toLocaleString("en-IN")}
                  </span>
                </div>
                <div className="h-1.5 w-full bg-slate-800 rounded-full overflow-hidden">
                  <div
                    className="h-full rounded-full transition-all duration-300"
                    style={{ width: `${pct}%`, backgroundColor: color }}
                  />
                </div>
              </div>
            );
          })}
        </div>
      ) : null}
    </div>
  );
}
