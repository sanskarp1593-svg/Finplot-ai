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
  Languages,
  Sun,
  Moon,
} from "lucide-react";
import { useLanguage } from "../../context/LanguageContext";
import { useTheme } from "../../context/ThemeContext";

export function Sidebar({ currentTab, setCurrentTab }) {
  const { t, language, toggleLanguage } = useLanguage();
  const { isDark, toggleTheme } = useTheme();

  const navItems = [
    { id: "dashboard",    label: t("navDashboard"),    icon: LayoutDashboard },
    { id: "assistant",    label: t("navAssistant"),    icon: Sparkles, badge: "AI" },
    { id: "transactions", label: t("navTransactions"), icon: ArrowLeftRight },
    { id: "invoices",     label: t("navInvoices"),     icon: FileText },
    { id: "reports",      label: t("navReports"),      icon: BarChart3 },
    { id: "knowledge",    label: t("navKnowledge"),    icon: BookOpen },
    { id: "settings",     label: t("navSettings"),     icon: Settings },
  ];

  return (
    <aside className="w-64 flex-shrink-0 flex flex-col justify-between h-screen bg-slate-900 border-r border-slate-800 select-none">
      {/* ── Brand Header ─────────────────────────────────── */}
      <div>
        <div className="p-6 flex items-center gap-3 border-b border-slate-800">
          <div className="w-9 h-9 rounded-xl flex items-center justify-center bg-emerald-500/10 text-emerald-400 border border-emerald-500/20 shadow-sm shrink-0">
            <Sparkles className="w-4 h-4" />
          </div>
          <div>
            <h1 className="font-bold text-base tracking-tight text-white flex items-center gap-1.5">
              FinPilot <span className="text-emerald-400 font-semibold text-xs px-1.5 py-0.5 rounded bg-emerald-500/10 border border-emerald-500/20">AI</span>
            </h1>
            <p className="text-[11px] font-medium text-slate-400">
              Enterprise Cashflow Copilot
            </p>
          </div>
        </div>

        {/* ── Navigation ───────────────────────────────────── */}
        <nav className="p-3 space-y-1">
          {navItems.map((item) => {
            const Icon = item.icon;
            const isActive = currentTab === item.id;
            return (
              <button
                key={item.id}
                onClick={() => setCurrentTab(item.id)}
                className={`w-full flex items-center justify-between px-3.5 py-2.5 text-sm font-medium transition-colors ${
                  isActive
                    ? "bg-slate-800 text-white border-l-2 border-emerald-500 rounded-r-lg"
                    : "text-slate-400 hover:text-slate-200 hover:bg-slate-800/50 rounded-lg"
                }`}
              >
                <div className="flex items-center gap-3">
                  <Icon
                    className={`w-4 h-4 shrink-0 transition-colors ${
                      isActive ? "text-emerald-400" : "text-slate-400"
                    }`}
                  />
                  <span>{item.label}</span>
                </div>

                {item.badge && (
                  <span className="text-[10px] font-semibold px-1.5 py-0.5 rounded bg-emerald-500/10 text-emerald-400 border border-emerald-500/20">
                    {item.badge}
                  </span>
                )}
              </button>
            );
          })}
        </nav>
      </div>

      {/* ── Footer Controls & CA Verified ─────────────────── */}
      <div className="p-3 space-y-2">
        <div className="flex items-center justify-between px-2.5 py-1.5 rounded-lg bg-slate-950/60 border border-slate-800/80 text-xs">
          <button
            onClick={toggleLanguage}
            className="flex items-center gap-1.5 text-slate-400 hover:text-white transition-colors font-medium"
            title="Toggle Language / भाषा बदलें"
          >
            <Languages className="w-3.5 h-3.5 text-emerald-400" />
            <span>{language === "en" ? "English" : "हिन्दी"}</span>
          </button>
          <button
            onClick={toggleTheme}
            className="p-1 rounded-md text-slate-400 hover:text-white hover:bg-slate-800 transition-colors"
            title={isDark ? "Switch to Light Mode" : "Switch to Dark Mode"}
          >
            {isDark ? <Sun className="w-3.5 h-3.5 text-amber-400" /> : <Moon className="w-3.5 h-3.5 text-indigo-400" />}
          </button>
        </div>

        <div className="p-3 rounded-xl bg-slate-950/70 border border-slate-800/80">
          <div className="flex items-start gap-2.5">
            <ShieldAlert className="w-4 h-4 shrink-0 mt-0.5 text-emerald-400" />
            <div className="text-xs">
              <p className="font-semibold text-slate-200">CA Verified Mode</p>
              <p className="mt-0.5 text-slate-400 leading-relaxed text-[11px]">
                Tax calculations follow GST & IT act rules with source citations.
              </p>
            </div>
          </div>
        </div>
      </div>
    </aside>
  );
}
