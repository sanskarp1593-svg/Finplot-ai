import React, { useState } from "react";
import {
  UploadCloud,
  FileText,
  CheckCircle2,
  AlertTriangle,
  XCircle,
  Sparkles,
  ArrowRight,
  ShieldCheck,
  Receipt,
} from "lucide-react";
import { uploadInvoice, confirmInvoice, rejectInvoice } from "../../api/invoices";
import { LoadingSpinner } from "../shared/LoadingSpinner";
import { useToast } from "../../context/ToastContext";
import { useLanguage } from "../../context/LanguageContext";

export function InvoicePage() {
  const { t } = useLanguage();
  const { addToast } = useToast();

  const [file, setFile] = useState(null);
  const [uploading, setUploading] = useState(false);
  const [extractedData, setExtractedData] = useState(null);
  const [documentId, setDocumentId] = useState(null);
  const [confirming, setConfirming] = useState(false);

  const handleFileDrop = async (selectedFile) => {
    if (!selectedFile) return;
    setFile(selectedFile);
    setUploading(true);
    setExtractedData(null);
    setDocumentId(null);

    try {
      const res = await uploadInvoice(selectedFile);
      setDocumentId(res.document_id);
      setExtractedData(res.extracted_data || res);
      addToast("Invoice extracted and cross-validated!", "success");
    } catch (err) {
      addToast(err.message || "Failed to extract invoice", "error");
    } finally {
      setUploading(false);
    }
  };

  const handleConfirm = async () => {
    if (!documentId) return;
    setConfirming(true);
    try {
      await confirmInvoice(documentId, {
        category: "Inventory / Stock",
      });
      addToast("Invoice confirmed & posted to transactions ledger!", "success");
      setExtractedData(null);
      setDocumentId(null);
      setFile(null);
    } catch (err) {
      addToast(err.message || "Confirmation failed", "error");
    } finally {
      setConfirming(false);
    }
  };

  const handleReject = async () => {
    if (!documentId) {
      setExtractedData(null);
      setFile(null);
      return;
    }
    try {
      await rejectInvoice(documentId);
      addToast("Invoice discarded", "info");
      setExtractedData(null);
      setDocumentId(null);
      setFile(null);
    } catch (err) {
      addToast(err.message || "Failed to discard", "error");
    }
  };

  const isMathValid = extractedData?.math_verification?.is_valid ?? true;

  return (
    <div className="p-6 max-w-6xl mx-auto space-y-6 animate-fade-in">
      {/* Header */}
      <div>
        <h2 className="text-xl font-bold tracking-tight" style={{ fontFamily: "var(--font-display)", color: "var(--text-primary)" }}>
          {t("navInvoices")}
        </h2>
        <p className="text-xs" style={{ color: "var(--text-muted)" }}>
          {t("uploadSubtext")}
        </p>
      </div>

      {/* Upload Dropzone */}
      {!extractedData && !uploading && (
        <label
          onDragOver={(e) => e.preventDefault()}
          onDrop={(e) => {
            e.preventDefault();
            if (e.dataTransfer.files && e.dataTransfer.files[0]) {
              handleFileDrop(e.dataTransfer.files[0]);
            }
          }}
          className="glass-panel border-2 border-dashed border-indigo-500/30 hover:border-indigo-400 p-12 flex flex-col items-center justify-center cursor-pointer transition-all rounded-3xl group shadow-glow"
          style={{ background: "var(--bg-secondary)" }}
        >
          <input
            type="file"
            accept=".pdf,.png,.jpg,.jpeg"
            onChange={(e) => {
              if (e.target.files && e.target.files[0]) {
                handleFileDrop(e.target.files[0]);
              }
            }}
            className="hidden"
          />
          <div className="w-16 h-16 rounded-2xl bg-indigo-500/10 border border-indigo-500/20 flex items-center justify-center text-indigo-400 mb-4 group-hover:scale-110 transition-transform">
            <UploadCloud className="w-8 h-8" />
          </div>
          <h3 className="text-base font-bold text-slate-100 mb-1">
            {t("dragDropText")}
          </h3>
          <p className="text-xs text-slate-400 max-w-md text-center leading-relaxed">
            Supports standard PDF supplier invoices, thermal receipts, and raw handwritten billing slips.
          </p>
          <span className="btn btn-primary mt-6 text-xs px-5 py-2">
            Select Invoice File
          </span>
        </label>
      )}

      {/* Uploading Animation */}
      {uploading && (
        <div className="glass-panel p-16 text-center space-y-4">
          <LoadingSpinner text={t("processingInvoice")} size="lg" />
          <p className="text-xs text-indigo-400 font-mono">
            Running PDF table extraction → OCR → Mathematical cross-verification...
          </p>
        </div>
      )}

      {/* Extracted Invoice Review */}
      {extractedData && (
        <div className="glass-panel p-6 space-y-6">
          <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 pb-4 border-b border-subtle">
            <div className="flex items-center gap-3">
              <div className="w-10 h-10 rounded-xl bg-indigo-500/10 border border-indigo-500/30 flex items-center justify-center text-indigo-400">
                <Receipt className="w-5 h-5" />
              </div>
              <div>
                <h3 className="font-bold text-base" style={{ color: "var(--text-primary)" }}>
                  {extractedData.vendor || "Extracted Invoice"}
                </h3>
                <span className="text-xs font-mono" style={{ color: "var(--text-muted)" }}>
                  Date: {extractedData.date || "N/A"} • File: {file?.name || "document"}
                </span>
              </div>
            </div>

            {/* Math Check Badge */}
            <div>
              {isMathValid ? (
                <span className="badge badge-success text-xs py-1 px-3 flex items-center gap-1.5">
                  <CheckCircle2 className="w-4 h-4" />
                  {t("mathCheckPassed")}
                </span>
              ) : (
                <span className="badge badge-danger text-xs py-1 px-3 flex items-center gap-1.5">
                  <AlertTriangle className="w-4 h-4" />
                  {t("mathCheckFailed")}
                </span>
              )}
            </div>
          </div>

          {/* Items Table */}
          <div>
            <h4 className="text-xs font-bold uppercase tracking-wider mb-3" style={{ color: "var(--text-muted)" }}>
              Line Items
            </h4>
            <div className="overflow-x-auto rounded-xl border border-subtle">
              <table className="data-table">
                <thead>
                  <tr>
                    <th>Item Description</th>
                    <th className="text-right">Qty</th>
                    <th className="text-right">Rate</th>
                    <th className="text-right">Amount</th>
                  </tr>
                </thead>
                <tbody>
                  {(extractedData.items || []).map((item, idx) => (
                    <tr key={idx}>
                      <td className="font-semibold text-slate-200">
                        {item.name || item.description || `Item #${idx + 1}`}
                      </td>
                      <td className="text-right font-mono text-xs">
                        {item.quantity ?? item.qty ?? 1}
                      </td>
                      <td className="text-right font-mono text-xs">
                        ₹{Number(item.rate || item.unit_price || 0).toLocaleString("en-IN")}
                      </td>
                      <td className="text-right font-bold font-mono text-xs text-indigo-300">
                        ₹{Number(item.amount || (item.quantity * item.rate) || 0).toLocaleString("en-IN")}
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </div>

          {/* Totals Summary */}
          <div className="flex flex-col sm:flex-row justify-between items-start sm:items-center p-4 rounded-xl bg-slate-900/60 border border-subtle gap-4">
            <div className="space-y-1 text-xs">
              <span className="font-semibold text-slate-400">Extraction Source:</span>
              <p className="text-indigo-400 font-mono">
                {extractedData.upload_source === "handwriting" ? "Handwriting AI" : "Printed OCR / PDF Plumber"}
              </p>
            </div>

            <div className="text-right space-y-1">
              <div className="text-xs text-slate-400">
                Subtotal: ₹{Number(extractedData.subtotal || 0).toLocaleString("en-IN")} + Tax: ₹{Number(extractedData.tax || 0).toLocaleString("en-IN")}
              </div>
              <div className="text-xl font-black text-white font-display">
                Total: ₹{Number(extractedData.total || 0).toLocaleString("en-IN")}
              </div>
            </div>
          </div>

          {/* Action Buttons */}
          <div className="flex items-center justify-end gap-3 pt-4 border-t border-subtle">
            <button
              onClick={handleReject}
              className="btn btn-secondary text-xs"
            >
              <XCircle className="w-3.5 h-3.5" />
              {t("rejectInvoice")}
            </button>
            <button
              disabled={confirming}
              onClick={handleConfirm}
              className="btn btn-primary text-xs px-5"
            >
              <CheckCircle2 className="w-3.5 h-3.5" />
              {confirming ? "Posting..." : t("confirmInvoice")}
            </button>
          </div>
        </div>
      )}
    </div>
  );
}
