# ThreatSutra

ThreatSutra is an AI-assisted security engineering project developed under the OWASP Foundation as part of Google Summer of Code (GSoC).

The project aims to assist security practitioners and development teams by transforming threat models into actionable security engineering artifacts. By combining Threat Dragon threat models, OWASP Cornucopia knowledge, GitHub project context, and Large Language Models (LLMs), ThreatSutra helps generate meaningful security outputs while keeping humans in control of the final decisions.

> **Project Status**
>
> ThreatSutra is currently under active development. The repository contains the foundational components being built during the first development phase.

---

## Vision

ThreatSutra aims to streamline security requirement generation by connecting multiple OWASP resources into a single workflow.

The long-term vision includes:

- Reading OWASP Threat Dragon threat models
- Enriching threats using OWASP Cornucopia knowledge
- Incorporating GitHub project context
- Generating AI-assisted security engineering outputs
- Supporting human review before acceptance
- Exporting approved outputs back into development workflows

Human oversight remains a core principle throughout the process.

---

## Current Development

The current implementation focuses on establishing the project's core architecture and integration layer.

Current work includes:

- Threat Dragon model processing
- OWASP Cornucopia integration
- GitHub milestone retrieval
- AI orchestration foundation
- Shared project context management
- Command-line interface (CLI)

These components form the foundation for future AI-powered security analysis.

---

## Planned Workflow

The intended workflow for ThreatSutra is:

```text
Threat Dragon Model
        │
        ▼
Threat Extraction
        │
        ▼
Cornucopia Knowledge
        │
        ▼
GitHub Project Context
        │
        ▼
AI Orchestrator
        │
        ▼
Security Engineering Outputs
        │
        ▼
Human Review
        │
        ▼
Approved Results
```

Additional capabilities will be introduced as the project progresses.

---

## Repository Structure

```
src/
├── adapters/          # External system integrations
├── orchestrator.py    # Coordinates the processing pipeline
├── context.py         # Shared analysis context
├── prompts.py         # Prompt templates
├── validation.py      # Validation utilities
├── review_store.py    # Review data management
└── cli.py             # Command-line interface

tests/                 # Automated tests
docs/                  # Project documentation
```

---

## Technology Stack

- Python
- OWASP Threat Dragon
- OWASP Cornucopia
- GitHub API
- Google Gemini
- JSON
- Command-Line Interface (CLI)

---

## Project Roadmap

ThreatSutra is being developed incrementally.

### Phase 1

- Foundation architecture
- Threat Dragon integration
- Cornucopia integration
- GitHub context retrieval
- AI orchestration
- Human review workflow

### Future Enhancements

Future development may include additional AI capabilities, richer project context, and expanded workflow integrations as the project evolves.

---

## Contributing

Contributions, feedback, and discussions are welcome.

Please refer to:

- `CONTRIBUTING.md`
- `CODE_OF_CONDUCT.md`

before submitting issues or pull requests.

---

## License

This project is licensed under the terms described in the `LICENSE` file.

---

## Acknowledgements

ThreatSutra is developed under the **OWASP Foundation** as part of **Google Summer of Code (GSoC)**.

The project builds upon the excellent work of the OWASP community, particularly:

- OWASP Threat Dragon
- OWASP Cornucopia