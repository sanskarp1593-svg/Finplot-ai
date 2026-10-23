import React from "react";
import { TrendingUp, TrendingDown, Minus } from "lucide-react";

export function StatCard({ title, amount, change, isCurrency = true, isPercentage = false, subtitle, type = "neutral" }) {
  const formatValue = () => {
    if (amount === undefined || amount === null) {
      return isPercentage ? "0.0%" : "₹0";
    }
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
    <div className="bg-slate-900 border border-slate-800 rounded-xl p-5 shadow-sm flex flex-col justify-between transition-colors hover:border-slate-700/70">
      <div>
        <p className="text-sm font-medium text-slate-400 uppercase tracking-wider mb-2">
          {title}
        </p>
        <p className="text-3xl font-semibold text-white tabular-nums tracking-tight">
          {formatValue()}
        </p>
      </div>

      <div className="flex items-center gap-1.5 text-xs text-slate-500 mt-2">
        {change !== undefined && change !== null && (
          <span className={`flex items-center gap-1 font-semibold ${getChangeColor()}`}>
            {getTrendIcon()}
            {change > 0 ? `+${change.toFixed(1)}%` : `${change.toFixed(1)}%`}
          </span>
        )}
        <span>{subtitle || "vs prior month"}</span>
      </div>
    </div>
  );
}
