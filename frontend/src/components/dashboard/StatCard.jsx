import React from "react";
import { TrendingUp, TrendingDown, Minus } from "lucide-react";

export function StatCard({ title, amount, change, isCurrency = true, isPercentage = false, subtitle, type = "neutral" }) {
  const formatValue = () => {
    if (amount === undefined || amount === null) return "—";
    if (isPercentage) return `${Number(amount).toFixed(1)}%`;
    if (isCurrency) {
      return `₹${Number(amount).toLocaleString("en-IN", {
        maximumFractionDigits: 0,
      })}`;
    }
    return amount;
  };

  const getTrendIcon = () => {
    if (change === undefined || change === null || change === 0) {
      return <Minus className="w-3.5 h-3.5" />;
    }
    if (change > 0) {
      return <TrendingUp className="w-3.5 h-3.5 text-emerald-400" />;
    }
    return <TrendingDown className="w-3.5 h-3.5 text-rose-400" />;
  };

  const getChangeColor = () => {
    if (change === undefined || change === null || change === 0) return "text-slate-400";
    if (type === "expense") {
      // For expense, higher is usually warning
      return change > 0 ? "text-amber-400" : "text-emerald-400";
    }
    return change > 0 ? "text-emerald-400" : "text-rose-400";
  };

  return (
    <div className="glass-card p-5 relative overflow-hidden group">
      <div className="flex items-center justify-between mb-2">
        <span className="text-xs font-semibold uppercase tracking-wider" style={{ color: "var(--text-muted)" }}>
          {title}
        </span>
      </div>

      <div className="stat-value text-2xl font-extrabold my-1" style={{ color: "var(--text-primary)" }}>
        {formatValue()}
      </div>

      <div className="flex items-center gap-1.5 mt-2 text-xs font-medium">
        {change !== undefined && change !== null && (
          <span className={`flex items-center gap-1 font-semibold ${getChangeColor()}`}>
            {getTrendIcon()}
            {change > 0 ? `+${change.toFixed(1)}%` : `${change.toFixed(1)}%`}
          </span>
        )}
        <span style={{ color: "var(--text-muted)" }}>{subtitle || "vs prior month"}</span>
      </div>
    </div>
  );
}
