import React, { useState, useEffect } from "react";
import { Settings, Save, CheckCircle2, ShieldAlert } from "lucide-react";
import { getSettings, updateSettings, updateBudgets } from "../../api/settings";
import { LoadingSpinner } from "../shared/LoadingSpinner";
import { useToast } from "../../context/ToastContext";
import { useLanguage } from "../../context/LanguageContext";

export function SettingsPage() {
  const { t } = useLanguage();
  const { addToast } = useToast();

  const [loading, setLoading] = useState(true);
  const [saving, setSaving] = useState(false);
  const [profile, setProfile] = useState({
    name: "",
    industry: "",
    language: "en",
  });
  const [budgets, setBudgets] = useState([]);

  useEffect(() => {
    async function load() {
      setLoading(true);
      try {
        const res = await getSettings();
        setProfile({
          name: res.name || "",
          industry: res.industry || "",
          language: res.language || "en",
        });
        setBudgets(res.budgets || []);
      } catch (err) {
        addToast(err.message || "Failed to load settings", "error");
      } finally {
        setLoading(false);
      }
    }
    load();
  }, []);

  const handleSaveProfile = async (e) => {
    e.preventDefault();
    setSaving(true);
    try {
      await updateSettings(profile);
      await updateBudgets(budgets);
      addToast(t("savedSuccess"), "success");
    } catch (err) {
      addToast(err.message || "Failed to save settings", "error");
    } finally {
      setSaving(false);
    }
  };

  const handleBudgetChange = (category, value) => {
    setBudgets((prev) =>
      prev.map((b) =>
        b.category === category ? { ...b, monthly_limit: parseFloat(value) || 0 } : b
      )
    );
  };

  return (
    <div className="p-6 max-w-4xl mx-auto space-y-6 animate-fade-in">
      {/* Header */}
      <div>
        <h2 className="text-xl font-bold tracking-tight" style={{ fontFamily: "var(--font-display)", color: "var(--text-primary)" }}>
          {t("navSettings")}
        </h2>
        <p className="text-xs" style={{ color: "var(--text-muted)" }}>
          Configure business profile parameters and monthly expenditure thresholds.
        </p>
      </div>

      {loading ? (
        <LoadingSpinner text="Loading business settings..." />
      ) : (
        <form onSubmit={handleSaveProfile} className="space-y-6">
          {/* Business Profile */}
          <div className="glass-panel p-6 space-y-4">
            <h3 className="font-bold text-sm" style={{ color: "var(--text-primary)" }}>
              {t("businessProfile")}
            </h3>

            <div className="grid grid-cols-1 sm:grid-cols-2 gap-4 text-xs">
              <div>
                <label className="block font-medium mb-1.5" style={{ color: "var(--text-secondary)" }}>
                  {t("businessName")}
                </label>
                <input
                  type="text"
                  required
                  value={profile.name}
                  onChange={(e) => setProfile({ ...profile, name: e.target.value })}
                  className="input-field font-semibold"
                />
              </div>

              <div>
                <label className="block font-medium mb-1.5" style={{ color: "var(--text-secondary)" }}>
                  {t("industry")}
                </label>
                <input
                  type="text"
                  required
                  value={profile.industry}
                  onChange={(e) => setProfile({ ...profile, industry: e.target.value })}
                  className="input-field"
                />
              </div>
            </div>
          </div>

          {/* Monthly Category Budgets */}
          <div className="glass-panel p-6 space-y-4">
            <div className="flex items-center justify-between">
              <div>
                <h3 className="font-bold text-sm" style={{ color: "var(--text-primary)" }}>
                  {t("budgetSettings")}
                </h3>
                <p className="text-xs mt-0.5" style={{ color: "var(--text-muted)" }}>
                  Budget thresholds used by BudgetAgent to calculate burn rate and over-budget alerts.
                </p>
              </div>
            </div>

            <div className="grid grid-cols-1 sm:grid-cols-2 gap-3 text-xs pt-2">
              {budgets.map((b) => (
                <div
                  key={b.category}
                  className="p-3 rounded-xl border border-subtle bg-slate-900/40 flex items-center justify-between gap-3"
                >
                  <span className="font-medium truncate text-slate-300">{b.category}</span>
                  <div className="flex items-center gap-1.5 shrink-0">
                    <span className="text-slate-500 font-mono">₹</span>
                    <input
                      type="number"
                      step="500"
                      value={b.monthly_limit}
                      onChange={(e) => handleBudgetChange(b.category, e.target.value)}
                      className="input-field w-28 py-1 px-2 text-right font-mono font-semibold"
                    />
                  </div>
                </div>
              ))}
            </div>
          </div>

          {/* Save Button */}
          <div className="flex justify-end">
            <button
              type="submit"
              disabled={saving}
              className="btn btn-primary px-6 py-2.5 text-xs font-semibold"
            >
              <Save className="w-4 h-4" />
              <span>{saving ? "Saving Changes..." : t("saveChanges")}</span>
            </button>
          </div>
        </form>
      )}
    </div>
  );
}
