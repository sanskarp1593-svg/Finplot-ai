# FinPilot AI – Live Demonstration Script

This script provides a step-by-step demonstration walkthrough for presentations, faculty reviews, and project viva examinations.

---

## 1. Setup & Launch Verification

1. Open PowerShell in the project root:
   ```powershell
   npm run seed      # Seeds clean demo data for Kumar General Store
   npm run ingest    # Indexes the 5 compliance knowledge documents
   npm run dev       # Starts backend on :8000 and frontend on :5173
   ```
2. Open your browser at `http://localhost:5173`.
3. Verify that the TopBar displays:
   - **Business Name**: Kumar General Store
   - **Status Pill**: System Healthy
   - **Controls**: Language Toggle (हिन्दी / English) and Theme Toggle (Dark / Light)

---

## 2. Demonstration Flow 1: Executive KPI Dashboard

**Objective**: Show financial metrics, multi-month trends, category breakdowns, and real-time budget tracking.

1. **Navigate to Dashboard** (Sidebar $\to$ Dashboard).
2. **Observe KPI Cards**:
   - Total Revenue (₹39,700 for August 2026).
   - Total Expenses (₹55,100).
   - Net Profit & Margin percentage.
   - Month-over-month change percentage indicator.
3. **Change Month Dropdown**:
   - Switch from `2026-08` to `2026-07`. Notice the immediate recalculation of revenue, expenses, and margin without reloading.
   - Switch to `2026-06` to inspect earlier trends.
4. **Inspect Visualizations**:
   - **Trend Area Chart**: Demonstrates revenue vs. expenses comparison over the quarter.
   - **Expense Breakdown Pie**: Highlights that Inventory & Stock and Rent constitute the bulk of business outflows.
   - **Budget Progress Bars**: Highlight the category status. Show how categories approaching or exceeding their limit display dynamic warning indicators.

---

## 3. Demonstration Flow 2: Multi-Agent AI Assistant

**Objective**: Prove that the AI Assistant runs specialized agents rather than hallucinating unstructured chat responses.

1. **Navigate to AI Assistant** (Sidebar $\to$ AI Assistant).
2. **Test Metric Calculation**:
   - Type: `How much was our revenue in July 2026?`
   - *Expected Output*: Shows exact ₹39,700 calculation.
   - *Trace Inspector*: Point out the trace badge showing `router` $\to$ `metric` $\to$ `narrator`.
3. **Test Budget Overrun Detection**:
   - Type: `Am I over budget in any category this month?`
   - *Expected Output*: Identifies any category exceeding its monthly threshold and states the exact rupee delta.
   - *Trace Inspector*: Shows `budget` agent execution.
4. **Test RAG Compliance with Citations & CA Review Flag**:
   - Type: `What are the GST rules for small retailers?`
   - *Expected Output*:
     - Plain-language explanation of GST registration thresholds and composition rules.
     - **Source Citation Card**: Clickable citation to `gst_rules_for_small_retailers.md` with similarity score.
     - **CA Review Alert Banner**: Prominently displays:
       > ⚖️ *This information is for reference only. Please consult your Chartered Accountant for statutory filings.*
5. **Test Hindi / Hinglish Query**:
   - Toggle language to **हिन्दी** in the TopBar (or type directly in Hinglish).
   - Type: `pichle mahine kitna kharcha hua?`
   - *Expected Output*: Returns native Hindi response with formatted currency (₹) and Hindi bullet points.
   - Type: `GST ke kya niyam hain?`
   - *Expected Output*: Compliance guidance in Hindi with statutory source citation.

---

## 4. Demonstration Flow 3: Smart Invoice Processing & Error-Catching

**Objective**: Demonstrate OCR document intelligence and deterministic arithmetic verification.

1. **Navigate to Invoices** (Sidebar $\to$ Invoices).
2. **Upload Sample Invoice**:
   - Click the DropZone or drag-and-drop `data/sample_invoices/invoice_aggarwal_traders.pdf`.
3. **Inspect Extraction & Cross-Validation**:
   - The system automatically extracts:
     - Vendor: *Aggarwal Traders*
     - Invoice Date: *2026-08-05*
     - Line Items: Item name, quantity, unit rate, and total.
   - **Math Verification**: Show that the system confirms $\text{Qty} \times \text{Rate} = \text{Amount}$ and checks subtotal + tax against grand total.
4. **Demonstrate Error Flagging**:
   - If an item or number has a typo, the system displays an amber warning badge instead of silently saving incorrect values.
   - Edit a field directly in the preview table.
   - Click **Confirm & Save to Ledger**.
5. **Verify Ledger Sync**:
   - Navigate to **Transactions**. Show that the confirmed invoice has been posted directly into the ledger with source `invoice`.

---

## 5. Demonstration Flow 4: Strict CSV Batch Import & Export

**Objective**: Show enterprise-grade all-or-nothing data consistency.

1. **Navigate to Transactions** (Sidebar $\to$ Transactions).
2. **Export Data**:
   - Click **Export CSV**. Show that the downloaded file contains the active filtered view.
3. **Import Data**:
   - Click **Import CSV**.
   - Upload a test CSV statement.
   - Explain the *all-or-nothing consistency*: If any row fails validation (e.g., negative amount or unrecognized type), the entire import is safely rejected without leaving orphan records.

---

## 6. Demonstration Flow 5: Accessibility & Offline Resilience

1. **Theme Switching**: Toggle Dark Mode and Light Mode to show contrast, typography, and glassmorphic UI tokens.
2. **Offline Resilience**:
   - Point out that the entire RAG pipeline and multi-agent workflow runs locally without requiring paid third-party API keys or external server dependencies.
