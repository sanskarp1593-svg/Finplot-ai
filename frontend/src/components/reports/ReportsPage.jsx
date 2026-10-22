import React, { useState, useEffect } from "react";
import { BarChart3, TrendingUp, Calendar, FileSpreadsheet } from "lucide-react";
import { getPnLReport, getCategoryReport } from "../../api/reports";
import { LoadingSpinner } from "../shared/LoadingSpinner";
import { useLanguage } from "../../context/LanguageContext";

export function ReportsPage() {
  const { t } = useLanguage();
  const [pnlData, setPnlData] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    async function loadReports() {
      setLoading(true);
      try {
        const res = await getPnLReport();
        setPnlData(res || []);
      } catch (err) {
        console.error("Failed to load reports:", err);
      } finally {
        setLoading(false);
      }
    }
    loadReports();
  }, []);

  return (
    <div className="p-6 max-w-6xl mx-auto space-y-6 animate-fade-in">
      {/* Header */}
      <div>
        <h2 className="text-xl font-bold tracking-tight" style={{ fontFamily: "var(--font-display)", color: "var(--text-primary)" }}>
          {t("pnlReport")}
        </h2>
        <p className="text-xs" style={{ color: "var(--text-muted)" }}>
          Monthly aggregated Profit and Loss statement calculated directly from double-checked ledger transactions.
        </p>
      </div>

      {loading ? (
        <LoadingSpinner text="Generating financial reports..." />
      ) : (
        <div className="glass-panel overflow-hidden">
          <div className="overflow-x-auto">
            <table className="data-table">
              <thead>
                <tr>
                  <th>Period</th>
                  <th className="text-right">Revenue (₹)</th>
                  <th className="text-right">Expenses (₹)</th>
                  <th className="text-right">Taxes Collected/Paid (₹)</th>
                  <th className="text-right">Net Profit (₹)</th>
                  <th className="text-right">Margin (%)</th>
                </tr>
              </thead>
              <tbody>
                {pnlData.map((row, idx) => {
                  const isPositive = (row.profit || 0) >= 0;
                  return (
                    <tr key={idx} className="transition-colors">
                      <td className="font-bold font-mono text-xs">{row.month}</td>
                      <td className="text-right font-mono text-xs text-emerald-400 font-semibold">
                        ₹{Number(row.revenue || 0).toLocaleString("en-IN")}
                      </td>
                      <td className="text-right font-mono text-xs text-rose-400 font-semibold">
                        ₹{Number(row.expenses || 0).toLocaleString("en-IN")}
                      </td>
                      <td className="text-right font-mono text-xs text-slate-400">
                        ₹{Number(row.tax_total || 0).toLocaleString("en-IN")}
                      </td>
                      <td
                        className={`text-right font-mono text-xs font-bold ${
                          isPositive ? "text-indigo-400" : "text-amber-400"
                        }`}
                      >
                        ₹{Number(row.profit || 0).toLocaleString("en-IN")}
                      </td>
                      <td className="text-right font-mono text-xs">
                        <span
                          className={`badge ${
                            isPositive ? "badge-success" : "badge-warning"
                          }`}
                        >
                          {Number(row.margin || 0).toFixed(1)}%
                        </span>
                      </td>
                    </tr>
                  );
                })}
              </tbody>
            </table>
          </div>
        </div>
      )}
    </div>
  );
}
