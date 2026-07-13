# ThreatSutra – Phase 1 

ThreatSutra is an AI-assisted security orchestration prototype developed as part of Google Summer of Code 2026 under the OWASP Foundation.
The current implementation focuses on the initial Phase 1 workflow using sample Threat Dragon and Cornucopia data.

---

## Current Features

The application currently performs the following workflow:

1. Loads sample Threat Dragon threat data.
2. Loads sample Cornucopia card data.
3. Validates the input data.
4. Builds prompts for Gemini.
5. Generates:
   - Evil User Story (Issue #6)
   - Verification Test (Issue #5)
6. Displays both generated outputs through the command-line interface.
7. Allows the reviewer to:
   - Approve
   - Reject
   - Edit
8. Saves the reviewed output automatically to the `outputs/` folder for future reference.

---

## Project Structure

```
ThreatSutra/
│
├── docs/
│   ├── diagrams/
│   ├── phase1_qa_review_2026-07-13.md
│   └── phase1_qa_summary_2026-07-13.md
│
├── outputs/
├── sample_data/
│   ├── threat_dragon_sample.json
│   └── cornucopia_card_sample.json
│
├── src/
│   ├── __init__.py
│   ├── cli.py
│   ├── orchestrator.py
│   ├── prompts.py
│   └── validation.py
│
├── .env.example
├── requirements.txt
├── .gitignore
└── README.md
```

---

## Installation

Create a virtual environment:

```bash
python -m venv .venv
```

Activate it:

Linux / WSL

```bash
source .venv/bin/activate
```

Windows

```powershell
.venv\Scripts\activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

---

## Configuration

Create a `.env` file from `.env.example`.

Add your Gemini API key:

```text
GEMINI_API_KEY=YOUR_API_KEY
```

An example file is included at `.env.example`.

---

## Running the Project

From the project root:

```bash
python src/cli.py
```

---

## Current Workflow

```
Threat Dragon Sample JSON
            │
            ▼
      Input Validation
            │
            ▼
      Prompt Generation
            │
            ▼
      Gemini API
            │
            ▼
 Evil User Story
 Verification Test
            │
            ▼
     Human Review Gate
(Approve / Reject / Edit)
            │
            ▼
 Automatic Output Saving
```

---

## Review Documents

The current QA and AppSec assessment for this prototype is documented here:

- `docs/phase1_qa_review_2026-07-13.md`
- `docs/phase1_qa_summary_2026-07-13.md`

These documents summarize what is already working, what is still missing for Phase 1, and the recommended implementation order for the remaining work.

---

## Current Status

This implementation represents the current Phase 1 prototype using sample data. The remaining Phase 1 work is in progress.

The prototype currently demonstrates the review flow and model integration, but it does not yet complete the real-source ingestion and joined-context work described by the active GitHub issues.