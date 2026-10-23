import React, { useEffect, useState } from "react";
import { Moon, Sun, Languages, Store } from "lucide-react";
import { useLanguage } from "../../context/LanguageContext";
import { useTheme } from "../../context/ThemeContext";

export function TopBar({ businessName = "Kumar General Store" }) {
  const { language, toggleLanguage } = useLanguage();
  const { isDark, toggleTheme } = useTheme();
  const [isHealthy, setIsHealthy] = useState(true);

  useEffect(() => {
    fetch("/api/health")
      .then((res) => res.json())
      .then((data) => setIsHealthy(data.status === "healthy" || data.status === "ok"))
      .catch(() => setIsHealthy(false));
  }, []);

  return (
    <header className="h-16 px-6 sm:px-8 border-b border-slate-800 bg-slate-900/95 backdrop-blur flex items-center justify-between shrink-0 sticky top-0 z-30">
      {/* Left: Active Business Profile */}
      <div className="flex items-center gap-3">
        <div className="w-8 h-8 rounded-lg flex items-center justify-center bg-slate-800 border border-slate-700/60 text-slate-200">
          <Store className="w-4 h-4 text-emerald-400" />
        </div>
        <div>
          <span className="text-sm font-semibold text-white">
            {businessName}
          </span>
          <div className="flex items-center gap-1.5">
            <span
              className={`w-1.5 h-1.5 rounded-full ${
                isHealthy ? "bg-emerald-400 animate-pulse" : "bg-rose-500"
              }`}
            />
            <span className="text-[11px] text-slate-400">
              {isHealthy ? "API Connected" : "API Offline"}
            </span>
          </div>
        </div>
      </div>

      {/* Right: Actions */}
      <div className="flex items-center gap-2">
        {/* Language Toggle */}
        <button
          onClick={toggleLanguage}
          className="px-3 py-1.5 rounded-lg bg-slate-800 hover:bg-slate-700/80 border border-slate-700/60 text-xs font-semibold text-slate-300 hover:text-white transition-colors flex items-center gap-1.5"
          title="Switch Language / भाषा बदलें"
        >
          <Languages className="w-3.5 h-3.5 text-emerald-400" />
          <span>{language === "en" ? "EN" : "हिन्दी"}</span>
        </button>

        {/* Theme Toggle */}
        <button
          onClick={toggleTheme}
          className="p-2 rounded-lg bg-slate-800 hover:bg-slate-700/80 border border-slate-700/60 text-slate-400 hover:text-white transition-colors"
          title={isDark ? "Switch to Light Mode" : "Switch to Dark Mode"}
        >
          {isDark ? <Sun className="w-4 h-4 text-amber-400" /> : <Moon className="w-4 h-4 text-indigo-400" />}
        </button>
      </div>
    </header>
  );
}
