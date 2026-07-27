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
ThreatSutra/
├── docs/
│   └── Threat_Dragon_Model/    # Threat Dragon model and DFD
├── src/
│   ├── adapters/               # External system integrations
│   │   ├── cornucopia.py       # OWASP Cornucopia API client
│   │   ├── github_milestone.py # GitHub milestone integration
│   │   └── threat_dragon.py    # Threat Dragon model reader
│   ├── orchestrator.py         # Coordinates the analysis workflow
│   ├── prompts.py              # Prompt templates
│   ├── validation.py           # Validation utilities
│   └── cli.py                  # Command-line interface
├── .env.example                # Example environment configuration
├── .gitignore                  # Git ignore rules
├── CODEOWNERS                  # Repository ownership
├── CODE_OF_CONDUCT.md          # Community code of conduct
├── CONTRIBUTING.md             # Contribution guidelines
├── LICENSE.md                  # Project license
├── README.md                   # Project overview and setup
└── requirements.txt            # Python dependencies
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

ThreatSutra is being developed under the **OWASP Foundation** through **Google Summer of Code (GSoC) 2026**.

The project extends and integrates the work of the OWASP community, particularly:

- **OWASP Threat Dragon**, which provides the threat modeling foundation used by ThreatSutra.
- **OWASP Cornucopia**, whose security knowledge base and threat cards form the basis for AI-assisted security requirement generation.