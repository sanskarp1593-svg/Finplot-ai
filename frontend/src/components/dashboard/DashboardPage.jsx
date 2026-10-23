import React, { useState, useEffect, useCallback } from "react";
import { Calendar, RefreshCw, AlertTriangle } from "lucide-react";
import { getDashboard } from "../../api/dashboard";
import { StatCard } from "./StatCard";
import { TrendChart } from "./TrendChart";
import { CategoryPieChart } from "./CategoryPieChart";
import { BudgetProgressBar } from "./BudgetProgressBar";
import { LoadingSpinner } from "../shared/LoadingSpinner";
import { useLanguage } from "../../context/LanguageContext";

export function DashboardPage() {
  const { t } = useLanguage();
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  // Infer available months or use a reasonable default set
  const currentDate = new Date();
  const buildMonthOptions = () => {
    const months = [];
    for (let i = 5; i >= 0; i--) {
      const d = new Date(currentDate.getFullYear(), currentDate.getMonth() - i, 1);
      const yyyy = d.getFullYear();
      const mm = String(d.getMonth() + 1).padStart(2, "0");
      months.push(`${yyyy}-${mm}`);
    }
    return months;
  };

  const months = buildMonthOptions();
  const [selectedMonth, setSelectedMonth] = useState(months[months.length - 1]);

  const loadData = useCallback(async (m) => {
    setLoading(true);
    setError(null);
    try {
      const res = await getDashboard(m);
      setData(res);
    } catch (err) {
      console.error("Failed to load dashboard:", err);
      setError(err.message || "Could not load dashboard data.");
      // Keep previous data if available so the UI doesn't blank out
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    loadData(selectedMonth);
  }, [selectedMonth, loadData]);

  // ── Safely extract fields from the nested backend response ──────────────
  // Backend schema: { summary: { revenue, expenses, profit, margin }, change: { revenue_change, ... }, trend: [...MonthSummary], ... }
  const summary = data?.summary ?? {};
  const change = data?.change ?? {};

  const revenue = summary.revenue ?? 0;
  const expenses = summary.expenses ?? 0;
  const profit = summary.profit ?? 0;
  const margin = summary.margin ?? 0;

  const revenue_change_pct = change.revenue_change ?? null;
  const expenses_change_pct = change.expenses_change ?? null;
  const profit_change_pct = change.profit_change ?? null;

  // trend is an array of MonthSummary objects — used for the bar chart
  const trendData = data?.trend ?? [];
  const categoryBreakdown = data?.category_breakdown ?? [];
  const budgetProgress = data?.budget_progress ?? [];

  return (
    <div className="max-w-7xl mx-auto space-y-6 animate-fade-in">
      {/* ── Header & Top Navigation (Step 2) ─────────────────────────── */}
      <div className="flex flex-col sm:flex-row justify-between sm:items-end gap-4 mb-6">
        <div>
          <div className="flex items-center gap-2.5 mb-1">
            <h1 className="text-2xl font-bold tracking-tight text-white">
              Kumar General Store
            </h1>
            <span className="px-2 py-1 bg-emerald-500/10 text-emerald-400 text-xs rounded-full flex items-center gap-1 font-medium border border-emerald-500/20">
              <span className="w-1.5 h-1.5 rounded-full bg-emerald-400 animate-pulse" />
              API Connected
            </span>
          </div>
          <p className="text-xs sm:text-sm text-slate-400">
            Real-time multi-agent cashflow intelligence and compliance monitoring.
          </p>
        </div>

        <div className="flex items-center gap-2.5 shrink-0">
          <div className="flex items-center gap-2 px-3 py-2 rounded-lg bg-slate-900 border border-slate-800 text-xs font-medium text-slate-300">
            <Calendar className="w-3.5 h-3.5 text-slate-400" />
            <select
              value={selectedMonth}
              onChange={(e) => setSelectedMonth(e.target.value)}
              className="bg-transparent border-none outline-none font-medium cursor-pointer text-slate-200"
            >
              {months.map((m) => (
                <option key={m} value={m} className="bg-slate-900 text-slate-200">
                  {m}
                </option>
              ))}
            </select>
          </div>

          <button
            onClick={() => loadData(selectedMonth)}
            className="p-2 rounded-lg bg-slate-900 border border-slate-800 text-slate-400 hover:text-white hover:bg-slate-800 transition-colors"
            title="Refresh metrics"
            disabled={loading}
          >
            <RefreshCw className={`w-4 h-4 ${loading ? "animate-spin" : ""}`} />
          </button>
        </div>
      </div>

      {/* API Error Banner */}
      {error && !data && (
        <div className="flex items-center gap-3 p-4 rounded-xl text-sm bg-rose-500/10 border border-rose-500/20 text-rose-400">
          <AlertTriangle className="w-4 h-4 shrink-0" />
          <span>
            <strong>Dashboard Error:</strong> {error} — Ensure the FastAPI backend is running on{" "}
            <code>localhost:8000</code>.
          </span>
        </div>
      )}

      {loading && !data ? (
        <LoadingSpinner text="Computing financial metrics…" />
      ) : (
        <>
          {/* ── Key Metric Cards (Step 3) ── */}
          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
            <StatCard
              title={t("totalRevenue")}
              amount={revenue}
              change={revenue_change_pct}
              type="revenue"
            />
            <StatCard
              title={t("totalExpenses")}
              amount={expenses}
              change={expenses_change_pct}
              type="expense"
            />
            <StatCard
              title={t("netProfit")}
              amount={profit}
              change={profit_change_pct}
              type={profit >= 0 ? "revenue" : "expense"}
            />
            <StatCard
              title={t("profitMargin")}
              amount={margin}
              isPercentage={true}
              isCurrency={false}
              change={null}
              type="revenue"
            />
          </div>

          {/* ── Historical Trend Chart (Step 4) ── */}
          <TrendChart data={trendData} />

          {/* ── Bottom Grid: Category Breakdown & Budget Progress (Step 5) ── */}
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 mt-6">
            <CategoryPieChart
              data={categoryBreakdown}
              title={t("expenseByCategory")}
            />
            <BudgetProgressBar
              items={budgetProgress}
              title={t("budgetTracking")}
            />
          </div>
        </>
      )}
    </div>
  );
}
