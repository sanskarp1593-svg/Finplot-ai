import React, { useState, useEffect, useRef } from "react";
import { Send, Sparkles, MessageSquare, ArrowRight, CornerDownLeft } from "lucide-react";
import { queryAssistant, getAssistantHistory } from "../../api/assistant";
import { ChatMessage } from "./ChatMessage";
import { useLanguage } from "../../context/LanguageContext";

export function AssistantPage() {
  const { language, t } = useLanguage();
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState("");
  const [loading, setLoading] = useState(false);
  const messagesEndRef = useRef(null);

  const suggestedPrompts = [
    t("prompt1"),
    t("prompt2"),
    t("prompt3"),
    t("prompt4"),
  ];

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages, loading]);

  const handleSend = async (textToSend) => {
    const q = (textToSend || input).trim();
    if (!q || loading) return;

    const userMsg = {
      role: "user",
      content: q,
    };

    setMessages((prev) => [...prev, userMsg]);
    setInput("");
    setLoading(true);

    try {
      const res = await queryAssistant(q, language);
      const assistantMsg = {
        role: "assistant",
        content: res.answer,
        agents_used: res.agents_used,
        traces: res.traces,
        charts: res.charts,
        sources: res.sources,
        needs_ca_review: res.needs_ca_review,
      };
      setMessages((prev) => [...prev, assistantMsg]);
    } catch (err) {
      setMessages((prev) => [
        ...prev,
        {
          role: "assistant",
          content: `⚠️ Failed to get answer: ${err.message || "Backend error"}.`,
        },
      ]);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="flex flex-col h-[calc(100vh-4rem)] max-w-5xl mx-auto p-4 sm:p-6 animate-fade-in">
      {/* Header */}
      <div className="flex items-center justify-between pb-4 border-b border-subtle shrink-0">
        <div className="flex items-center gap-3">
          <div className="w-10 h-10 rounded-xl bg-indigo-500/10 border border-indigo-500/30 flex items-center justify-center text-indigo-400">
            <Sparkles className="w-5 h-5" />
          </div>
          <div>
            <h2 className="text-base font-bold tracking-tight" style={{ fontFamily: "var(--font-display)", color: "var(--text-primary)" }}>
              {t("appName")}
            </h2>
            <p className="text-xs" style={{ color: "var(--text-muted)" }}>
              Multi-Agent Decision Support (English / हिन्दी)
            </p>
          </div>
        </div>
      </div>

      {/* Messages Scroll Area */}
      <div className="flex-1 overflow-y-auto py-4 space-y-4 pr-1">
        {messages.length === 0 ? (
          <div className="py-12 px-4 text-center max-w-xl mx-auto space-y-6">
            <div className="w-14 h-14 rounded-2xl bg-indigo-500/10 border border-indigo-500/20 flex items-center justify-center text-indigo-400 mx-auto shadow-inner">
              <MessageSquare className="w-7 h-7" />
            </div>
            <div>
              <h3 className="text-lg font-bold" style={{ fontFamily: "var(--font-display)", color: "var(--text-primary)" }}>
                {t("appSubtitle")}
              </h3>
              <p className="text-xs mt-1" style={{ color: "var(--text-muted)" }}>
                Ask financial questions, budget health, GST compliance rules, or compare item rates.
              </p>
            </div>

            {/* Quick Pills */}
            <div className="text-left space-y-2">
              <span className="text-[11px] font-semibold uppercase tracking-wider block" style={{ color: "var(--text-muted)" }}>
                {t("suggestedPrompts")}
              </span>
              <div className="grid grid-cols-1 sm:grid-cols-2 gap-2">
                {suggestedPrompts.map((p, i) => (
                  <button
                    key={i}
                    onClick={() => handleSend(p)}
                    className="p-3 rounded-xl border border-subtle text-left text-xs hover:border-indigo-500/40 transition-all flex items-center justify-between group"
                    style={{ background: "var(--bg-secondary)", color: "var(--text-secondary)" }}
                  >
                    <span className="line-clamp-2">{p}</span>
                    <ArrowRight className="w-3.5 h-3.5 opacity-40 group-hover:opacity-100 group-hover:translate-x-0.5 text-indigo-400 shrink-0 ml-2 transition-all" />
                  </button>
                ))}
              </div>
            </div>
          </div>
        ) : (
          messages.map((m, idx) => <ChatMessage key={idx} message={m} />)
        )}

        {/* Loading Indicator */}
        {loading && (
          <div className="flex items-center gap-3 my-4">
            <div className="w-8 h-8 rounded-xl bg-indigo-600/20 border border-indigo-500/30 flex items-center justify-center text-indigo-400 animate-spin">
              <Sparkles className="w-4 h-4" />
            </div>
            <div className="p-3.5 rounded-2xl border border-subtle text-xs animate-pulse" style={{ background: "var(--bg-secondary)", color: "var(--text-muted)" }}>
              {t("thinking")}
            </div>
          </div>
        )}

        <div ref={messagesEndRef} />
      </div>

      {/* Input Bar */}
      <div className="pt-3 border-t border-subtle shrink-0">
        <form
          onSubmit={(e) => {
            e.preventDefault();
            handleSend();
          }}
          className="relative flex items-center"
        >
          <input
            type="text"
            value={input}
            onChange={(e) => setInput(e.target.value)}
            placeholder={t("askAssistantPlaceholder")}
            disabled={loading}
            className="input-field pr-24 py-3 text-sm rounded-xl"
            style={{ background: "var(--bg-secondary)" }}
          />
          <div className="absolute right-2 flex items-center gap-1.5">
            <button
              type="submit"
              disabled={loading || !input.trim()}
              className="btn btn-primary py-1.5 px-3 rounded-lg text-xs"
            >
              <Send className="w-3.5 h-3.5" />
              <span className="hidden sm:inline">Send</span>
            </button>
          </div>
        </form>
      </div>
    </div>
  );
}
