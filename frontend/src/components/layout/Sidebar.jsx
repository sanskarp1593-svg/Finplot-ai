import React from "react";
import {
  LayoutDashboard,
  ArrowLeftRight,
  FileText,
  Sparkles,
  BarChart3,
  BookOpen,
  Settings,
  ShieldAlert,
} from "lucide-react";
import { useLanguage } from "../../context/LanguageContext";

export function Sidebar({ currentTab, setCurrentTab }) {
  const { t } = useLanguage();

  const navItems = [
    { id: "dashboard", label: t("navDashboard"), icon: LayoutDashboard },
    { id: "assistant", label: t("navAssistant"), icon: Sparkles, badge: "AI" },
    { id: "transactions", label: t("navTransactions"), icon: ArrowLeftRight },
    { id: "invoices", label: t("navInvoices"), icon: FileText },
    { id: "reports", label: t("navReports"), icon: BarChart3 },
    { id: "knowledge", label: t("navKnowledge"), icon: BookOpen },
    { id: "settings", label: t("navSettings"), icon: Settings },
  ];

  return (
    <aside className="w-64 border-r border-subtle flex flex-col justify-between shrink-0 h-screen sticky top-0" style={{ background: "var(--bg-secondary)" }}>
      {/* Brand Header */}
      <div>
        <div className="p-6 border-b border-subtle flex items-center gap-3">
          <div className="w-10 h-10 rounded-xl bg-gradient-to-tr from-indigo-600 via-indigo-500 to-violet-500 flex items-center justify-center text-white shadow-lg shadow-indigo-500/25">
            <Sparkles className="w-5 h-5" />
          </div>
          <div>
            <h1 className="font-extrabold text-lg tracking-tight" style={{ fontFamily: "var(--font-display)", color: "var(--text-primary)" }}>
              FinPilot <span style={{ color: "var(--primary)" }}>AI</span>
            </h1>
            <p className="text-xs font-medium" style={{ color: "var(--text-muted)" }}>
              Decision Copilot
            </p>
          </div>
        </div>

        {/* Navigation Links */}
        <nav className="p-3 space-y-1">
          {navItems.map((item) => {
            const Icon = item.icon;
            const isActive = currentTab === item.id;
            return (
              <button
                key={item.id}
                onClick={() => setCurrentTab(item.id)}
                className={`w-full flex items-center justify-between px-3.5 py-2.5 rounded-xl text-sm font-medium transition-all ${
                  isActive
                    ? "bg-indigo-600/10 text-indigo-400 font-semibold border border-indigo-500/20"
                    : "hover:bg-slate-800/40 text-slate-400 hover:text-slate-200"
                }`}
                style={isActive ? { background: "var(--primary-subtle)", color: "var(--primary)" } : { color: "var(--text-secondary)" }}
              >
                <div className="flex items-center gap-3">
                  <Icon className={`w-4 h-4 ${isActive ? "text-indigo-500" : ""}`} />
                  <span>{item.label}</span>
                </div>
                {item.badge && (
                  <span className="text-[10px] font-bold px-1.5 py-0.5 rounded-md bg-indigo-500/20 text-indigo-400 border border-indigo-500/30">
                    {item.badge}
                  </span>
                )}
              </button>
            );
          })}
        </nav>
      </div>

      {/* Compliance / CA Footer Callout */}
      <div className="p-4 m-3 rounded-xl border border-subtle" style={{ background: "var(--bg-tertiary)" }}>
        <div className="flex items-start gap-2.5">
          <ShieldAlert className="w-4 h-4 text-amber-500 shrink-0 mt-0.5" />
          <div className="text-xs">
            <p className="font-semibold text-amber-500">CA Verified Mode</p>
            <p className="text-[11px] mt-0.5 leading-relaxed" style={{ color: "var(--text-muted)" }}>
              Tax calculations follow GST & IT act rules with source citations.
            </p>
          </div>
        </div>
      </div>
    </aside>
  );
}
