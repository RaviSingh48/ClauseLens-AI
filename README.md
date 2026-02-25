# ClauseLens AI – Intelligent Contract Review Bot

ClauseLens AI is an AI-powered contract analysis tool that automatically extracts key clauses, identifies risks, and generates a plain-English summary of legal agreements.

Built as part of an AI Engineer Hiring Task.

---

## Problem Statement

Businesses deal with contracts daily — NDAs, service agreements, vendor contracts, employment letters, etc.  
Manually reviewing these documents is slow, expensive, and error-prone.

ClauseLens AI automates contract review using Large Language Models (LLMs), providing:

- Structured clause extraction
- Risk identification
- Plain-English explanation
- Visual risk highlighting

---

## How It Works (System Architecture)

### Input Layer
- User uploads a PDF OR pastes raw contract text.
- PDF text is extracted using **PyMuPDF**.

### Processing Layer
- Text is chunked for scalability.
- Structured system prompt enforces deterministic JSON output.
- Contract text is sent to an LLM (LLaMA 3.1 via Groq API).

### Intelligence Layer (LLM Brain)
The model extracts:

- Key Parties
- Contract Type
- Effective Date
- Duration
- Renewal Terms
- Payment Terms
- Termination Clauses
- Confidentiality Clause
- Risk Categories
- Plain English Summary

### Risk Detection Logic
The system highlights 4 major risk categories:

- Auto-Renewal Risk
- Liability & Indemnity Risk
- Missing Exit Clause Risk
- Intellectual Property Ownership Risk

Each risk is classified as:
- High (Red)
- Medium (Yellow)
- Low (Green)

### Output Layer
- Structured sections displayed in UI
- Color-coded risk alerts
- Downloadable JSON report

---

## 🛠 Tech Stack

| Layer | Technology Used |
|--------|----------------|
| Frontend | Streamlit |
| Backend | Python |
| PDF Parsing | PyMuPDF |
| Environment Management | python-dotenv |
| LLM API | Groq API |
| Model Used | LLaMA 3.1 (8B Instant) |

---

## Why Groq + LLaMA?

The assignment allows any LLM API if Claude is unavailable.  
Due to API credit constraints, this implementation uses:

**LLaMA 3.1 (8B Instant) via Groq API (Free Tier)**

The structured system prompt is fully Claude-compatible.

---

## Features Implemented

- PDF Upload  
- Raw Text Input  
- Structured JSON Output  
- Clause Extraction  
- Confidentiality Detection  
- 4 Risk Categories  
- Color-Coded Risk Flags  
- Plain English Summary  
- Downloadable Report  
- Error Handling  
- Chunking for Large Documents  




