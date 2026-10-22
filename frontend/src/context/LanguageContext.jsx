import React, { createContext, useContext, useState, useEffect } from "react";
import { en } from "../i18n/en";
import { hi } from "../i18n/hi";

const LanguageContext = createContext();

const dictionaries = { en, hi };

export function LanguageProvider({ children }) {
  const [language, setLanguage] = useState(() => {
    return localStorage.getItem("finpilot_language") || "en";
  });

  useEffect(() => {
    localStorage.setItem("finpilot_language", language);
  }, [language]);

  const t = (key) => {
    const dict = dictionaries[language] || en;
    return dict[key] || en[key] || key;
  };

  const toggleLanguage = () => {
    setLanguage((prev) => (prev === "en" ? "hi" : "en"));
  };

  return (
    <LanguageContext.Provider value={{ language, setLanguage, toggleLanguage, t }}>
      {children}
    </LanguageContext.Provider>
  );
}

export function useLanguage() {
  const ctx = useContext(LanguageContext);
  if (!ctx) throw new Error("useLanguage must be used within LanguageProvider");
  return ctx;
}
