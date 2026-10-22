import React, { useState } from "react";
import { ThemeProvider } from "./context/ThemeContext";
import { LanguageProvider } from "./context/LanguageContext";
import { ToastProvider } from "./context/ToastContext";
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
      case "dashboard":
        return <DashboardPage />;
      case "assistant":
        return <AssistantPage />;
      case "transactions":
        return <TransactionsPage />;
      case "invoices":
        return <InvoicePage />;
      case "reports":
        return <ReportsPage />;
      case "knowledge":
        return <KnowledgePage />;
      case "settings":
        return <SettingsPage />;
      default:
        return <DashboardPage />;
    }
  };

  return (
    <div className="app-container">
      <Sidebar currentTab={currentTab} setCurrentTab={setCurrentTab} />
      <div className="main-content">
        <TopBar />
        <main className="flex-1">{renderCurrentPage()}</main>
      </div>
    </div>
  );
}

export function App() {
  return (
    <ThemeProvider>
      <LanguageProvider>
        <ToastProvider>
          <AppContent />
        </ToastProvider>
      </LanguageProvider>
    </ThemeProvider>
  );
}

export default App;
