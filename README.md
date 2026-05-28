# Tayler Erbe · Portfolio

Production AI/ML engineering, applied NLP, and inference performance work — built end-to-end across a four-year tenure leading the Advanced Analytics function at the University of Illinois System.

**Live site:** [terbe2022.github.io/tayler-portfolio](https://terbe2022.github.io/tayler-portfolio/)

---

## What's Inside

A working portfolio of production and research projects spanning the full applied AI stack — from RAG systems serving executive decision-making, to inference performance engineering on constrained hardware, to predictive ML models that have informed institutional retention and workforce strategy.

Each project links to a dedicated case study with architecture diagrams, methodology, measured results, and the engineering reasoning behind key decisions.

### Featured Work

- **vLLM Throughput Migration · Archival Image Pipeline** — Diagnosed request serialization in a production LLaVA pipeline on a single NVIDIA L4. Migrated to vLLM continuous batching for a 6.22× speedup on the same hardware and same model class. 12,125-image corpus from 22 hours to 3.7 hours.
- **vLLM Multi-Model Sweep · Legislation Pipeline** — Controlled 54-cell benchmark across three open-weight 7–8B AWQ models (Mistral, Qwen 2.5, Llama 3.1) to defend or replace the production model choice. 8h 34m unattended runtime, 4,586 per-chunk samples. Identified Llama 3.1 8B AWQ as the production winner.
- **Archival Image Intelligence & Sensitive Content Detection** — Multimodal AI proof-of-concept for automatically detecting culturally significant content in historical image archives. Combines LLaVA visual classification, semantic similarity embeddings, and IPTC-compliant metadata extraction.
- **Legislative Intelligence Platform** — End-to-end RAG system for executive-level natural-language querying of state and federal legislation. LLM feature extraction, vector retrieval, semantic search, chatbot interface. Live on Azure.
- **Research Proposal Processing Pipeline** — Fully automated NLP pipeline ingesting live Oracle BLOB data, running an 11-step extraction chain, and writing structured results back to institutional databases on a cron schedule.
- **Email Archiving & PII Anonymization** — Privacy-first multimodal pipeline processing 79,676 messages with Microsoft Presidio anonymization, LLM summarization, and LDA topic modeling.
- **Legacy File Archive Intelligence** — Semantic search across heterogeneous legacy institutional content (15+ file types, LLaVA for images, LLaMA for text/code/spreadsheets, FAISS retrieval).
- **HR Workforce Analytics POC** — Predictive models combining Random Forest, Markov chain career simulation, and graph community detection to anticipate workforce risks and surface internal mobility paths.
- **UIC Enrollment Forecasting** — 10-year departmental enrollment projections combining Random Forest, tree ensemble, and ARIMA approaches.

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
