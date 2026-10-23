
# FinPilot AI
A multi-agent decision-support assistant for small businesses of any kind. It extracts data from supplier invoices, answers financial questions from computed numbers, tracks spending against monthly budgets, looks up a small compliance knowledge base with citations, and flags anything interpretive for review by a Chartered Accountant.

It is a Semester-5 AIML mini-project. It is **not** a replacement for a Chartered Accountant.

> **Status**: Full-stack application fully implemented and operational with FastAPI backend, React 19 frontend, LangGraph 6-agent workflow, RAG compliance engine, and comprehensive automated test suite.

<img width="2752" height="1536" alt="Gemini_Generated_Image_h8zggbh8zggbh8zg (1)" src="https://github.com/user-attachments/assets/24f4ccda-52e0-429c-ac2b-b786ff130736" />


<img width="2752" height="1536" alt="Gemini_Generated_Image_h8zggbh8zggbh8zg" src="https://github.com/user-attachments/assets/d752eceb-ee6c-4b4d-8f6b-a80dcf9aae63" />


## Features

- **Dashboard:** revenue, expenses, profit and margin for any month, with change vs the previous month and a sparkline trend. Also shows the monthly trend chart, expenses by category, and budget progress bars with over-budget alerts.
- **Transactions:** filter and search. Add or delete entries by hand. Import a CSV, where every row is validated and nothing is saved if any row is invalid. Export the current view to CSV.
- **Invoice Upload:** drag and drop a PDF or image. Fields are extracted, and anything unreadable is flagged "Verification required" instead of being guessed. You correct and confirm, and the invoice is saved as a transaction.
- **AI Assistant:** a chat thread over a 6-agent LangGraph workflow. Each answer shows the agents that ran, metrics, driver analysis, charts, evidence and retrieved sources, plus a CA-review banner when needed.
- **Item prices:** ask "What was the last onion price?" or "Should I buy 10 kg at Rs 2000?". The answer comes from the items on your confirmed bills: the last rate, earlier rates, and how an offer compares. It warns when rates on record differ a lot, which often means a typo. It never says "buy" or "don't buy".
- **Reports:** a month-by-month P&L and a category comparison.
- **Knowledge & History:** the demo knowledge base and every past query.
- **Settings:** business name and industry, and monthly budgets per expense category.
- **Hindi or English (हिन्दी / English):** the first visit asks which language to use; switch any time from the sidebar or Settings. Menus, messages and the AI Assistant's answers follow the choice, and the assistant understands questions typed in Hindi, English or Hinglish (e.g. "is mahine munafa kitna hua?").
- **Dark mode**, and a layout that works at phone width.

CSV import format (header row required; `tax_amount`, `description` and `vendor` are optional):

```csv
date,type,category,amount,tax_amount,description,vendor
2026-08-10,expense,Travel & Transport,1800,90,Courier charges,BlueDart
2026-08-11,revenue,Service Revenue,5000,900,Installation job,
```

## Stack

| Layer | Used |
|---|---|
| Frontend | React 19 + Tailwind CSS 4 (Vite), Recharts |
| Backend | Python 3.12, FastAPI, Pydantic models on every endpoint |
| Orchestration | LangGraph `StateGraph` with 6 agent nodes |
| Database | SQLAlchemy models. **This build runs on SQLite, the documented dev fallback**, because PostgreSQL is not installed on the development machine. The same models run on PostgreSQL by changing `DATABASE_URL` (install `psycopg[binary]`). |
| RAG | ChromaDB (local persistent), local ONNX embeddings (`all-MiniLM-L6-v2`), so no API key is needed for retrieval |
| Documents | pdfplumber for PDF text and tables; pytesseract + Pillow for images and scanned PDFs |
| LLM | OpenAI (optional). Without a key: a deterministic keyword router and template narration. |

## Quick start

From the project root:

```powershell
npm install
npm install --prefix frontend
npm run dev        # starts backend (http://localhost:8000) and frontend (http://localhost:5173) together
```

The frontend checks `http://localhost:5173/api/health` through the Vite proxy. The backend health
endpoint is also available directly at `http://localhost:8000/api/health`.

## Reading handwritten notes (optional, free)

Printed bills are read on your computer by Tesseract OCR. Tesseract can't read handwriting, so when it finds no printed text, FinPilot can send the image to **Google Gemini** to transcribe it.

1. Go to https://aistudio.google.com, sign in, and click **Get API key**.
2. Open `backend/.env` and paste the key after `GEMINI_API_KEY=`.
3. Restart the app (`Ctrl+C`, then `npm run dev`). The sidebar shows **Handwriting AI: on**.

How it stays honest:
- Gemini is only asked to **copy the text exactly as written**. It does no calculating or filling in.
- The copied text goes through the same checks as any bill.
- **Every field is marked "Verification required"**, with the note "Read by AI from handwriting".
- Anything not written on the note (seller, date, GST) is left empty.
- Your own business name at the top of a note is never taken as the seller.

Printed bills are **never** sent to Gemini.

Privacy and limits:
- The image is sent to Google.
- On the free tier Google may use it to improve its products, so don't upload sensitive documents.
- The free tier has request limits. If they're reached, the app says so and offers manual entry.
- If the default model is retired, set `GEMINI_MODEL` to a current one listed in AI Studio.

## Sharing with someone else

The frontend calls the backend through `/api` on the same server (a Vite proxy), so one address serves the whole app.

- **Same Wi-Fi:** run `npm run share` instead of `npm run dev`, then send `http://<your-laptop-IP>:5173` (find the IP with `ipconfig`). If it doesn't load, allow Node.js through Windows Firewall on private networks.
- **Anywhere, no account (Cloudflare quick tunnel):**
  1. Install once: `winget install Cloudflare.cloudflared`.
  2. Keep `npm run dev` running and, in a second terminal, run `cloudflared tunnel --url http://localhost:5173`.
  3. Send the printed `https://….trycloudflare.com` link.
- **Anywhere with ngrok** (free account needed):
  1. Run `ngrok config add-authtoken <token>` once.
  2. Run `ngrok http 5173` and send the `https://….ngrok-free.app` link.

The link only works while your laptop and both terminals are running, and a Cloudflare quick tunnel gets a new URL each time. **There is no login**, so anyone with the link can view and change the data. Share it only with people you trust, and stop the tunnel (Ctrl+C) when you're done. Run `npm run seed` afterwards to reset the data.

## Setup (Windows PowerShell)

```powershell
npm install
npm install --prefix frontend
npm run seed       # Populates sample demo business with transactions & budgets
npm run ingest     # Indexes the compliance knowledge base
npm run dev        # Starts backend (http://localhost:8000) and frontend (http://localhost:5173) together
```

To run the automated test suite across all subsystems:
```powershell
npm test           # Runs 14 comprehensive pytest tests
```

To regenerate the two sample invoices, run `backend\.venv\Scripts\python.exe data\generate_sample_invoices.py`. They are already generated in `data/sample_invoices/`.

Re-running `npm run seed` resets business #1 to the clean sample data: the name, transactions, budgets, uploaded documents and query history are all reset. To use FinPilot for a real business, run `backend\.venv\Scripts\python.exe -m app.db.seed --empty` instead. It clears everything and starts with an empty ledger and no budgets. Then set the name and industry in Settings, and add data by CSV import, manual entry or invoice upload.

## Environment variables (`backend/.env`)

| Variable | Default | Meaning |
|---|---|---|
| `DATABASE_URL` | SQLite at `data/finpilot.db` | e.g. `postgresql+psycopg://user:pass@localhost:5432/finpilot` |
| `OPENAI_API_KEY` | unset | Optional. Enables LLM classification and narration. |
| `OPENAI_MODEL` | `gpt-4o-mini` | |
| `LLM_TIMEOUT_SECONDS` | 20 | Timeout for each LLM call. On timeout the app falls back. |
| `FORCE_FALLBACK_ROUTER` | false | Use the keyword router even when a key is set. |
| `CORS_ORIGINS` | `http://localhost:5173` | Comma-separated allowed origins. |
| `MAX_UPLOAD_MB` | 5 | Upload size limit. |
| `RAG_MIN_SIMILARITY` | 0.45 | Cosine-similarity threshold below which RAG answers "No relevant source found". |

Secrets are only read from `backend/.env`, which is git-ignored. The frontend can use
`VITE_API_BASE_URL` in `frontend/.env`; when unset, it calls `/api` through the Vite proxy.

## Documentation

Comprehensive guides are available in the `docs/` directory:
- [Architecture & System Design](docs/ARCHITECTURE.md) – Detailed multi-agent state graph, RAG pipeline, and data schemas.
- [Live Demonstration Script](docs/DEMO_SCRIPT.md) – Step-by-step walkthrough for faculty presentations.
- [Viva & Exam Preparation Guide](docs/VIVA_GUIDE.md) – Technical Q&A on agents, determinism, and OCR validation.

## Tests

```powershell
npm test
```

The tests use a transactional test SQLite DB and local RAG index, seeded from the real seed script and knowledge docs. All 14 tests run offline in sub-second time without requiring external API keys.


## Known limitations

- **No authentication.** Authentication is out of scope for this MVP. Anyone who can reach the API can read and write the single demo business's data. Do not expose it beyond localhost.
- SQLite dev fallback in use (see above).
- **Photos and scanned PDFs need Tesseract OCR.** Install it once with `winget install UB-Mannheim.TesseractOCR`. FinPilot finds it in `C:\Program Files\Tesseract-OCR` automatically, or set `TESSERACT_CMD` in `backend/.env`. Without it, image uploads fail with an explicit `ocr_unavailable` error. PDFs with a text layer work either way.
- **OCR is less accurate than reading a real PDF.** Blurry, tilted or crumpled photos may misread digits or skip rows. FinPilot checks every row (quantity × rate = amount), the item total against the subtotal, and subtotal + GST against the total, and highlights anything that doesn't add up. The user corrects it, including the editable item rows, before saving. Clear, flat, well-lit photos work best.
- The knowledge base is five short, hand-written demo notes, not an authoritative legal or tax corpus.
- "This month" means the latest month that has transactions (August 2026 in the seed), not the calendar month.
- One business per installation, with a fixed category list.
- **Item prices** only know items from bills you have uploaded and confirmed (the sample data starts with none). Bills don't record units, so an offer in kg is compared assuming the bill's quantity was also in kg; the answer says so. Item names are matched by words, with plurals, small spelling slips and common Hindi names (प्याज़/pyaaz → onion) handled.
- **Hindi:** only the words change. Numbers come from the same calculations in both languages (the tests check this). Hindi questions are understood by keyword matching, so unusual phrasings may fall back to "unsupported". The knowledge-base notes are in English, so compliance passages are quoted in English, and Hindi compliance questions match them less often (the "no source found" rule still applies). The evidence trail and some rare error messages stay in English.

See `docs/ARCHITECTURE.md`, `docs/DEMO_SCRIPT.md` and `docs/VIVA_GUIDE.md`.
