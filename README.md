# Tayler Erbe · Portfolio

Production AI/ML engineering, applied NLP, and inference performance work — built end-to-end across a four-year tenure leading the Advanced Analytics function at the University of Illinois System.

**Live site:** [taylererbe.com](https://taylererbe.com) (GitHub Pages mirror: [tayler-erbe.github.io/tayler-portfolio](https://tayler-erbe.github.io/tayler-portfolio/))

---

## What's Inside

A working portfolio of production and research projects spanning the full applied AI stack — from RAG systems serving executive decision-making, to inference performance engineering on constrained hardware, to predictive ML models that have informed institutional retention and workforce strategy.

Each project links to a dedicated case study with architecture diagrams, methodology, measured results, and the engineering reasoning behind key decisions.

### Featured Work

- **vLLM Throughput Migration · Archival Image Pipeline** — Diagnosed request serialization in a production LLaVA pipeline on a single NVIDIA L4. Migrated to vLLM continuous batching for a 6.22× speedup on the same hardware and same model class. 12,125-image corpus from 22 hours to 3.7 hours.
- **vLLM Multi-Model Sweep · Legislation Pipeline** — Controlled 54-cell benchmark across three open-weight 7–8B AWQ models (Mistral, Qwen 2.5, Llama 3.1) to defend or replace the production model choice. 8h 34m unattended runtime, 4,586 per-chunk samples. Identified Llama 3.1 8B AWQ as the production winner.
- **Archival Image Intelligence & Sensitive Content Detection** — Multimodal AI proof-of-concept for automatically detecting culturally significant content in historical image archives. Combines LLaVA visual classification, semantic similarity embeddings, and IPTC-compliant metadata extraction. Now part of the RIMS archival pipeline production build (August 2026 onward), which I lead as technical lead, architect and project manager: three proofs of concept unified into one eight-stage pipeline, with the University Library's engineer mentored toward full ownership.
- **Legislative Intelligence Platform** — End-to-end RAG system for executive-level natural-language querying of state and federal legislation. LLM feature extraction, vector retrieval, semantic search, chatbot interface. Delivered to IGPA in production on Azure (August 2026). Bill passage prediction validated on a held-out General Assembly: 75.1% precision and 76.2% recall with a median 21 days' warning before the floor vote (introduction-time ROC-AUC 0.845).
- **Research Proposal Processing Pipeline** — Fully automated NLP pipeline ingesting live Oracle BLOB data, running an 11-step extraction chain, and writing structured results back to institutional databases on a cron schedule.
- **Email Archiving & PII Anonymization** — Privacy-first multimodal pipeline processing 79,676 messages with Microsoft Presidio anonymization, LLM summarization, and LDA topic modeling.
- **Legacy File Archive Intelligence** — Semantic search across heterogeneous legacy institutional content (15+ file types, LLaVA for images, LLaMA for text/code/spreadsheets, FAISS retrieval).
- **HR Workforce Analytics POC** — Predictive models combining Random Forest, Markov chain career simulation, and graph community detection to anticipate workforce risks and surface internal mobility paths. Related production work: recovered and rebuilt the quarterly retirement-risk forecasting system end to end in Python after its platform was decommissioned, correcting long-standing statistical defects and returning it to monitored quarterly production.
- **UIC Enrollment Forecasting** — 10-year departmental enrollment projections combining Random Forest, tree ensemble, and ARIMA approaches.
- **Skyrule (personal project)** — A self-funded relational-intelligence product built by a 15-agent AI engineering organization I designed, with code ownership enforced by tooling, an autonomous job queue and GPU scheduler (650+ unattended jobs), a self-hosted vLLM stack on an RTX 5090, validator-gated LLM generation with founder review, statistical acceptance testing, and dedicated quality-governance and security functions.
- **Drop Radar (personal project)** — A 24/7 drop-alert system I built for my husband over one weekend (live since October 22, 2026). It watches about 40 stores and sources, alerts his phone in seconds, and improves itself through a Claude Code agent that reads his Telegram notes, changes its own code, tests it and replies. Official Discord Gateway ingestion over a standard-library websocket, cart links within store rules, a private purchase and eBay ledger, and alerts only, never a checkout bot. Its AI deep search found a 100-piece limited-edition watch that sold out in minutes, and he got one. 357 commits, ~3,300 lines of standard-library Python, 25 automated tests.

---

## Technical Focus Areas

- **LLM & Inference Engineering** — vLLM, Ollama, LLaVA, continuous batching, throughput characterization, GPU profiling on NVIDIA L4
- **Applied NLP** — RAG systems, semantic search, topic modeling, feature extraction, PII detection, document intelligence
- **Predictive ML** — Random Forest, time-series forecasting, graph analytics, Markov chain simulation
- **Production Engineering** — End-to-end pipelines, Oracle integration, cron orchestration, custom observability, post-write verification, Azure deployment

---

## About

I'm a Senior Data Scientist on the AI Solutions team at AITS, University of Illinois System, where I led the Advanced Analytics function for the past several years. I own projects from problem scoping through production deployment, and I write about the engineering choices behind them in dedicated case studies and on Medium.

- **Website:** [taylererbe.com](https://taylererbe.com)
- **LinkedIn:** [linkedin.com/in/tayler-erbe-194374141](https://www.linkedin.com/in/tayler-erbe-194374141)
- **Medium:** [medium.com/@tayler.erbe](https://medium.com/@tayler.erbe)
