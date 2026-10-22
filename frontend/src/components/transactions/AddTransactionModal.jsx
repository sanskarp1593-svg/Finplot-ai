import React, { useState } from "react";
import { Modal } from "../shared/Modal";
import { createTransaction } from "../../api/transactions";
import { useToast } from "../../context/ToastContext";

const EXPENSE_CATEGORIES = [
  "Inventory / Stock",
  "Rent & Utilities",
  "Salaries & Wages",
  "Travel & Transport",
  "Marketing & Ads",
  "Office Supplies",
  "Repairs & Maintenance",
  "Insurance",
  "Taxes & Fees",
  "Miscellaneous",
];

const REVENUE_CATEGORIES = [
  "Product Sales",
  "Service Revenue",
  "Other Income",
];

export function AddTransactionModal({ isOpen, onClose, onCreated }) {
  const { addToast } = useToast();
  const [formData, setFormData] = useState({
    date: new Date().toISOString().split("T")[0],
    type: "expense",
    category: "Inventory / Stock",
    amount: "",
    tax_amount: "0",
    vendor: "",
    description: "",
  });
  const [submitting, setSubmitting] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!formData.amount || Number(formData.amount) <= 0) {
      addToast("Please enter a valid amount", "error");
      return;
    }

    setSubmitting(true);
    try {
      await createTransaction({
        ...formData,
        amount: parseFloat(formData.amount),
        tax_amount: parseFloat(formData.tax_amount || "0"),
        source: "manual",
      });
      addToast("Transaction added successfully", "success");
      onCreated();
      onClose();
    } catch (err) {
      addToast(err.message || "Failed to create transaction", "error");
    } finally {
      setSubmitting(false);
    }
  };

  const categories = formData.type === "revenue" ? REVENUE_CATEGORIES : EXPENSE_CATEGORIES;

  return (
    <Modal isOpen={isOpen} onClose={onClose} title="Add New Transaction">
      <form onSubmit={handleSubmit} className="space-y-4 text-xs">
        {/* Type Toggle */}
        <div className="grid grid-cols-2 gap-2 p-1 rounded-xl bg-slate-800/40 border border-subtle">
          <button
            type="button"
            onClick={() => setFormData({ ...formData, type: "expense", category: EXPENSE_CATEGORIES[0] })}
            className={`py-2 rounded-lg font-semibold transition-all ${
              formData.type === "expense"
                ? "bg-rose-500 text-white shadow-sm"
                : "text-slate-400 hover:text-slate-200"
            }`}
          >
            Expense
          </button>
          <button
            type="button"
            onClick={() => setFormData({ ...formData, type: "revenue", category: REVENUE_CATEGORIES[0] })}
            className={`py-2 rounded-lg font-semibold transition-all ${
              formData.type === "revenue"
                ? "bg-emerald-500 text-white shadow-sm"
                : "text-slate-400 hover:text-slate-200"
            }`}
          >
            Revenue
          </button>
        </div>

        {/* Date & Category */}
        <div className="grid grid-cols-1 sm:grid-cols-2 gap-3">
          <div>
            <label className="block font-medium mb-1" style={{ color: "var(--text-secondary)" }}>
              Date
            </label>
            <input
              type="date"
              required
              value={formData.date}
              onChange={(e) => setFormData({ ...formData, date: e.target.value })}
              className="input-field"
            />
          </div>

          <div>
            <label className="block font-medium mb-1" style={{ color: "var(--text-secondary)" }}>
              Category
            </label>
            <select
              value={formData.category}
              onChange={(e) => setFormData({ ...formData, category: e.target.value })}
              className="input-field"
            >
              {categories.map((c) => (
                <option key={c} value={c}>
                  {c}
                </option>
              ))}
            </select>
          </div>
        </div>

        {/* Amount & Tax */}
        <div className="grid grid-cols-1 sm:grid-cols-2 gap-3">
          <div>
            <label className="block font-medium mb-1" style={{ color: "var(--text-secondary)" }}>
              Amount (₹)
            </label>
            <input
              type="number"
              step="0.01"
              required
              placeholder="0.00"
              value={formData.amount}
              onChange={(e) => setFormData({ ...formData, amount: e.target.value })}
              className="input-field font-semibold"
            />
          </div>

          <div>
            <label className="block font-medium mb-1" style={{ color: "var(--text-secondary)" }}>
              Tax / GST Amount (₹)
            </label>
            <input
              type="number"
              step="0.01"
              placeholder="0.00"
              value={formData.tax_amount}
              onChange={(e) => setFormData({ ...formData, tax_amount: e.target.value })}
              className="input-field"
            />
          </div>
        </div>

        {/* Vendor */}
        <div>
          <label className="block font-medium mb-1" style={{ color: "var(--text-secondary)" }}>
            Vendor / Customer
          </label>
          <input
            type="text"
            placeholder="e.g. Aggarwal Traders"
            value={formData.vendor}
            onChange={(e) => setFormData({ ...formData, vendor: e.target.value })}
            className="input-field"
          />
        </div>

        {/* Description */}
        <div>
          <label className="block font-medium mb-1" style={{ color: "var(--text-secondary)" }}>
            Description / Item Notes
          </label>
          <textarea
            rows="2"
            placeholder="e.g. 50kg basmati rice + 20kg toor dal"
            value={formData.description}
            onChange={(e) => setFormData({ ...formData, description: e.target.value })}
            className="input-field"
          />
        </div>

        {/* Actions */}
        <div className="flex items-center justify-end gap-2 pt-3 border-t border-subtle">
          <button type="button" onClick={onClose} className="btn btn-secondary">
            Cancel
          </button>
          <button type="submit" disabled={submitting} className="btn btn-primary">
            {submitting ? "Saving..." : "Add Transaction"}
          </button>
        </div>
      </form>
    </Modal>
  );
}
