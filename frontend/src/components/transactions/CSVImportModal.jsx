import React, { useState } from "react";
import { UploadCloud, FileSpreadsheet, AlertCircle, CheckCircle2 } from "lucide-react";
import { Modal } from "../shared/Modal";
import { importCSV } from "../../api/transactions";
import { useToast } from "../../context/ToastContext";

export function CSVImportModal({ isOpen, onClose, onImported }) {
  const { addToast } = useToast();
  const [file, setFile] = useState(null);
  const [uploading, setUploading] = useState(false);
  const [errorDetails, setErrorDetails] = useState(null);

  const handleFileChange = (e) => {
    if (e.target.files && e.target.files[0]) {
      setFile(e.target.files[0]);
      setErrorDetails(null);
    }
  };

  const handleUpload = async () => {
    if (!file) return;
    setUploading(true);
    setErrorDetails(null);
    try {
      const res = await importCSV(file);
      addToast(`Successfully imported ${res.imported_count || "all"} transactions!`, "success");
      onImported();
      onClose();
    } catch (err) {
      setErrorDetails(err.message || "Failed to import CSV");
      addToast("CSV Import Failed (All rows rejected on error)", "error");
    } finally {
      setUploading(false);
    }
  };

  return (
    <Modal isOpen={isOpen} onClose={onClose} title="Import Bank / Accounting CSV">
      <div className="space-y-4 text-xs">
        <p style={{ color: "var(--text-muted)" }}>
          Upload standard statement CSV. The system validates all rows before committing (strict all-or-nothing consistency).
        </p>

        {/* Drop Box */}
        <label
          className={`border-2 border-dashed rounded-2xl p-6 flex flex-col items-center justify-center cursor-pointer transition-all ${
            file
              ? "border-indigo-500 bg-indigo-500/10"
              : "border-slate-700 hover:border-indigo-400 bg-slate-900/40"
          }`}
        >
          <input
            type="file"
            accept=".csv"
            onChange={handleFileChange}
            className="hidden"
          />
          {file ? (
            <div className="flex flex-col items-center gap-2 text-indigo-300">
              <FileSpreadsheet className="w-8 h-8 text-indigo-400" />
              <span className="font-semibold">{file.name}</span>
              <span className="text-[11px] text-slate-400">
                {(file.size / 1024).toFixed(1)} KB
              </span>
            </div>
          ) : (
            <div className="flex flex-col items-center gap-2 text-slate-400">
              <UploadCloud className="w-8 h-8 text-indigo-400 mb-1" />
              <span className="font-medium">Click to select or drag CSV file</span>
              <span className="text-[10px] text-slate-500">Columns: date, type, category, amount, vendor, description</span>
            </div>
          )}
        </label>

        {/* Error Callout */}
        {errorDetails && (
          <div className="p-3 rounded-xl bg-rose-500/10 border border-rose-500/30 text-rose-400 flex items-start gap-2">
            <AlertCircle className="w-4 h-4 shrink-0 mt-0.5" />
            <div className="text-[11px] leading-relaxed break-words">{errorDetails}</div>
          </div>
        )}

        <div className="flex items-center justify-end gap-2 pt-3 border-t border-subtle">
          <button type="button" onClick={onClose} className="btn btn-secondary">
            Cancel
          </button>
          <button
            type="button"
            disabled={!file || uploading}
            onClick={handleUpload}
            className="btn btn-primary"
          >
            {uploading ? "Validating & Importing..." : "Confirm Import"}
          </button>
        </div>
      </div>
    </Modal>
  );
}
