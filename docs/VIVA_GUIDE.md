# FinPilot AI – Viva & Examination Preparation Guide

This guide compiles anticipated questions and technical answers for the Semester-5 AIML project examination and viva defense.

---

## 1. Core Architecture & Multi-Agent Concepts

### Q1: Why did you build a multi-agent system rather than passing the query and data to a single LLM prompt?
**Answer:**
Single-prompt LLMs suffer from three critical weaknesses in financial applications:
1. **Arithmetic Hallucination**: LLMs are autoregressive token predictors, not mathematical calculation engines. Asking an LLM to sum 35 ledger transactions frequently results in subtle arithmetic errors. In FinPilot, calculations are handled deterministically in Python/SQL via the `MetricAgent`.
2. **Context Window Contamination**: Stuffing transactional ledgers, compliance statutes, and item histories into a single prompt wastes tokens and causes the LLM to lose focus.
3. **Auditing & Traceability**: In a multi-agent architecture (orchestrated via LangGraph), each step is isolated into a discrete node (`Router` $\to$ `Agent` $\to$ `Narrator`). This produces a structured trace showing exactly which tools ran, what data was fetched, and which statutory sources were cited.

### Q2: How does LangGraph coordinate state across agents?
**Answer:**
We use LangGraph's `StateGraph` with a strongly typed `AgentState` dictionary (`backend/app/agents/state.py`). The state maintains:
- `question`: The user's prompt.
- `language`: Target language (`en` or `hi`).
- `intent`: Classified by the `Router` (`metric`, `budget`, `compliance`, or `item_price`).
- `data`: Ground-truth values computed by the tool agents.
- `sources`: Retrieved compliance citations.
- `needs_ca_review`: Boolean flag for statutory topics.
- `agents_used`: List tracking the execution pipeline for auditing.
Conditional edges direct execution from the `Router` to the appropriate tool node, and then converge onto the `Narrator` node.

### Q3: What happens if external LLM APIs (OpenAI / Gemini) are unavailable or have expired keys?
**Answer:**
FinPilot is engineered with complete **offline resilience**:
- **Router Fallback**: If `OPENAI_API_KEY` is absent, the system seamlessly uses a deterministic keyword/regex router (`router.py`) that classifies English, Hindi, and Hinglish queries.
- **Narration Fallback**: Ground-truth computed numbers are rendered using structured native templates (`hindi.py`) rather than generic conversational approximations.
- **RAG Fallback**: If ChromaDB or external embeddings are absent, the RAG engine switches to a local BM25-style keyword density index over the markdown corpus.

---

## 2. Document Extraction & OCR Pipeline

### Q4: How does the document extraction pipeline handle low-quality or scanned invoices?
**Answer:**
We implement a multi-tiered pipeline:
1. **Digital PDFs**: `pdfplumber` directly extracts characters and table structures from vector elements.
2. **Scanned Images / Photos**: `pytesseract` (Tesseract OCR) preprocessed by Pillow converts pixels to text.
3. **Handwritten Slips**: When Tesseract detects zero printed text, the image can be routed to Google Gemini Vision (`gemini-flash-latest`), explicitly prompting the model only for transcription without extrapolation.
4. **Deterministic Cross-Validation**: To guard against OCR errors (such as misreading `8` as `B` or `0` as `O`), our `validator.py` executes mathematical cross-checks:
   $$\text{Quantity} \times \text{Unit Rate} = \text{Amount}$$
   $$\sum \text{Item Amounts} = \text{Subtotal}$$
   $$\text{Subtotal} + \text{Tax} = \text{Total}$$
   Any discrepancies flag the field as *"Verification Required"*, requiring human confirmation before writing to the database.

---

## 3. Retrieval-Augmented Generation (RAG) & Ethics

### Q5: How is RAG implemented, and how do you prevent compliance hallucinations?
**Answer:**
- **Corpus**: We curated 5 focused compliance guides covering GST rules, invoice mandates, the composition scheme, TDS section 194C, and business expense deductibility under the Income Tax Act.
- **Chunking**: Documents are split along markdown section headers (`## `), preserving contextual boundaries.
- **Scoring & Thresholding**: Each retrieved chunk is scored for semantic/keyword similarity. Chunks with similarity score $< 0.45$ are discarded.
- **Guardrails**: If no chunk exceeds the threshold, the assistant states *"No relevant compliance source found"* rather than generating unverified legal advice.

### Q6: Why is the "CA Review" flag necessary?
**Answer:**
Under Indian financial regulations, algorithmic software cannot provide certified statutory tax advice. FinPilot is strictly a **decision-support tool**. Whenever a query routes to the `ComplianceAgent`, the system automatically attaches a formal disclaimer (`needs_ca_review: true`), prompting the business owner to verify deductions and rates with a licensed Chartered Accountant.

---

## 4. Database & Transactional Integrity

### Q7: Why use SQLite for development and how would this transition to production?
**Answer:**
- **Development**: SQLite provides a zero-setup, self-contained, ACID-compliant database embedded in the application filesystem (`data/finpilot.db`).
- **Production Readiness**: Because FinPilot is built with **SQLAlchemy ORM** and clean repository patterns, transitioning to PostgreSQL requires only changing `DATABASE_URL` in `backend/.env` (e.g. `postgresql+psycopg://user:pass@localhost:5432/finpilot`). No application queries or models require modification.

### Q8: How does the CSV Import guarantee database consistency?
**Answer:**
We implement **strict all-or-nothing validation**:
- The uploaded CSV is parsed into Pydantic models (`CSVRow`) in memory.
- Every row is validated for date formats, category existence, and positive monetary values.
- If even a single row fails validation, the entire transaction is rolled back and an error list with exact row numbers is returned to the user. No corrupted or partial batches are committed.

---

## 5. Frontend & User Experience

### Q9: Why build with Vanilla CSS instead of Tailwind CSS or pre-made UI libraries?
**Answer:**
- **Zero Overhead & Full Control**: Vanilla CSS with custom CSS custom properties (variables) provides complete design flexibility, glassmorphism effects, dynamic theme switching without build-step overhead, and guarantees zero dependency conflicts.
- **Performance**: Yields an ultra-compact production bundle (~91 kB gzipped JS, 1.8 kB gzipped CSS) with sub-second page loads.

### Q10: How does bilingual (Hindi/English) support work?
**Answer:**
- The frontend maintains reactive context (`LanguageContext`) translating interface labels, buttons, modals, and tooltips via dedicated dictionary bundles (`en.js` and `hi.js`).
- The backend multi-agent workflow receives the language code and matches queries using Hindi keyword dictionaries (`hindi.py`), outputting culturally appropriate terminology (e.g., *मुनाफ़ा* for profit, *खर्चा* for expenses, *बिक्री* for revenue).
