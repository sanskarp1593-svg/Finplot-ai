import React, { useState } from "react";
import { ThemeProvider } from "./context/ThemeContext";
import { LanguageProvider } from "./context/LanguageContext";
import { ToastProvider } from "./context/ToastContext";
import { ErrorBoundary } from "./components/shared/ErrorBoundary";
import { Sidebar } from "./components/layout/Sidebar";
import { TopBar } from "./components/layout/TopBar";
import { DashboardPage } from "./components/dashboard/DashboardPage";
import { AssistantPage } from "./components/assistant/AssistantPage";
import { TransactionsPage } from "./components/transactions/TransactionsPage";
import { InvoicePage } from "./components/invoices/InvoicePage";
import { ReportsPage } from "./components/reports/ReportsPage";
import { KnowledgePage } from "./components/knowledge/KnowledgePage";
import { SettingsPage } from "./components/settings/SettingsPage";

function AppContent() {
  const [currentTab, setCurrentTab] = useState("dashboard");

  const renderCurrentPage = () => {
    switch (currentTab) {
      case "dashboard":     return <DashboardPage />;
      case "assistant":     return <AssistantPage />;
      case "transactions":  return <TransactionsPage />;
      case "invoices":      return <InvoicePage />;
      case "reports":       return <ReportsPage />;
      case "knowledge":     return <KnowledgePage />;
      case "settings":      return <SettingsPage />;
      default:              return <DashboardPage />;
    }
  };

  return (
    <div className="flex h-screen bg-slate-950 text-slate-50 overflow-hidden">
      <Sidebar currentTab={currentTab} setCurrentTab={setCurrentTab} />
      <main className="flex-1 overflow-y-auto p-6 md:p-8 space-y-6">
        <ErrorBoundary key={currentTab}>
          {renderCurrentPage()}
        </ErrorBoundary>
      </main>
    </div>
  );
}

export function App() {
  return (
    <ThemeProvider>
      <LanguageProvider>
        <ToastProvider>
          {/* Top-level boundary catches provider/layout crashes */}
          <ErrorBoundary>
            <AppContent />
          </ErrorBoundary>
        </ToastProvider>
      </LanguageProvider>
    </ThemeProvider>
  );
}

export default App;
