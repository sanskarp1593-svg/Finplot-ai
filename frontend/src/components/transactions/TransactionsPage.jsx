import React, { useState, useEffect } from "react";
import {
  Plus,
  Upload,
  Download,
  Search,
  Filter,
  Trash2,
  Calendar,
  ArrowUpDown,
} from "lucide-react";
import { getTransactions, deleteTransaction, getExportCSVUrl } from "../../api/transactions";
import { AddTransactionModal } from "./AddTransactionModal";
import { CSVImportModal } from "./CSVImportModal";
import { LoadingSpinner } from "../shared/LoadingSpinner";
import { EmptyState } from "../shared/EmptyState";
import { useToast } from "../../context/ToastContext";
import { useLanguage } from "../../context/LanguageContext";

export function TransactionsPage() {
  const { t } = useLanguage();
  const { addToast } = useToast();

  const [transactions, setTransactions] = useState([]);
  const [loading, setLoading] = useState(true);
  const [totalCount, setTotalCount] = useState(0);

  // Filters & Pagination
  const [search, setSearch] = useState("");
  const [typeFilter, setTypeFilter] = useState("");
  const [page, setPage] = useState(1);
  const limit = 15;

  // Modals
  const [isAddOpen, setIsAddOpen] = useState(false);
  const [isImportOpen, setIsImportOpen] = useState(false);

  const loadData = async () => {
    setLoading(true);
    try {
      const res = await getTransactions({
        search,
        type: typeFilter,
        page,
        limit,
      });
      setTransactions(res.items || []);
      setTotalCount(res.total || 0);
    } catch (err) {
      addToast(err.message || "Failed to load transactions", "error");
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadData();
  }, [typeFilter, page]);

  const handleSearchSubmit = (e) => {
    e.preventDefault();
    setPage(1);
    loadData();
  };

  const handleDelete = async (id) => {
    if (!window.confirm(t("deleteConfirm"))) return;
    try {
      await deleteTransaction(id);
      addToast("Transaction deleted", "info");
      loadData();
    } catch (err) {
      addToast(err.message || "Failed to delete", "error");
    }
  };

  const totalPages = Math.ceil(totalCount / limit) || 1;

  return (
    <div className="p-6 max-w-7xl mx-auto space-y-6 animate-fade-in">
      {/* Header & Main Actions */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
        <div>
          <h2 className="text-xl font-bold tracking-tight" style={{ fontFamily: "var(--font-display)", color: "var(--text-primary)" }}>
            {t("allTransactions")}
          </h2>
          <p className="text-xs" style={{ color: "var(--text-muted)" }}>
            General ledger transactions across manual, CSV, and OCR-extracted invoice entries.
          </p>
        </div>

        <div className="flex items-center gap-2 flex-wrap">
          <button
            onClick={() => setIsImportOpen(true)}
            className="btn btn-secondary text-xs"
          >
            <Upload className="w-3.5 h-3.5 text-indigo-400" />
            <span>{t("importCSV")}</span>
          </button>

          <a
            href={getExportCSVUrl({ search, type: typeFilter })}
            target="_blank"
            rel="noopener noreferrer"
            className="btn btn-secondary text-xs"
          >
            <Download className="w-3.5 h-3.5 text-emerald-400" />
            <span>{t("exportCSV")}</span>
          </a>

          <button
            onClick={() => setIsAddOpen(true)}
            className="btn btn-primary text-xs"
          >
            <Plus className="w-3.5 h-3.5" />
            <span>{t("addTransaction")}</span>
          </button>
        </div>
      </div>

      {/* Filter Toolbar */}
      <div className="glass-panel p-4 flex flex-col sm:flex-row sm:items-center justify-between gap-3">
        {/* Search */}
        <form onSubmit={handleSearchSubmit} className="relative flex-1 max-w-md">
          <Search className="w-4 h-4 text-slate-400 absolute left-3 top-1/2 -translate-y-1/2" />
          <input
            type="text"
            placeholder={t("searchPlaceholder")}
            value={search}
            onChange={(e) => setSearch(e.target.value)}
            className="input-field pl-9 py-2 text-xs"
          />
        </form>

        {/* Type Toggle Tabs */}
        <div className="flex items-center gap-1.5 p-1 rounded-xl bg-slate-900/60 border border-subtle self-start sm:self-auto text-xs">
          <button
            onClick={() => { setTypeFilter(""); setPage(1); }}
            className={`px-3 py-1.5 rounded-lg font-medium transition-all ${
              typeFilter === ""
                ? "bg-indigo-600 text-white shadow-sm"
                : "text-slate-400 hover:text-slate-200"
            }`}
          >
            All
          </button>
          <button
            onClick={() => { setTypeFilter("expense"); setPage(1); }}
            className={`px-3 py-1.5 rounded-lg font-medium transition-all ${
              typeFilter === "expense"
                ? "bg-rose-500 text-white shadow-sm"
                : "text-slate-400 hover:text-slate-200"
            }`}
          >
            Expenses
          </button>
          <button
            onClick={() => { setTypeFilter("revenue"); setPage(1); }}
            className={`px-3 py-1.5 rounded-lg font-medium transition-all ${
              typeFilter === "revenue"
                ? "bg-emerald-500 text-white shadow-sm"
                : "text-slate-400 hover:text-slate-200"
            }`}
          >
            Revenue
          </button>
        </div>
      </div>

      {/* Transactions Data Table */}
      <div className="glass-panel overflow-hidden">
        {loading ? (
          <LoadingSpinner text="Loading transactions ledger..." />
        ) : transactions.length === 0 ? (
          <EmptyState
            title="No transactions found"
            description="Try modifying search keywords or add a new transaction."
            action={
              <button onClick={() => setIsAddOpen(true)} className="btn btn-primary text-xs">
                <Plus className="w-3.5 h-3.5" /> Add Transaction
              </button>
            }
          />
        ) : (
          <div className="overflow-x-auto">
            <table className="data-table">
              <thead>
                <tr>
                  <th>{t("date")}</th>
                  <th>{t("type")}</th>
                  <th>{t("category")}</th>
                  <th>{t("vendor")}</th>
                  <th>{t("description")}</th>
                  <th className="text-right">{t("tax")}</th>
                  <th className="text-right">{t("amount")}</th>
                  <th className="text-center">{t("actions")}</th>
                </tr>
              </thead>
              <tbody>
                {transactions.map((tx) => (
                  <tr key={tx.id} className="transition-colors">
                    <td className="font-mono text-xs whitespace-nowrap" style={{ color: "var(--text-secondary)" }}>
                      {tx.date}
                    </td>
                    <td>
                      <span
                        className={`badge ${
                          tx.type === "revenue" ? "badge-success" : "badge-danger"
                        }`}
                      >
                        {tx.type === "revenue" ? t("revenue") : t("expense")}
                      </span>
                    </td>
                    <td className="font-medium">{tx.category}</td>
                    <td className="text-xs" style={{ color: "var(--text-secondary)" }}>
                      {tx.vendor || "—"}
                    </td>
                    <td className="text-xs max-w-xs truncate" style={{ color: "var(--text-muted)" }}>
                      {tx.description || "—"}
                    </td>
                    <td className="text-right font-mono text-xs" style={{ color: "var(--text-muted)" }}>
                      ₹{Number(tx.tax_amount || 0).toLocaleString("en-IN")}
                    </td>
                    <td
                      className={`text-right font-bold font-mono text-xs ${
                        tx.type === "revenue" ? "text-emerald-400" : "text-rose-400"
                      }`}
                    >
                      {tx.type === "revenue" ? "+" : "-"}₹{Number(tx.amount).toLocaleString("en-IN")}
                    </td>
                    <td className="text-center">
                      <button
                        onClick={() => handleDelete(tx.id)}
                        className="p-1 rounded-lg text-slate-500 hover:text-rose-400 hover:bg-rose-500/10 transition-colors"
                        title="Delete record"
                      >
                        <Trash2 className="w-3.5 h-3.5" />
                      </button>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}

        {/* Pagination Footer */}
        {totalCount > limit && (
          <div className="p-4 border-t border-subtle flex items-center justify-between text-xs" style={{ color: "var(--text-muted)" }}>
            <span>
              Showing {transactions.length} of {totalCount} records
            </span>
            <div className="flex items-center gap-1.5">
              <button
                disabled={page <= 1}
                onClick={() => setPage((p) => Math.max(1, p - 1))}
                className="btn btn-secondary px-2.5 py-1 text-xs disabled:opacity-40"
              >
                Previous
              </button>
              <span className="px-2 font-semibold text-slate-300">
                Page {page} of {totalPages}
              </span>
              <button
                disabled={page >= totalPages}
                onClick={() => setPage((p) => p + 1)}
                className="btn btn-secondary px-2.5 py-1 text-xs disabled:opacity-40"
              >
                Next
              </button>
            </div>
          </div>
        )}
      </div>

      {/* Modals */}
      <AddTransactionModal
        isOpen={isAddOpen}
        onClose={() => setIsAddOpen(false)}
        onCreated={loadData}
      />
      <CSVImportModal
        isOpen={isImportOpen}
        onClose={() => setIsImportOpen(false)}
        onImported={loadData}
      />
    </div>
  );
}
