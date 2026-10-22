import React, { useState, useEffect } from "react";
import { BookOpen, Search, ShieldCheck, ChevronRight, FileText } from "lucide-react";
import { getKnowledgeDocs } from "../../api/knowledge";
import { LoadingSpinner } from "../shared/LoadingSpinner";
import { useLanguage } from "../../context/LanguageContext";

export function KnowledgePage() {
  const { t } = useLanguage();
  const [docs, setDocs] = useState([]);
  const [loading, setLoading] = useState(true);
  const [selectedDoc, setSelectedDoc] = useState(null);
  const [search, setSearch] = useState("");

  useEffect(() => {
    async function loadDocs() {
      setLoading(true);
      try {
        const res = await getKnowledgeDocs();
        setDocs(res || []);
        if (res && res.length > 0) {
          setSelectedDoc(res[0]);
        }
      } catch (err) {
        console.error("Failed to load knowledge:", err);
      } finally {
        setLoading(false);
      }
    }
    loadDocs();
  }, []);

  const filteredDocs = docs.filter(
    (d) =>
      d.title.toLowerCase().includes(search.toLowerCase()) ||
      d.content.toLowerCase().includes(search.toLowerCase())
  );

  return (
    <div className="p-6 max-w-7xl mx-auto space-y-6 animate-fade-in">
      {/* Header */}
      <div>
        <h2 className="text-xl font-bold tracking-tight" style={{ fontFamily: "var(--font-display)", color: "var(--text-primary)" }}>
          {t("complianceKnowledge")}
        </h2>
        <p className="text-xs" style={{ color: "var(--text-muted)" }}>
          {t("knowledgeSubtitle")}
        </p>
      </div>

      {loading ? (
        <LoadingSpinner text="Loading regulatory compliance knowledge base..." />
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
          {/* Left Column: Documents List */}
          <div className="space-y-3">
            <div className="relative">
              <Search className="w-4 h-4 text-slate-400 absolute left-3 top-1/2 -translate-y-1/2" />
              <input
                type="text"
                placeholder="Search regulatory rules..."
                value={search}
                onChange={(e) => setSearch(e.target.value)}
                className="input-field pl-9 py-2 text-xs"
              />
            </div>

            <div className="space-y-2">
              {filteredDocs.map((doc) => {
                const isSelected = selectedDoc?.id === doc.id;
                return (
                  <button
                    key={doc.id}
                    onClick={() => setSelectedDoc(doc)}
                    className={`w-full text-left p-3.5 rounded-xl border transition-all flex items-center justify-between ${
                      isSelected
                        ? "bg-indigo-600/10 border-indigo-500/40 text-indigo-300"
                        : "glass-card border-subtle hover:border-slate-700 text-slate-300"
                    }`}
                  >
                    <div className="flex items-center gap-2.5 truncate">
                      <FileText className={`w-4 h-4 shrink-0 ${isSelected ? "text-indigo-400" : "text-slate-500"}`} />
                      <span className="font-semibold text-xs truncate">{doc.title}</span>
                    </div>
                    <ChevronRight className="w-3.5 h-3.5 opacity-50 shrink-0" />
                  </button>
                );
              })}
            </div>
          </div>

          {/* Right Column: Document Viewer */}
          <div className="md:col-span-2 glass-panel p-6 overflow-y-auto max-h-[75vh]">
            {selectedDoc ? (
              <div className="space-y-4">
                <div className="pb-4 border-b border-subtle flex items-center justify-between">
                  <div>
                    <h3 className="text-lg font-bold" style={{ color: "var(--text-primary)" }}>
                      {selectedDoc.title}
                    </h3>
                    <span className="text-xs font-mono text-indigo-400">
                      Source: data/knowledge/{selectedDoc.source_file}
                    </span>
                  </div>
                  <span className="badge badge-success text-[10px] py-1 px-2.5 flex items-center gap-1">
                    <ShieldCheck className="w-3 h-3" /> Indexed in RAG
                  </span>
                </div>

                <div className="prose prose-invert max-w-none text-xs leading-relaxed space-y-3 font-sans whitespace-pre-wrap" style={{ color: "var(--text-secondary)" }}>
                  {selectedDoc.content}
                </div>
              </div>
            ) : (
              <div className="text-center py-12 text-xs text-slate-500">
                Select a document from the left to read full compliance guidelines.
              </div>
            )}
          </div>
        </div>
      )}
    </div>
  );
}
