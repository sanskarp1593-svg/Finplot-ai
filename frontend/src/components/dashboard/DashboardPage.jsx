import React, { useState, useEffect } from "react";
import { Calendar, RefreshCw } from "lucide-react";
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
  const [selectedMonth, setSelectedMonth] = useState("2026-07");

  const months = ["2026-06", "2026-07", "2026-08"];

  const loadData = async (m) => {
    setLoading(true);
    try {
      const res = await getDashboard(m);
      setData(res);
    } catch (err) {
      console.error("Failed to load dashboard:", err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadData(selectedMonth);
  }, [selectedMonth]);

  return (
    <div className="p-6 max-w-7xl mx-auto space-y-6 animate-fade-in">
      {/* Page Title & Month Filter */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
        <div>
          <h2 className="text-xl font-bold tracking-tight" style={{ fontFamily: "var(--font-display)", color: "var(--text-primary)" }}>
            {t("monthlyOverview")}
          </h2>
          <p className="text-xs" style={{ color: "var(--text-muted)" }}>
            Real-time multi-agent cashflow intelligence and compliance monitoring.
          </p>
        </div>

        <div className="flex items-center gap-2">
          <div className="flex items-center gap-2 px-3 py-1.5 rounded-xl border border-subtle text-xs font-semibold" style={{ background: "var(--bg-secondary)" }}>
            <Calendar className="w-3.5 h-3.5 text-indigo-400" />
            <select
              value={selectedMonth}
              onChange={(e) => setSelectedMonth(e.target.value)}
              className="bg-transparent border-none outline-none font-semibold cursor-pointer"
              style={{ color: "var(--text-primary)" }}
            >
              {months.map((m) => (
                <option key={m} value={m} style={{ background: "var(--bg-secondary)", color: "var(--text-primary)" }}>
                  {m}
                </option>
              ))}
            </select>
          </div>

          <button
            onClick={() => loadData(selectedMonth)}
            className="btn btn-secondary p-2"
            title="Refresh metrics"
          >
            <RefreshCw className={`w-3.5 h-3.5 ${loading ? "animate-spin" : ""}`} />
          </button>
        </div>
      </div>

      {loading && !data ? (
        <LoadingSpinner text="Computing financial metrics..." />
      ) : data ? (
        <>
          {/* Key Metric Cards */}
          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
            <StatCard
              title={t("totalRevenue")}
              amount={data.revenue}
              change={data.revenue_change_pct}
              type="revenue"
            />
            <StatCard
              title={t("totalExpenses")}
              amount={data.expenses}
              change={data.expenses_change_pct}
              type="expense"
            />
            <StatCard
              title={t("netProfit")}
              amount={data.profit}
              change={data.profit_change_pct}
              type={data.profit >= 0 ? "revenue" : "expense"}
            />
            <StatCard
              title={t("profitMargin")}
              amount={data.margin}
              isPercentage={true}
              isCurrency={false}
              change={data.margin_change_pct}
              type="revenue"
            />
          </div>

          {/* Historical Trend Chart */}
          <TrendChart data={data.sparkline_data || []} />

          {/* Bottom Grid: Category Breakdown & Budget Progress */}
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
            <CategoryPieChart
              data={data.category_breakdown || []}
              title={t("expenseByCategory")}
            />
            <BudgetProgressBar
              items={data.budget_progress || []}
              title={t("budgetTracking")}
            />
          </div>
        </>
      ) : (
        <div className="glass-panel p-8 text-center text-sm" style={{ color: "var(--text-muted)" }}>
          Failed to load dashboard data. Ensure the backend is running.
        </div>
      )}
    </div>
  );
}
