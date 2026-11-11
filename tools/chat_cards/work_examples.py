"""Work-example and "have you used X" answer cards for the Ask Tayler chat.

Every fact here comes from a page on taylererbe.com or the Applied AI Lab. Edit this file, then run
    python3 tools/chat_cards/merge.py
to write the cards into assets/chat/kb.json (cards with the same id are replaced, so it is safe to re-run).
"""

LAB = "https://tayler-erbe.github.io/document-intelligence-lab/"


def L(label, url):
    return {"label": label, "url": url}


LAB_LINK = L("Applied AI Lab", LAB)

EX = ("examples", "Examples of my work")
TECH = ("tools", "Tools and platforms")

CARDS = []


def card(sec, cid, title, questions, tags, links, answer, sources=None, **extra):
    c = {"id": cid, "section": sec[0], "section_label": sec[1], "title": title, "questions": questions,
         "tags": tags, "links": links, "state": "CLEAN", "answer": " ".join(answer.split())}
    if sources:
        c["sources"] = sources
    c.update(extra)
    CARDS.append(c)


# ----------------------------------------------------------------------------------------------------------------
# Capabilities: "show me an example of ..."
# ----------------------------------------------------------------------------------------------------------------

card(EX, "ex-data-science-projects", "Examples of my data science projects", [
    "examples of data science projects",
    "examples of data science project",
    "what kind of data science have you done",
    "what data science work have you done",
    "show me your data science work",
    "give me an example of a data science project",
    "tell me about a data science project",
    "what data science projects have you worked on",
    "have you done real data science",
    "what kind of data science do you do",
    "data science experience",
    "data science portfolio",
    "tell me about when you did data science",
    "tell me about the data science you did",
    "data science work you have done",
    "tell me about a time you did something that was more data science",
    "something more data science",
], ["data science", "examples", "projects", "machine learning", "predictive", "modeling"], [
    L("Bill passage prediction", "legislative-pipeline.html"),
    L("UIC enrollment forecasting", "uic-enrollment.html"),
    L("HR workforce analytics", "hr-workforce-analytics.html"),
    L("Procurement intelligence", "procurement-intelligence.html"),
], """
Four good examples. Bill passage prediction: I trained a model on 117,722 Illinois bills and validated it on a General
Assembly it never saw, with 75.1% precision, 76.2% recall and a median 21 days' warning before the floor vote.
Student enrollment at UIC: a classifier that flags students at risk of discontinuing, at about 82% accuracy, plus
ARIMA projections ten years out by department. HR workforce analytics: Random Forest promotion prediction, Markov chain
career simulation and graph community detection, and I rebuilt the quarterly retirement-risk forecast in Python.
Procurement: matching 6 million catalog rows to find $161,564 in savings that hold up after unit normalization.
""")

card(EX, "ex-predictive-model", "An example of a predictive model I built", [
    "show me an example of a predictive model",
    "example of a predictive model",
    "tell me about a predictive model you built",
    "have you built a predictive model",
    "have you done predictive modeling",
    "predictive modeling example",
    "tell me about a time you built a model that predicted something",
    "what is the best model you have built",
    "walk me through a machine learning model you built",
    "have you built a machine learning model end to end",
    "did you build a model that predicts",
    "have you built a model to predict something",
    "prediction model example",
    "predictive analytics experience",
    "most impressive model you have built",
], ["predictive model", "prediction", "machine learning", "classifier", "bill passage", "validation", "example"], [
    L("Legislative pipeline: prediction", "legislative-pipeline.html"),
    L("UIC enrollment forecasting", "uic-enrollment.html"),
], """
My strongest example is bill passage prediction for the Legislative Intelligence Platform. The original dataset was
missing every resolved bill, so I rebuilt it: 117,722 Illinois bills. Adding each bill's title and synopsis raised the
introduction-time ROC-AUC from 0.561 to 0.845, and I confirmed that with ablation and leakage checks. On the 103rd
General Assembly, held out completely, it reached 75.1% precision and 76.2% recall at a 0.70 threshold, with a median
21 days' warning before the floor vote. I also fixed train/serve skew with one shared input module and checked 36,028
inputs byte for byte. A second example is the UIC enrollment-risk classifier, at about 82% accuracy.
""")

card(EX, "ex-predictive-models-list", "Every kind of predictive model I've built", [
    "what predictive models have you built",
    "what kinds of models have you built",
    "list the machine learning models you have built",
    "what machine learning have you done",
    "what types of machine learning have you used",
    "what ml models have you used",
    "traditional machine learning not llms",
], ["machine learning", "models", "random forest", "arima", "markov", "gradient boosting", "classification", "forecasting"], [
    L("UIC enrollment", "uic-enrollment.html"),
    L("HR workforce analytics", "hr-workforce-analytics.html"),
    L("Legislative pipeline", "legislative-pipeline.html"),
], """
Classification: bill passage prediction (75.1% precision, 76.2% recall on a held-out Assembly) and UIC
enrollment risk (about 82% accuracy), where the team compared Random Forest, tree ensembles, H2O and CatBoost. Forecasting:
ARIMA with exponential smoothing for ten-year enrollment projections, and the quarterly retirement-risk forecast I
rebuilt in Python. Workforce modeling: Random Forest promotion prediction, Markov chain career simulation and graph
community detection, plus designs for XGBoost and logistic regression departure risk and a learning-to-rank readiness
model. Text models: TF-IDF, KeyBERT and LDA for keywords and topics, and HERDS research-field classification.
""")

card(EX, "ex-forecasting", "Forecasting and time-series work", [
    "have you done forecasting",
    "time series forecasting experience",
    "example of a forecasting model",
    "have you used arima",
    "tell me about your forecasting work",
    "have you forecast demand or enrollment",
    "time series example",
], ["forecasting", "time series", "arima", "projection", "enrollment", "retirement", "workforce"], [
    L("UIC enrollment forecasting", "uic-enrollment.html"),
    L("HR workforce analytics", "hr-workforce-analytics.html"),
], """
Yes. For UIC I led a project that paired the classifier I built, which flags students at risk of leaving, with ten-year enrollment projections by department and college from ARIMA and exponential smoothing models built by teammates. For HR, I rebuilt the quarterly retirement-risk
forecast in Python after its KNIME platform was retired. I delivered the overdue report the same day, corrected
long-standing statistical defects, and it now runs on a monitored quarterly schedule. The HR workforce platform also
includes workforce growth forecasting with BLS and O*NET outlook data.
""")

card(EX, "ex-classification", "Classification models I've built", [
    "example of a classification model",
    "have you built a classifier",
    "classification project example",
    "have you done binary classification",
    "have you built a model to flag risk",
    "risk scoring model example",
    "how do you handle a classifier with imbalanced classes in practice",
], ["classification", "classifier", "risk", "flag", "accuracy", "precision", "recall"], [
    L("UIC enrollment: models", "uic-enrollment.html#models"),
    L("Legislative pipeline", "legislative-pipeline.html"),
    L("Research proposals", "research-proposal-processing.html"),
], """
Three examples. Bill passage: a classifier I tuned for precision and warning time, 75.1% precision and 76.2% recall
at a 0.70 threshold on a held-out Assembly. UIC enrollment: a model that flags students at risk of discontinuing,
about 82% accuracy, grouped into high, medium and low tiers for advisors. There the team's comparison chose H2O over CatBoost because its
error stayed under 5% for every class, while CatBoost missed 47.71% of the Discontinued class, the one that mattered
most. Research proposals: every SPA proposal and award is classified into HERDS research fields automatically.
""")

card(EX, "ex-performance-engineering", "An example of performance engineering", [
    "tell me about your performance engineering",
    "example of performance engineering",
    "where did you do performance engineering",
    "have you done performance engineering",
    "show me performance engineering work",
    "tell me about a time you made something faster",
    "how have you optimized inference",
    "have you sped up a model",
    "example of being a performance engineer",
    "performance engineer experience",
], ["performance engineering", "throughput", "gpu", "vllm", "optimization", "speedup", "benchmark", "latency"], [
    L("vLLM vs Ollama throughput study", "archival-image-throughput-evaluation.html"),
    L("vLLM multi-model sweep", "vllm-inference-throughput-evaluation.html"),
    LAB_LINK,
], """
The clearest example: an archival image job on a single NVIDIA L4 was going to take 22 hours, with the GPU only 28%
busy. I ran a controlled benchmark that held the model and hardware fixed and varied the serving stack and concurrency,
and found the bottleneck was request serialization in Ollama, not the GPU or the model. Moving to vLLM's continuous
batching gave a 6.22x speedup at concurrency 8 on the same card: 22 hours down to 3.7, GPU use up to 97%. I then ran
a multi-model sweep on vLLM for the legislative pipeline (chunk size, concurrency, telemetry, SLO gate) to pick and size
the production model. Both studies are in my Applied AI Lab.
""")

card(EX, "ex-capacity-planning", "Sizing hardware and capacity planning", [
    "how many gpus do we need",
    "have you done capacity planning",
    "how do you size hardware for an llm",
    "how do you decide what gpu to use",
    "how would you size infrastructure for inference",
    "how far does one gpu go",
    "what hardware does a local model need",
    "slo and capacity planning",
], ["capacity planning", "gpu", "hardware", "sizing", "slo", "l4", "a100", "throughput"], [
    L("vLLM sweep: SLO gate", "vllm-inference-throughput-evaluation.html#slo-gate"),
    L("Document intelligence: hardware", "document-intelligence-evaluation.html"),
], """
I size from measured throughput at the real load, not the spec sheet. For the legislative pipeline I measured Llama
3.1 8B AWQ on one NVIDIA L4 and ran an SLO gate: closing the steady-state gap takes about 3 L4s in parallel or one
A100-class GPU, and peak bursts need about 7 L4s or H100-class hardware. Quality stayed within 0.6 points from
concurrency 1 to 24, so the recommendation was concurrency 12 to 24. For document intelligence I sized every model for a
single L4 (24 GB) or L40S (48 GB), one model on the card at a time, and measured all of them on the same 32 GB desktop so
speeds compare fairly.
""")

card(EX, "ex-model-evaluation", "Examples of model evaluation", [
    "show me an example of a model evaluation",
    "have you evaluated models",
    "model evaluation experience",
    "how have you compared llms",
    "tell me about a model evaluation you ran",
    "have you benchmarked llms",
    "examples of model selection work",
    "where are your model evaluations",
    "model evaluation website",
], ["model evaluation", "benchmark", "model selection", "llm", "open weight", "comparison", "lab"], [
    L("Document intelligence evaluation", "document-intelligence-evaluation.html"),
    L("Generation model screen", "generation-model-evaluation.html"),
    L("vLLM multi-model sweep", "vllm-inference-throughput-evaluation.html"),
    LAB_LINK,
], """
They are collected in my Applied AI Lab. Document intelligence: eleven open-weight models across seven frozen tasks
(OCR, tables, charts, whole pages, layout, contract clauses), 40,975 scored rows, winners confirmed on data no model had
seen, and no model grading another. Rule-bound generation: seven local configurations screened on a generator's own
checks under a rule written before the run, then replicated on 60 new groups. Legislation extraction: Mistral, Qwen 2.5
and Llama 3.1 8B AWQ on vLLM, where Llama won with a 20+ point lead in parse-OK. Each study says how it was measured
and what it does not show.
""")

card(EX, "ex-document-intelligence", "Document intelligence: which local model reads what", [
    "tell me about the document intelligence evaluation",
    "which model is best for reading documents",
    "which model should read our documents",
    "best local model for ocr tables and charts",
    "document intelligence on one gpu",
    "how do you extract data from pdfs",
    "can ai read tables in pdfs",
], ["document intelligence", "ocr", "tables", "charts", "pdf", "local models", "evaluation", "paddleocr", "qwen"], [
    L("Case study", "document-intelligence-evaluation.html"),
    LAB_LINK,
], """
Proposals, contracts, awards and reports keep their most useful facts in scans, budget tables, charts and buried
clauses, and many can't leave the organization. So I tested which open model, on one L4 or L40S, can be trusted with
which part. There is no single winner. On fresh data, the 0.9B PaddleOCR-VL-1.6 beat Qwen3-VL 32B on financial tables
(0.852 vs 0.762 TEDS, 97.4% numeric recall). Nemotron 3.5 Parse wrote the best page text. The same self-check prompt
moved one model up 26.5 points and another down 43.5 on charts. On 60 fresh contracts, local Qwen3 32B answered 18 of 30
entailment questions against 12 for a hosted model.
""")

card(EX, "ex-generation-eval", "Screening local models on a rule-bound generator", [
    "tell me about the generation model evaluation",
    "rule bound generation",
    "how did you pick a model for skyrule generation",
    "did a newer model beat the old one",
    "tell me about the qwen3.8 screen",
], ["generation", "screening", "pre-registration", "ifeval", "qwen", "gemma", "local models", "evaluation"], [
    L("Case study", "generation-model-evaluation.html"),
    LAB_LINK,
], """
Skyrule's generator writes a plan, then the piece, and code checks both, and its yield had stalled at 3 of 20 groups.
I screened seven local model configurations on the real generator, with the prompt, checks and bar held fixed and the
decision rule frozen by hash before any model loaded. Qwen3.8 27B accepted 7 of 20 against the current configuration's
3. A second pre-registered round on 60 new groups replicated it: 24 against 11, an interval of 6.6 to 35.5 points. I
also found a contradiction in the prompt itself, and the public IFEval ranking didn't match the task ranking. It's
eligible for release, not adopted.
""")

card(EX, "ex-choosing-model-process", "My process for choosing a model", [
    "what is your general process for choosing a model",
    "what is your process for choosing a model",
    "how do you pick an llm",
    "how do you select a model",
    "how do you decide which llm to use",
    "how do you choose the right model for a task",
    "model selection process",
    "how do you choose a model",
    "model selection",
    "which model should we use",
    "how do you evaluate which model to use",
    "how do you choose between llms",
    "choosing between models",
    "how would you pick a model for our use case",
], ["model selection", "process", "choose", "llm", "evaluation", "method", "decision rule"], [
    L("Choosing a local model (guide)", "choosing-local-models-guide.html"),
    L("How I choose between models", "uic-enrollment.html#models"),
    LAB_LINK,
], """
First, I find candidates that fit the hardware at the context, output length and concurrency we need, and I check each
licence, with the current model as the baseline. Second, I turn the real task into a frozen test with code-based checks,
keeping failures and timeouts in the denominator. Third, I write the decision rule before the run: the primary measure,
the minimum useful improvement, and what a pass earns. Then I check that the harness reproduces the baseline, change
one thing at a time, and confirm any winner on fresh cases. Size and benchmark scores are only a starting point: a
smaller model beat a bigger one in two of my evaluations.
""")

card(EX, "ex-small-vs-big-model", "Why a smaller model can beat a bigger one", [
    "is a bigger model always better",
    "why would a smaller model beat a bigger one",
    "do we need the biggest model",
    "do parameters matter",
    "small model vs large model",
    "is a bigger llm better",
    "are bigger models better",
], ["model size", "parameters", "small model", "large model", "model selection"], [
    L("Choosing a local model (guide)", "choosing-local-models-guide.html"),
    L("Document intelligence", "document-intelligence-evaluation.html"),
], """
No. In my document evaluation, the 0.9B PaddleOCR-VL-1.6 beat Qwen3-VL 32B on financial tables, 0.852 vs 0.762 TEDS.
In my generation screen, Qwen3.8 27B accepted 7 of 20 groups against 3 for the larger Qwen3-32B, and held up on 60 new
groups. Size sets capacity. It doesn't tell you how well a model was trained or how well it fits your task. Training
recipe, quantization, server and chat template all change behaviour: the same 32B accepted 3 groups under one backend
and 1 under another. A model that fits fully on the card also runs faster, which matters when a pipeline retries.
""")

card(EX, "ex-public-benchmarks", "What public benchmarks can and can't tell you", [
    "can we trust public benchmarks",
    "are leaderboards useful",
    "should we pick a model from a leaderboard",
    "do benchmark scores predict real performance",
    "what about ifeval and mmlu",
], ["benchmarks", "leaderboard", "ifeval", "contamination", "model selection"], [
    L("Choosing a local model (guide)", "choosing-local-models-guide.html#benchmarks"),
], """
I use them to build a shortlist, never as the verdict. In my generation screen, Gemma 4 had the highest IFEval score of
the four models completed, 0.900, and accepted 0 of 20 task groups. Qwen3.8 had the lowest IFEval score, 0.806, and
accepted the most. Benchmarks only compare fairly when the harness, template and decoding settings match. Public test
material can also leak into training data. So the real test is your own task, frozen, with code-based checks.
""")

card(EX, "ex-fine-tuning", "Fine-tuning", [
    "have you fine tuned a model",
    "fine tuning experience",
    "do you do fine tuning",
    "have you used lora",
    "have you used qlora",
    "when should we fine tune",
    "should we fine tune or use rag",
], ["fine tuning", "lora", "qlora", "training", "adapters", "dpo"], [
    L("Choosing a local model (guide)", "choosing-local-models-guide.html#finetune"),
], """
I treat fine-tuning as the last lever, not the first. My order is: fix the instructions and checks, switch or route
models, add retrieval or tools if the gap is knowledge, and only then fine-tune, once the best prompt and model still
miss the bar and there are enough good examples. My guide covers LoRA and QLoRA on one GPU, rejection-sampling and
preference tuning, and how to validate a tuned model without it just learning the checks. A fine-tuning experiment
following that method is designed for my generation screen. I'll publish the results when it finishes.
""")

card(EX, "ex-local-vs-hosted", "Local models vs hosted APIs", [
    "local models or openai",
    "should we self host or use an api",
    "open source models vs hosted models",
    "why do you use local models",
    "when would you use a cloud llm",
    "are local models good enough",
], ["local", "hosted", "self hosted", "open weight", "api", "privacy", "cost"], [
    L("Document intelligence", "document-intelligence-evaluation.html"),
    L("Legislative platform", "legislative-pipeline.html"),
    L("Email archiving", "email-archiving.html"),
], """
It depends on the data and the job, and I've shipped both. Sensitive data stays local: the email archive, legacy
files and archival images never touch an external API. The legislative platform uses local Llama for bulk extraction and
a GPT-4.1 Copilot agent for the citation-backed chatbot. Local is not automatically worse. On 60 fresh contract documents, local
Qwen3 32B answered 18 of 30 entailment questions against 12 for a hosted model. Starting on-prem also let the team
experiment freely after a short Azure run got expensive fast.
""")

card(EX, "ex-data-engineering", "Examples of data engineering", [
    "show me an example of data engineering",
    "example of data engineering",
    "have you built data pipelines",
    "data engineering experience",
    "tell me about a data pipeline you built",
    "have you been a data engineer",
    "have you done etl",
    "what pipelines have you built",
    "tell me about your data engineering",
    "data engineering work you have done",
], ["data engineering", "pipeline", "etl", "ingestion", "oracle", "parquet", "cron", "batch"], [
    L("Research proposal processing", "research-proposal-processing.html"),
    L("Legislative pipeline", "legislative-pipeline.html"),
    L("Email archiving", "email-archiving.html"),
    LAB_LINK,
], """
I was hired as a Data Engineer, and pipelines are still most of my work. Research proposals: live Oracle data through an
11-step NLP chain and back into Oracle, unattended on a schedule, for every SPA proposal and award at UIUC and UIC. The
legislative pipeline ingests bills daily, extracts features with a local LLM and predicts passage. Email archiving
processed 44,677 .eml files (79,676 messages). Procurement handled 6 million catalog rows. Since August 2026 I've led
the RIMS build that unifies three archival proofs of concept into one eight-stage pipeline: 2,375 real files in about 21
seconds.
""")

card(EX, "ex-etl-pipeline", "An end-to-end ETL pipeline in production", [
    "example of an etl pipeline",
    "have you built an etl pipeline in production",
    "walk me through a production pipeline",
    "have you written back to a database",
    "have you worked with oracle data",
], ["etl", "oracle", "pipeline", "production", "writeback", "cron", "idempotent"], [
    L("Research proposal processing", "research-proposal-processing.html"),
    L("GitHub", "https://github.com/tayler-erbe/research-proposal-processing"),
], """
The research proposals pipeline. It connects to live Oracle databases and pulls proposal attachments stored as BLOBs. It
runs an 11-step NLP chain (TF-IDF, KeyBERT and LDA fusion, then HERDS classification) and writes structured results back
to Oracle. It runs unattended on a cron schedule, with idempotent writes and a printed rollback. It covers every SPA
research proposal and award across UIUC and UIC, and it's the foundation for the Research Proposal Intelligence
platform supporting the System's ~$517M annual research portfolio. I scoped, designed and built it end to end.
""")

card(EX, "ex-document-processing", "How I process documents", [
    "how do you process documents",
    "document processing experience",
    "how do you turn documents into data",
    "proposal document processing",
    "how do you handle pdfs and scanned documents",
    "intake pipeline",
    "proposals and awards with evidence",
], ["document processing", "documents", "pdf", "extraction", "intake", "proposals", "evidence", "pipeline"], [
    L("Research proposal processing", "research-proposal-processing.html"),
    L("Document intelligence", "document-intelligence-evaluation.html"),
    LAB_LINK,
], """
I treat a document as several extraction problems: running text, tables, charts, flattened spreadsheets and clause
evidence, each with its own test. My production proposal pipeline turns attachments into annotated, classified text
analysts can query by research field. The next step is a system design in my Lab for reading proposals and awards with local models and showing the evidence for every value. The model picks block IDs and code copies the source text, so nothing is paraphrased. The
intake pipeline design runs one stage and one model at a time on a single GPU, with nothing overwritten. That one is
design only so far: tested on fictional documents, accuracy not yet measured.
""")

card(EX, "ex-solutions-architecture", "An example of AI solutions architecture", [
    "example of ai solutions architecture",
    "have you been a solutions architect",
    "tell me about a system you architected",
    "show me an architecture you designed",
    "how do you design an ai system",
    "end to end ai system design example",
    "ai architect experience",
], ["architecture", "solutions architect", "system design", "end to end", "azure", "routing"], [
    L("Legislative platform", "legislative-pipeline.html"),
    L("Procurement intelligence", "procurement-intelligence.html"),
    L("Agent architecture", "agent-architecture.html"),
], """
The Legislative Intelligence Platform. I designed the architecture, pipelines, models, cloud infrastructure,
application and documentation: daily ingestion, 12+ LLaMA-extracted signals per bill, hybrid FAISS search, a GPT-4.1
chatbot with citations, and a Streamlit app on Azure App Service. It was our team's first production cloud AI
deployment. Procurement is a good routing example: exact part-number matching first, FAISS semantic retrieval second,
and an LLM only for the equivalence judgment, with prices compared in code. Skyrule's agent architecture is the
personal-project version: 29 agents on one queue, one memory and one ownership map.
""")

card(EX, "ex-forward-deployed", "Forward-deployed work with stakeholders", [
    "example of forward deployed engineering",
    "have you worked directly with clients",
    "have you worked directly with stakeholders",
    "tell me about building something for a stakeholder",
    "have you embedded with a business team",
    "client facing experience",
    "have you worked with customers",
], ["forward deployed", "stakeholders", "clients", "customers", "requirements", "delivery"], [
    L("Archival image intelligence", "archival-image-intelligence.html"),
    L("HR workforce analytics", "hr-workforce-analytics.html"),
    L("Drop Radar", "drop-radar.html"),
], """
Most of my work starts with someone's problem. RIMS reached out in December 2024, and the email archive was scoped in a working meeting with the University Archivist. Since August 2026 I've led the production build with the University Library, mentoring their
engineer toward full ownership. When HR lost its retirement-risk report with its KNIME platform, I rebuilt it in Python
and delivered the overdue report the same day. Outside work, I built Drop Radar for my husband over one weekend. He
judged the early alerts low-value, so I reset the design within a day and built in a weekly feedback check-in.
""")

card(EX, "ex-ai-consulting", "Examples of AI and data consulting", [
    "example of being a data consultant",
    "tell me an example of how you have been a data consultant",
    "have you done ai consulting",
    "example of ai consulting",
    "have you advised an organization on ai",
    "tell me about a recommendation you made",
    "consulting experience",
    "have you been a consultant",
], ["consulting", "consultant", "advisory", "recommendation", "trade-offs", "strategy"], [
    L("Procurement intelligence", "procurement-intelligence.html"),
    L("Data readiness framework", "https://github.com/tayler-erbe/enterprise-data-readiness-framework"),
    L("Choosing a local model (guide)", "choosing-local-models-guide.html"),
    LAB_LINK,
], """
Procurement is my best example. The raw savings figure was $317,583, and I showed 49.1% of it was pack-size inflation.
The defensible number was $161,564, documented and downloadable so anyone could check it. I also wrote the Enterprise
Data Readiness Framework, which scores every table from undocumented to AI-ready before data moves to a new system. My
"Charts Without Guesswork" brief recommends computing accessible chart descriptions from the data, not from AI. My
local-model guide is advice for teams picking their first open-weight model. In each one, I make the trade-offs plain
and give a recommendation someone can act on.
""")

card(EX, "ex-where-ai-adds-value", "Deciding where AI is worth using, and where it isn't", [
    "how do you decide where ai adds value",
    "when should you not use ai",
    "when is ai the wrong tool",
    "should we use ai for this",
    "how do you decide whether a problem needs an llm",
    "do you always use llms",
    "how do you avoid overusing ai",
], ["ai value", "when not to use ai", "deterministic", "rules", "llm", "judgment"], [
    L("Procurement intelligence", "procurement-intelligence.html"),
    L("Charts without guesswork", "https://tayler-erbe.github.io/semantic-visualizations-for-access/brief/"),
    L("Medium: messy data", "https://medium.com/@tayler.erbe/stop-throwing-ai-at-your-messy-data-heres-what-to-do-instead-3b0875aed908"),
], """
I use code where code is reliable, and a model only for the part that needs judgment. In procurement, exact part-number
matching came first (about 42,000 pairs), semantic search second, and the LLM only decided whether two products were
equivalent. Prices were compared in code, never by the model. For accessible charts, my first version used AI, and I
rebuilt it so every description is calculated from the chart's own data, because research shows AI still gets chart
facts wrong. Drop Radar alerts but never buys. I wrote about this on Medium as "stop throwing AI at your messy data".
""")

card(EX, "ex-agentic-workflows", "Agentic workflows I've built", [
    "example of an agentic workflow",
    "have you built agentic workflows",
    "have you built ai agents",
    "tell me about your agents",
    "multi agent system example",
    "have you used claude code agents",
    "multi-agent experience",
    "multi agent systems",
], ["agents", "agentic", "multi agent", "claude code", "orchestration", "job queue", "automation"], [
    L("Agent architecture", "agent-architecture.html"),
    L("Skyrule", "skyrule.html"),
    L("Drop Radar", "drop-radar.html"),
], """
Two in production on my own machine. For Skyrule and my other personal projects I run 29 agents with written charters.
They share one job queue, one memory, one decision log and an ownership map that tooling enforces. As of October 19,
2026, the queue had finished 1,060 jobs and 1,496 of 1,499 product tests were passing. Drop Radar has a self-improving
loop. My husband texts a note, a Claude Code agent reads it, edits the code or source list, runs the tests, restarts the
service and replies with what changed. He never touches a line of code.
""")

card(EX, "ex-agent-guardrails", "How I keep agents governed and safe", [
    "how do you keep ai agents under control",
    "how do you stop agents breaking things",
    "how do you govern multiple agents",
    "what can your agents not do",
], ["agents", "guardrails", "governance", "charters", "permissions", "quality gate", "security"], [
    L("Agent architecture: governance", "agent-architecture.html"),
], """
Every agent has a written charter that says what it owns, what it may do and what it may not, and tooling enforces the
ownership map. A quality agent and a security agent can block a merge or release in writing, but can't make the release
decision. An overseer checks every agent hourly but can't restart or delete anything. Big jobs wait for my approval, and I
had logged 294 founder decisions by mid-October 2026. Generated claims pass code validators before I review them.
""")

card(EX, "ex-rag-example", "Retrieval-augmented generation (RAG) in practice", [
    "example of rag",
    "have you built a rag system",
    "retrieval augmented generation example",
    "have you built a chatbot over documents",
    "have you built a chatbot",
    "have you made a chatbot",
    "have you built chatbots",
    "have you used rag",
], ["rag", "retrieval", "chatbot", "faiss", "citations", "semantic search", "vector search"], [
    L("Legislative platform", "legislative-pipeline.html"),
    L("Legacy file search", "file-archiving-smart-search.html"),
    L("Procurement intelligence", "procurement-intelligence.html"),
], """
The legislative platform's GPT-4.1 Copilot answers questions about Illinois and federal legislation from hybrid FAISS
retrieval, with a citation behind every answer. Legacy file search embeds LLaMA summaries of 15+ file types into a FAISS
HNSW index and returns exact Box file paths for a plain-language question. Procurement retrieves over 5.19 million
embeddings, with the similarity threshold calibrated on 20 to 30 hand-picked queries. This chat is the deliberately
simple opposite: pre-written answers searched in your browser, with no model at all.
""")

card(EX, "ex-nlp", "Natural language processing projects", [
    "example of an nlp project",
    "nlp experience",
    "have you done natural language processing",
    "text analytics experience",
    "have you done text mining",
    "have you done sentiment analysis",
], ["nlp", "natural language processing", "text", "keywords", "topics", "classification", "sentiment"], [
    L("Research proposal processing", "research-proposal-processing.html"),
    L("Email archiving", "email-archiving.html"),
], """
Research proposals: TF-IDF, KeyBERT and LDA fused into keywords, plus spaCy entities and HERDS research-field
classification, running in production on every SPA proposal and award. Email archiving: Presidio entity detection and
anonymization, LLaMA summaries, and LDA topics labeled by an LLM. Legislation: 12+ structured signals extracted per bill
with a local LLM. My first job used NLTK to run sentiment analysis on user posts at Dragonchain.
""")

card(EX, "ex-computer-vision", "Computer vision and multimodal work", [
    "computer vision experience",
    "have you worked with images",
    "example of a vision model project",
    "have you used vision language models",
    "have you done image classification",
], ["computer vision", "images", "vision language model", "llava", "multimodal", "image classification"], [
    L("Archival image intelligence", "archival-image-intelligence.html"),
    L("Historical book OCR", "historical-book-ocr.html"),
    L("Document intelligence", "document-intelligence-evaluation.html"),
], """
Archival images: I compared embedding-similarity classification against LLaVA on sensitive content in historical
collections and scaled it to 12,125 images, with EXIF and IPTC metadata extraction. Legacy files: LLaVA describes
photographs that OCR can't read. Historical books: about 22,700 pages of early print read with self-hosted OCR and vision
models. Document intelligence: vision-language models on tables, charts and whole pages, compared across eleven models.
""")

card(EX, "ex-ocr", "OCR experience", [
    "have you done ocr",
    "ocr experience",
    "optical character recognition",
    "can you read scanned documents",
    "have you used tesseract",
    "how accurate is ocr",
], ["ocr", "scans", "text recognition", "historical", "paddleocr", "olmocr", "nemotron parse"], [
    L("Historical book OCR", "historical-book-ocr.html"),
    L("Document intelligence", "document-intelligence-evaluation.html"),
], """
Yes, at scale and as an evaluation. For Skyrule I read 170 early printed books, about 22,700 pages from the 1480s to the
1850s, on one GPU workstation. Several models read each page, and their disagreement became a per-page quality score that
routes hard pages to review. In my document evaluation, Qwen3-VL 8B reached 1.2% character error on prose crops, as good
as the 32B models. But every model recovered only 96.5% of the numbers, under my 99% bar, so OCR on budgets stays
review-assisted. For the legacy archive, I chose LLaVA over Tesseract because most of the images were photographs, not
scanned text.
""")

card(EX, "ex-tables-charts", "Extracting tables, charts and numbers", [
    "can ai extract tables",
    "table extraction",
    "chart extraction",
    "can a model read charts",
    "extracting numbers from documents",
    "financial table extraction",
], ["tables", "charts", "numbers", "numeric recall", "teds", "extraction"], [
    L("Document intelligence", "document-intelligence-evaluation.html"),
], """
Tables: on 100 fresh financial-report tables, the small PaddleOCR-VL-1.6 beat Qwen3-VL 32B, 0.852 vs 0.762 TEDS with
97.4% numeric recall. Charts: the method matters as much as the model. Self-check lifted one model 26.5 points and sank
another 43.5. Recovering the table behind a chart went from 0.418 to 0.930 value recall with self-check. And I always
report numbers beside text: masking raised word F1 by 0.067 but cut numeric recall by 0.178 on the same pages.
""")

card(EX, "ex-contracts", "Contracts and legal documents", [
    "have you worked with contracts",
    "contract extraction",
    "legal document ai",
    "can you extract clauses",
    "contract analysis experience",
], ["contracts", "legal", "clauses", "cuad", "contractnli", "evidence"], [
    L("Document intelligence: legal track", "document-intelligence-evaluation.html"),
], """
In my document evaluation I tested clause questions on the public CUAD and ContractNLI sets. On 60 fresh contracts,
local Qwen3 32B answered 18 of 30 entailment questions against 12 for a hosted model. I designed an evidence-by-ID
method. The model picks block IDs, code copies the source text and verifies its hash and offset, absent fields are
recorded as absent, and a person reviews with the page beside the answer. That removed every copy failure, but it
doesn't make answers right by itself, so I report correctness and retrieval coverage separately.
""")

card(EX, "ex-structured-extraction", "Structured extraction with LLMs", [
    "have you used llms for extraction",
    "feature extraction with llms",
    "extracting structured data with an llm",
    "llm information extraction example",
], ["extraction", "structured", "json", "llm", "features", "schema"], [
    L("Legislative pipeline", "legislative-pipeline.html"),
    L("vLLM sweep", "vllm-inference-throughput-evaluation.html"),
], """
The legislative pipeline extracts 12+ structured signals per bill with Llama 3.1 8B AWQ on vLLM, and those signals
feed search, trends and the prediction model. Before committing the 11,673-bill, roughly 155-hour unattended backfill, I declared acceptance criteria before any evaluation run, and on vLLM I chose chunk size 1200 because it gave the highest parse-OK of any configuration, 92.5%. Llama was also the only model above 80% at every chunk size.
Procurement normalizes pack sizes into JSON with qwen2.5:7b. My proposals-and-awards design extracts narrative facts with the
evidence beside every value.
""")

card(EX, "ex-privacy", "Working with PII and regulated data", [
    "have you worked with pii",
    "have you worked with sensitive data",
    "hipaa ferpa experience",
    "have you handled confidential data",
    "data privacy experience",
    "have you done anonymization",
    "have you worked with personally identifiable information",
    "personally identifiable information",
    "anonymizing data",
    "anonymization experience",
], ["pii", "privacy", "anonymization", "presidio", "ferpa", "hipaa", "sensitive data", "local"], [
    L("Email archiving", "email-archiving.html"),
    L("Archival image intelligence", "archival-image-intelligence.html"),
], """
Yes. The email archive held 79,676 messages of personal information, so I built two layers: Presidio detects and
anonymizes entities (five strategies), and a local LLaMA writes de-identified summaries. Nothing goes to an external API.
The archival-image categories are grounded in FERPA, HIPAA and NAGPRA. Skyrule never sends personal chart data to a cloud
model. In my Lab, private documents and results from real-document runs stay on approved machines. Only public-benchmark
results, aggregates or design are published.
""")

card(EX, "ex-cost-savings", "Saving money and showing ROI", [
    "have you saved a company money",
    "example of cost savings",
    "roi of your work",
    "how much money have you saved",
    "business value of your projects",
    "how do you prove ai is worth it",
], ["cost", "savings", "roi", "value", "business impact", "procurement"], [
    L("Procurement intelligence", "procurement-intelligence.html"),
    L("Throughput study", "archival-image-throughput-evaluation.html"),
], """
Procurement found $161,564 in defensible, unit-normalized savings, counting only products where two of the four distributors had prior-year purchase quantities, after I removed the 49.1%
pack-size inflation from the raw $317,583. The tool's estimated production cost is about $77 a month. The vLLM migration
cut a 22-hour job to 3.7 hours on the same GPU, with no new hardware. For bill prediction I reported what leadership can
use, not just an AUC: right about 75% of the time when it flags a bill, typically three weeks before the vote. I show the
floor, not the guess.
""")

card(EX, "ex-executive-stakeholders", "Working with executives and leadership", [
    "have you presented to executives",
    "executive stakeholder experience",
    "have you worked with c suite",
    "how do you present to leadership",
    "who have you presented to",
    "examples of executive presentations",
    "presenting to leadership",
], ["executives", "leadership", "stakeholders", "presentations", "governance", "committees"], [
    L("Experience", "index.html#experience"),
], """
I present regularly to executive leadership, governance committees and the Enterprise Architecture Committee, and I'm a
member of the university-wide Generative AI Committee. Stakeholders on the legislative platform include the AVP Academic
Affairs, IGPA and the AVP External & State Relations. I presented the enrollment work to UIC leadership. I'm the sole
author of governance dossiers for the SPA Research Funding and Workforce Analytics platforms: leadership briefings, ROI
defenses, data inventories and stakeholder discovery.
""")

card(EX, "ex-discovery-scoping", "How I scope a project with stakeholders", [
    "how do you gather requirements",
    "how do you scope a project",
    "how do you start a new ai project",
    "how would you approach our problem",
    "what is your process for a new engagement",
    "how do you work with a client from the start",
], ["scoping", "requirements", "discovery", "process", "engagement", "proof of concept"], [
    L("Email archiving", "email-archiving.html"),
    L("HR workforce analytics", "hr-workforce-analytics.html"),
    L("Document intelligence: the problem", "document-intelligence-evaluation.html"),
], """
I start by defining the problem precisely, then the measure, and only then the model. For document intelligence I
wrote down what "solved" meant first: numbers right, source page attached, and the system says when it's unsure. For
the email archive, I scoped the work with the University Archivist and RIMS before building. The HR platform ran as
deliberate proof-of-concept phases that validated each model and data mapping before any platform build. I build the
cheapest reliable baseline first, measure it, and check back with the people who'll use it.
""")

card(EX, "ex-rapid-prototyping", "Building fast", [
    "how fast can you build something",
    "rapid prototyping example",
    "have you built something quickly",
    "can you move fast",
], ["rapid prototyping", "speed", "fast", "weekend", "deadline"], [
    L("Drop Radar", "drop-radar.html"),
    L("HR workforce analytics", "hr-workforce-analytics.html"),
], """
Drop Radar went from nothing to live in one weekend: 357 commits, about 3,300 lines of standard-library Python in 12
modules, 25 automated tests. It has run 24/7 since October 22, 2026. At work, when the retirement-risk report was lost
with its platform, I rebuilt it end to end in Python and delivered the overdue report the same day, correcting
statistical defects along the way. Fast doesn't mean unchecked. Both have tests and monitoring.
""")

card(EX, "ex-production-deployment", "Deploying AI to production", [
    "have you deployed models to production",
    "have you shipped ai to production",
    "production ai experience",
    "is any of your work in production",
    "what is running in production",
], ["production", "deployment", "azure", "cron", "linux", "monitoring", "shipped"], [
    L("Legislative platform", "legislative-pipeline.html#prod"),
    L("Research proposal processing", "research-proposal-processing.html"),
], """
Yes. The Legislative Intelligence Platform has been live on Azure App Service since its delivery to IGPA in August
2026. It was our team's first production cloud AI deployment, and its pipeline runs daily on our Linux analytics server.
The research proposals pipeline runs unattended on a cron schedule for SPA across UIUC and UIC. The retirement-risk
forecast runs quarterly under monitoring. I architected the Linux AI execution environment behind all our production
pipelines and the monitoring that watches them.
""")

card(EX, "ex-monitoring", "Monitoring and observability", [
    "observability experience",
    "have you built monitoring",
    "how do you know when a pipeline fails",
    "alerting experience",
], ["monitoring", "observability", "alerting", "health checks", "logging", "silent failures"], [
    L("Medium: monitoring", "https://medium.com/@tayler.erbe/i-got-tired-of-pipelines-failing-silently-so-i-built-my-own-monitoring-system-e8224fe22387"),
    L("Drop Radar", "drop-radar.html"),
    L("Agent City", "agent-city.html"),
], """
I built a job execution monitor for every scheduled pipeline on our analytics server. Each pipeline writes structured
Parquet logs, and the monitor reads them every 30 to 60 minutes. It catches script failures, cascade failures, missed
runs and pipelines that have gone silent, then emails a diagnostic with the traceback. It works like a lightweight
MLflow or Airflow equivalent. In Drop Radar, the Discord feed only counts as healthy when a followed post actually arrived in the last 24 hours. Running without errors isn't enough. For my agents, Agent City is a 3D town that shows me what they're doing.
""")

card(EX, "ex-data-readiness", "Is your data ready for AI?", [
    "is our data ready for ai",
    "data readiness",
    "enterprise data readiness framework",
    "semantic layer",
    "text to sql on enterprise data",
    "data governance for ai",
    "how do you prepare data for ai",
], ["data readiness", "semantic layer", "governance", "metadata", "text to sql", "data catalog"], [
    L("Framework (GitHub)", "https://github.com/tayler-erbe/enterprise-data-readiness-framework"),
    LAB_LINK,
], """
Most enterprise data isn't ready for AI. Not because it's wrong, but because nobody has written down what it means in a
form a machine can use. Tools like Snowflake Cortex Analyst, Databricks Genie and Power BI Copilot are only as accurate
as the semantic layer under them. My framework scores every table from 0 (undocumented) to 4 (AI-ready), mostly with
deterministic checks. AI drafts what's missing, labeled unconfirmed and routed to the table's owner, and it publishes a
portable semantic layer tested with questions whose answers are known. The research is complete and a prototype scorer
is next.
""")

card(EX, "ex-accessibility", "AI and accessibility", [
    "accessibility work",
    "accessible charts",
    "ai for accessibility",
    "charts without guesswork",
    "have you worked on accessibility",
], ["accessibility", "charts", "screen reader", "a11y", "descriptions"], [
    L("Charts Without Guesswork (brief)", "https://tayler-erbe.github.io/semantic-visualizations-for-access/brief/"),
    L("GitHub", "https://github.com/tayler-erbe/semantic-visualizations-for-access"),
], """
I built accessible chart descriptions for the Legislative Intelligence Platform. My first version used AI. I rebuilt
it so every description is calculated by rules from the chart's own data, next to an accessible data table and an Excel
download. The research backs that up. People checked 1,187 AI chart captions and 82% had at least one factual error, and
blind readers mostly want straight facts about the data, which code computes reliably. My brief, "Charts Without
Guesswork", and a pre-registered evaluation plan are in my Lab.
""")

card(EX, "ex-matching", "Matching records across messy sources", [
    "entity resolution",
    "record linkage",
    "have you matched products across vendors",
    "deduplication experience",
    "fuzzy matching",
], ["matching", "entity resolution", "record linkage", "deduplication", "semantic matching"], [
    L("Procurement intelligence", "procurement-intelligence.html"),
], """
Procurement is my example: 6 million catalog rows from four distributors in three tiers. Exact part-number matching came
first, about 42,000 matched pairs. Then FAISS semantic retrieval over 5.19 million embeddings, with the threshold
calibrated on hand-picked queries. Then an LLM decided equivalence and normalized pack sizes into JSON. Prices were
compared in code, which is how I caught the 49.1% pack-size inflation in the raw savings figure.
""")

card(EX, "ex-semantic-search", "Semantic search", [
    "have you built semantic search",
    "vector search example",
    "search by meaning",
    "have you built a search engine",
], ["semantic search", "vector search", "faiss", "embeddings", "search"], [
    L("Legacy file search", "file-archiving-smart-search.html"),
    L("Legislative platform", "legislative-pipeline.html"),
], """
Legacy file search makes a Box archive of institutional files searchable without anyone opening each file. I extract 15+
file types, summarize them with LLaMA (LLaVA for images), embed the summaries into a 384-dimensional FAISS HNSW index,
and return exact Box paths for a plain-language query. The legislative platform uses hybrid FAISS and keyword search.
Procurement searches 5.19 million product embeddings.
""")

card(EX, "ex-topic-modeling", "Topic modeling", [
    "have you done topic modeling",
    "lda experience",
    "topic modeling example",
], ["topic modeling", "lda", "topics", "clustering", "text"], [
    L("Email archiving", "email-archiving.html"),
    L("Research proposal processing", "research-proposal-processing.html"),
], """
Yes, in two pipelines. In email archiving, LDA found topics across the archive and Llama 3.2 turned
each topic's keywords into a title of five words or fewer, so archivists could read them. In research proposals, LDA
is fused with TF-IDF and KeyBERT so the keywords agree across methods before HERDS classification.
""")

card(EX, "ex-graph-simulation", "Graph analytics and simulation", [
    "have you done graph analytics",
    "network analysis experience",
    "markov chain experience",
    "simulation modeling",
    "community detection",
], ["graph", "network", "markov chain", "simulation", "community detection", "networkx"], [
    L("HR workforce analytics", "hr-workforce-analytics.html"),
], """
In HR workforce analytics I used Markov chain simulation to model career movement, and graph community detection with
NetworkX to find career communities. It shows which roles connect many pathways and which ones isolate employees. Those
fed internal mobility and succession-readiness proofs of concept, with O*NET skill matching.
""")

card(EX, "ex-anomaly-trends", "Anomaly detection and trend analysis", [
    "have you done anomaly detection",
    "trend analysis example",
    "have you detected anomalies",
], ["anomaly detection", "z-score", "trends", "tf-idf", "momentum"], [
    L("Legislative platform", "legislative-pipeline.html"),
], """
The legislative dashboard on Azure uses Z-score anomaly detection to surface unusual legislative activity, TF-IDF trend
analysis to show which topics are rising, and subcategory momentum modeling. They sit beside the passage predictions so
users see what's moving, not just what might pass.
""")

card(EX, "ex-dashboards-apps", "Dashboards and applications I've built", [
    "have you built dashboards",
    "have you built web apps",
    "have you built a user interface",
    "dashboard experience",
    "full stack experience",
    "what apps have you built",
], ["dashboards", "apps", "streamlit", "fastapi", "web", "pwa", "ui"], [
    L("Legislative web application", "legislative-web-application.html"),
    L("Procurement intelligence", "procurement-intelligence.html"),
    L("Legacy app", "legacy-app-about.html"),
], """
The legislative platform is a live Streamlit application on Azure, with personalized impact ratings, team sharing and
AI email digests. Procurement has a price comparison tool (search, browse by category or manufacturer) on FastAPI, and a
spending dashboard for leadership. Legacy is an installable, offline-first iPhone web app. Drop Radar has a GitHub Pages
dashboard and a Telegram bot interface.
""")

card(EX, "ex-real-time", "Real-time systems", [
    "have you built real time systems",
    "real time alerting",
    "streaming data experience",
    "websocket experience",
], ["real time", "alerts", "streaming", "websocket", "latency"], [
    L("Drop Radar", "drop-radar.html"),
], """
Drop Radar watches about 40 sources around the clock and alerts a phone within seconds. I moved its Discord feed from
10-second REST polling to Discord's official Gateway, using a websocket client I wrote on the Python standard library
with heartbeat, resume and dead-connection detection. Posts now arrive in about a second, with polling as an automatic
fallback. An arrival log records every alert's upstream post time, detection time and send time.
""")

card(EX, "ex-project-leadership", "Leading a technical project", [
    "have you led a project",
    "example of technical leadership",
    "have you been a tech lead",
    "have you managed a project",
    "project management experience",
], ["leadership", "tech lead", "project management", "architect", "mentoring"], [
    L("Archival image intelligence", "archival-image-intelligence.html"),
    L("Experience", "index.html#experience"),
], """
Since August 2026 I've been technical lead, architect and project manager for the RIMS archival pipeline production
build, across AITS and the University Library. I unified three proofs of concept into one eight-stage pipeline,
demonstrated in September 2026 on 2,375 real files in about 21 seconds. I'm also mentoring the Library's engineer toward
full ownership. I've functionally led the Advanced Analytics team since early 2023: architecture, delivery,
prioritization, governance and executive engagement. I've recruited and mentored 7+ data science interns.
""")

card(EX, "ex-poc-to-production", "Taking a proof of concept to production", [
    "have you taken a poc to production",
    "how do you productionize a prototype",
    "prototype to production example",
], ["proof of concept", "production", "prototype", "productionize"], [
    L("Archival image intelligence", "archival-image-intelligence.html"),
    L("Legislative platform", "legislative-pipeline.html"),
], """
The RIMS pipeline started as three separate proofs of concept: email archiving, archival images and legacy file
search. I'm now leading the production build that unifies them into one eight-stage pipeline the Library will own. The
legislative work went from prototype to a platform delivered to IGPA on Azure, and the prediction model was then validated on a held-out Assembly. On the way, the throughput fix (22 hours to 3.7) is what made production runs practical.
""")

card(EX, "ex-modernization", "Migrating and modernizing legacy systems", [
    "have you migrated a legacy system",
    "modernization experience",
    "have you migrated from knime",
    "have you replaced an old platform",
], ["migration", "modernization", "legacy", "knime", "python", "vllm"], [
    L("HR workforce analytics", "hr-workforce-analytics.html"),
    L("Throughput study", "archival-image-throughput-evaluation.html"),
], """
When the retirement-risk forecast was lost with its KNIME platform, I rebuilt it end to end in Python, corrected its
statistical defects and put it on a monitored quarterly schedule. KNIME-to-Python migration is part of my work more broadly. I
migrated inference from Ollama to vLLM for a 6.22x speedup on the same GPU. The archival work is part of the university's
ERP modernization.
""")

card(EX, "ex-responsible-ai", "Responsible AI in practice", [
    "how do you approach responsible ai",
    "ai ethics in your work",
    "how do you make sure ai is used responsibly",
    "ai safety in your projects",
], ["responsible ai", "ethics", "consent", "human review", "terms of service", "privacy"], [
    L("Drop Radar: what it will not do", "drop-radar.html"),
    L("Email archiving", "email-archiving.html"),
], """
Concretely: before building Drop Radar I read the terms of all 22 stores my husband buys from. None permits automated
checkout, so it only alerts, never scrapes where scraping is forbidden, and never hides behind proxies. Sensitive data
stays local, and the archive categories are grounded in FERPA, HIPAA and NAGPRA. People stay responsible for decisions
that affect someone's life. In Skyrule, storing any third-party data requires consent, and I review outputs before
release.
""")

card(EX, "ex-honest-evaluation", "How I keep evaluations honest", [
    "how do you keep your results honest",
    "how do you avoid fooling yourself",
    "what are the lab rules",
    "how do you make benchmarks trustworthy",
    "do you pre register experiments",
    "pre registration",
], ["evaluation", "pre-registration", "honesty", "rigor", "method", "lab rules"], [
    L("Applied AI Lab: how it works", LAB + "#rules"),
    L("Generation model screen", "generation-model-evaluation.html"),
], """
Six rules in my Lab. Only public data or design gets published. The method is fixed before results: prompts, scoring,
thresholds and decision rules are written down first, and a change means a new, labeled protocol. Every attempt counts,
so errors, timeouts and truncations stay as failures. Code checks accuracy against labels, not another model. Speed is
measured at real load with GPU telemetry. Each page says what it does not show. My generation screen froze its rule by
hash before any model loaded.
""")

card(EX, "ex-applied-ai-lab", "My Applied AI Lab", [
    "what is the applied ai lab",
    "tell me about your lab",
    "document intelligence lab",
    "your other website",
    "what is on your lab site",
    "where are your studies",
], ["lab", "applied ai lab", "studies", "website", "evaluation", "document intelligence lab"], [
    LAB_LINK,
], """
It's my second site, where I collect my AI engineering work: 16 studies, briefs and system designs, filterable by
practice area. Those areas are model evaluation, performance engineering, data engineering, solution architecture and AI
consulting. Most studies are sized for a single local GPU, and no private documents are published. Each study answers a
practical question, like which model should read your documents, or why a GPU sits idle and how to fix it.
""")

card(EX, "ex-what-i-can-help-with", "What I can help a team with", [
    "what problems can you help us solve",
    "what can you do for my company",
    "what kind of work can you do for us",
    "what services do you offer",
    "why should we hire you",
    "what would you bring to our team",
], ["services", "help", "hire", "strengths", "capabilities", "what i do"], [
    L("About", "index.html#about"),
    LAB_LINK,
], """
Five kinds of work. Data engineering: pipelines that turn documents and databases into data people can check. Performance
engineering: benchmarking, throughput, GPU use and cost, like the 6.22x speedup on one GPU. AI solutions architecture:
model selection, infrastructure and deployment, like the legislative platform on Azure. Forward-deployed engineering:
working directly with the people who have the problem and building what they need. AI consulting: making trade-offs plain
and recommending what's worth building. I own projects from discovery through delivery and stay close to the evidence.
""")

card(EX, "ex-industries", "Domains and industries I've worked in", [
    "what industries have you worked in",
    "what domains do you know",
    "do you have industry experience",
    "have you worked outside higher education",
    "what sectors have you worked in",
], ["industries", "domains", "higher education", "government", "policy", "hr", "procurement", "archives"], [
    L("Projects", "index.html#projects"),
], """
Most of my work is for a large public university system, but the problems cross industries. Government and policy:
legislation tracking and prediction. Research administration: proposals and awards. HR and workforce: attrition,
succession and retirement forecasting. Procurement and purchasing: cross-vendor price comparison. Records and archives:
privacy-preserving email, image and file processing. Earlier I analyzed economic growth from nighttime light data, and
did sentiment analysis at a blockchain startup. On my own: consumer apps and retail alerting.
""")

card(EX, "ex-unstructured-data", "Working with messy, unstructured data", [
    "have you worked with unstructured data",
    "messy data experience",
    "how do you deal with messy data",
    "dirty data example",
], ["unstructured data", "messy data", "data cleaning", "documents", "email"], [
    L("Procurement intelligence", "procurement-intelligence.html"),
    L("Legacy file search", "file-archiving-smart-search.html"),
], """
It's most of what I do: 44,677 email files, 12,125 historical images, legacy archives of 15+ file types, 22,700 pages of
early print, and 6 million catalog rows with inconsistent pack sizes. The bill dataset was missing every resolved bill
until I rebuilt it. My rule is to clean and match deterministically first and use AI only where judgment is needed. I
wrote about it on Medium as "stop throwing AI at your messy data".
""")

card(EX, "ex-cost-of-llms", "Keeping LLM costs down", [
    "how do you reduce llm costs",
    "llm cost optimization",
    "how do you keep inference cheap",
    "token costs",
], ["cost", "llm", "tokens", "caching", "routing", "inference"], [
    L("Thinking about cost", "procurement-intelligence.html#stack"),
    L("Generation model screen", "generation-model-evaluation.html"),
], """
Route each task to the cheapest model that meets its quality bar, measured on our own hardware. Cache LLM responses by
prompt hash, so repeated queries cost nothing. Build indexes offline once and reuse them. Fix the serving layer before
buying hardware: continuous batching cut a 22-hour job to 3.7 hours on the same GPU. Count cost per successful case, not
per call. In my generation screen, the best configuration used about a quarter of the output tokens per accepted group.
""")

card(EX, "ex-uncertainty", "When the model isn't sure", [
    "what happens when the model is unsure",
    "how do you handle low confidence",
    "how do you handle errors in ai output",
    "when do you send things to human review",
], ["uncertainty", "confidence", "human review", "routing", "quality"], [
    L("Historical book OCR", "historical-book-ocr.html"),
    L("Document intelligence", "document-intelligence-evaluation.html"),
], """
I make the system say so, and route those cases to a person. In historical OCR, several readers' disagreement becomes a
per-page quality score: the hard pages go to stronger readers, and the hardest go to a review queue. In document
intelligence, numeric recall was 96.5% against a 99% bar, so that route is review-assisted, not unattended. Absent fields
are recorded as absent, not guessed. For a budget, fluent text that's 90% right is a liability.
""")

card(EX, "ex-scaling", "Scaling a system up", [
    "how would you scale this",
    "how do you scale an ai pipeline",
    "scalability experience",
    "can your pipelines scale",
], ["scaling", "scalability", "throughput", "gpu", "batch", "pipeline"], [
    L("Throughput study", "archival-image-throughput-evaluation.html"),
    L("vLLM sweep: SLO gate", "vllm-inference-throughput-evaluation.html#slo-gate"),
], """
Measure first, then scale the part that's actually the bottleneck. The archival images scaled from 1,000 to 12,125, and
the fix was continuous batching on the same GPU, not more hardware. For legislation, I measured exactly how far one L4
goes: about 3 L4s or one A100-class GPU for steady state, and about 7 L4s for peak bursts. The email work came with a
scalability analysis documenting the production path. The unified RIMS pipeline processed 2,375 files in about 21
seconds.
""")

card(EX, "ex-research-skills", "Research and reading the literature", [
    "do you read research papers",
    "research skills",
    "how do you stay current",
    "literature review experience",
], ["research", "papers", "literature", "staying current"], [
    L("Charts without guesswork", "https://tayler-erbe.github.io/semantic-visualizations-for-access/brief/"),
    L("Data readiness research", "https://github.com/tayler-erbe/enterprise-data-readiness-framework"),
], """
Yes. My accessible-charts work rests on a catalog of 22 papers, summarized into a brief and a pre-registered evaluation
plan. The data readiness framework started with a survey of platforms, catalogs, open-source tools, standards and
papers. It found the pieces exist but nothing does the whole job. I also run a writing-partner agent that briefs me on AI
news and argues the other side, and I publish what I learn on Medium.
""")

card(EX, "ex-data-scientist-or-engineer", "Data scientist or engineer?", [
    "are you a data scientist or an engineer",
    "are you more data science or engineering",
    "are you an ml engineer",
    "what is your actual title",
], ["title", "data scientist", "data engineer", "ml engineer", "role"], [
    L("About", "index.html#about"),
], """
Both. My title is Data Scientist on the AI Solutions Team at the University of Illinois System. I joined as a Data
Engineer in May 2022 and was reclassified in November 2023. Day to day I design, build and measure end-to-end systems:
pipelines, model evaluation, inference performance and AI solutions in production. The roles I'm targeting are Data
Engineer, Performance Engineer, AI Solutions Architect, Forward-Deployed Engineer and AI Consultant.
""", prior=0.6)

card(EX, "ex-solo-and-team", "Working solo and on a team", [
    "do you work alone or on a team",
    "have you built things on your own",
    "team size",
    "how big is your team",
], ["team", "solo", "collaboration", "interns", "ownership"], [
    L("Experience", "index.html#experience"),
], """
Both. I scoped, designed and built the research proposals pipeline end to end. I've functionally led the
Advanced Analytics team since early 2023, after major departures, and have recruited and mentored 7+ interns. On the RIMS
build I lead across two organizations, AITS and the University Library. On my personal projects I'm the only human, and
I run 29 AI agents.
""")

card(EX, "ex-governance-docs", "Governance and documentation for leadership", [
    "governance experience",
    "have you written business cases",
    "roi defense",
    "have you written documentation for leadership",
], ["governance", "documentation", "business case", "roi", "committees"], [
    L("Experience", "index.html#experience"),
], """
I'm the sole author of multi-document ESGC governance dossiers for the SPA Research Funding and Workforce Analytics
platforms: leadership briefings, ROI defenses, master data inventories and stakeholder discovery. I present to governance
committees and the Enterprise Architecture Committee, and I sit on the university-wide Generative AI Committee.
""")

card(EX, "ex-experiment-design", "Experiment design and A/B testing", [
    "have you done ab testing",
    "a b testing experience",
    "experiment design",
], ["experiment design", "ab testing", "controlled experiment", "statistics", "intervals"], [
    L("Throughput study: methodology", "archival-image-throughput-evaluation.html#methodology"),
    L("Generation model screen", "generation-model-evaluation.html"),
], """
My experiments are controlled comparisons rather than live product A/B tests. In the throughput study, I held the model and
hardware fixed and varied only the serving stack and concurrency. In the generation screen, I froze the decision rule
before the run and confirmed the winner on 60 new groups with a paired interval. In document intelligence, I used paired
bootstrap intervals and McNemar tests with Holm correction. I change one thing at a time and record every setting.
""")

# ----------------------------------------------------------------------------------------------------------------
# Tools and platforms: "have you worked with X?"  (facts: jobhunter master/work_history.md, cited by line)
# ----------------------------------------------------------------------------------------------------------------

card(TECH, "tech-aws", "Have I worked with AWS?", [
    "have you worked with aws",
    "aws experience",
    "do you know aws",
    "amazon web services",
    "have you used sagemaker",
    "have you used amazon bedrock",
    "aws or azure",
    "are you familiar with aws services",
], ["aws", "amazon", "cloud", "sagemaker", "bedrock", "s3", "ec2", "lambda"], [
    L("Legislative platform", "legislative-pipeline.html"),
], """
My AWS exposure is academic; my production cloud work is on Microsoft Azure. There I designed and run a multi-service
system for the Legislative Intelligence Platform: App Service for the web app, Azure Functions for scheduled jobs, Cosmos DB
for user data, Communication Services for email, Blob Storage and Azure OpenAI. I also diagnosed and fixed its production
issues myself, including a container crash loop and an enterprise SSO restriction on deployments. The concepts map closely
(Functions to Lambda, Blob to S3, Cosmos to DynamoDB), and getting more hands-on AWS time is something I'd welcome.
""", sources=["work_history.md:1405", "work_history.md:150-175"])

card(TECH, "tech-gcp", "Have I worked with Google Cloud?", [
    "have you worked with google cloud",
    "gcp experience",
    "have you used vertex ai",
    "have you used bigquery",
    "do you know google cloud platform",
], ["gcp", "google cloud", "vertex", "bigquery", "colab", "cloud"], [
    L("Legislative platform", "legislative-pipeline.html"),
], """
Not in production. I've used Google Colab with a T4 GPU as a shared development environment, but my production cloud
work is on Microsoft Azure: App Service, Azure Functions, Cosmos DB, Blob Storage, Communication Services and Azure
OpenAI behind the Legislative Intelligence Platform. Most of my heavy AI work runs on self-managed Linux GPU servers,
which keeps the skills portable across clouds.
""", sources=["work_history.md:1415", "work_history.md:150-175"])

card(TECH, "tech-azure", "Azure experience", [
    "have you worked with azure",
    "azure experience",
    "what azure services have you used",
    "have you deployed to the cloud",
    "microsoft azure experience",
    "microsoft azure",
    "do you know azure well",
    "what cloud platforms have you used",
    "which cloud providers have you used",
    "azure functions",
    "cosmos db",
    "azure openai",
], ["azure", "cloud", "app service", "functions", "cosmos", "blob storage", "azure openai", "serverless", "deployment"], [
    L("Legislative platform", "legislative-pipeline.html"),
    L("Legislative web application", "legislative-web-application.html"),
], """
Yes, in production. For the Legislative Intelligence Platform, our team's first production multi-service cloud AI
deployment, I designed, provisioned and operate App Service for the web app, timer-triggered Azure Functions for weekly
digests and nightly impact scoring, Cosmos DB for user data with TTL policies, Communication Services for passwordless
magic-link sign-in and email, Blob Storage for the data, and Azure OpenAI for on-demand briefings. I set up the deployment
pipeline from scratch, fixed a production outage caused by a startup command reinstalling dependencies on every container
boot, and wrote the cost and scaling analysis for the tier upgrade.
""", sources=["work_history.md:69-86", "work_history.md:150-175"])

card(TECH, "tech-containers", "Docker and Kubernetes", [
    "have you used docker",
    "have you used kubernetes",
    "container experience",
    "k8s experience",
    "do you have experience with docker",
    "have you worked with kubernetes",
    "containerized deployment",
], ["docker", "kubernetes", "containers", "k8s", "containerization", "deployment"], [
    L("Running AI in production", "legislative-pipeline.html#prod"),
], """
My container experience is with managed platforms rather than Kubernetes. The legislative app runs as a container on Azure
App Service, where I tuned container start-time limits, startup commands and cold starts, and fixed a crash loop where the
container died on boot. Kubernetes and running my own containerized model deployments are areas I'm actively expanding
into. My GPU serving so far has been vLLM and Ollama on Linux servers, including isolated environments on an air-gapped
institutional machine.
""", sources=["work_history.md:158", "work_history.md:168-171", "work_history.md:1427", "work_history.md:59-66"])

card(TECH, "tech-big-data-platforms", "Spark, Databricks and Snowflake", [
    "have you used spark",
    "have you used databricks",
    "have you used snowflake",
    "big data tools",
    "pyspark experience",
    "data warehouse experience",
    "do you know spark",
    "snowflake experience",
], ["spark", "databricks", "snowflake", "big data", "warehouse", "pyspark", "distributed"], [
    L("Data readiness framework", "https://github.com/tayler-erbe/enterprise-data-readiness-framework"),
], """
Not hands-on. I've handled my larger workloads with pandas, pyarrow and partitioned Parquet: 6 million catalog rows and
5.19 million embeddings for procurement, and 117,722 bills for the passage model, with column pruning and vectorized
passes to keep them fast. My data comes from Oracle and the institution's enterprise data warehouse. My Enterprise Data
Readiness Framework studies how Snowflake Cortex Analyst and Databricks Genie depend on a semantic layer, and it's designed
to publish one that works in either.
""", sources=["work_history.md:1402", "page:procurement-intelligence.html", "readme:enterprise-data-readiness-framework"])

card(TECH, "tech-dl-frameworks", "PyTorch, TensorFlow and Hugging Face", [
    "have you used pytorch",
    "have you used tensorflow",
    "have you used hugging face",
    "deep learning frameworks",
    "transformers library",
], ["pytorch", "tensorflow", "hugging face", "transformers", "deep learning", "sentence transformers"], [
    L("Archival image intelligence", "archival-image-intelligence.html"),
], """
I work mostly at the applied and serving layer: Hugging Face Transformers and open-weight models served through vLLM and
Ollama, and sentence-transformers embedding models such as MiniLM, all-mpnet-base-v2 and bge-small-en-v1.5. I used PyTorch
for the similarity scoring in the archival image work. I've staged Hugging Face weights onto an air-gapped server by hand,
and run a beta deployment on Hugging Face Spaces. TensorFlow isn't part of my work.
""", sources=["work_history.md:1396", "work_history.md:1405", "work_history.md:63", "page:archival-image-intelligence.html"])

card(TECH, "tech-langchain", "LangChain and LLM frameworks", [
    "have you used langchain",
    "have you used llamaindex",
    "llm frameworks",
    "what orchestration framework do you use",
    "do you use langchain",
    "have you used haystack",
], ["langchain", "llamaindex", "haystack", "frameworks", "orchestration"], [
    L("Agent architecture", "agent-architecture.html"),
    L("Legacy file search", "file-archiving-smart-search.html"),
], """
I haven't used LangChain or LlamaIndex in production. I explored Haystack for the legacy file search (FAISS document store
plus an embedding retriever) to check that the design was portable across frameworks, then kept the pipeline in plain
Python. That's my usual choice: a backend-agnostic router between Ollama and vLLM, FAISS retrieval, JSON schemas enforced
on output, and my own job queue for agents. Fewer layers means every step stays visible and testable.
""", sources=["work_history.md:692", "work_history.md:61", "page:agent-architecture.html"])

card(TECH, "tech-openai", "OpenAI and GPT models", [
    "have you used openai",
    "have you used chatgpt",
    "openai api experience",
    "have you used the openai api",
    "hosted llm apis",
    "have you used groq",
], ["openai", "gpt", "gpt-4.1", "gpt-4o-mini", "azure openai", "chatgpt", "api", "groq"], [
    L("Legislative platform", "legislative-pipeline.html"),
], """
Yes. The legislative platform's Copilot chatbot runs on GPT-4.1 with citation-backed answers, and I integrated Azure OpenAI
(gpt-4o-mini) for on-demand executive briefings and nightly impact scoring, while heavy batch extraction stays on local
models. I've used the Groq API for open-weights Llama inference for briefings, and the OpenAI image API in personal
projects. I've used ChatGPT since soon after its public release, and I tested the open-weight GPT-OSS 20B in two of my
evaluations.
""", sources=["work_history.md:1396", "work_history.md:155", "work_history.md:1397", "page:generation-model-evaluation.html"])

card(TECH, "tech-claude", "Claude and Claude Code", [
    "have you used claude",
    "have you used claude code",
    "anthropic experience",
    "do you code with ai",
    "do you use claude code",
], ["claude", "claude code", "anthropic", "ai coding", "agents", "subagents", "hooks"], [
    L("Agent architecture", "agent-architecture.html"),
    L("vLLM qualitative review", "vllm-qualitative-review.html"),
], """
Heavily. In my personal projects I run 29 agents on Claude Code, with subagents, pre-execution hooks, scoped permissions and
persistent memory, coordinated through my own job queue. Drop Radar's self-improving maintenance agent is a Claude Code
agent. For the legislative model sweep, Claude Opus graded output quality in two independent passes that agreed on 60 of 60;
in my newer evaluations I score with code instead of a model. AI assistants write and run my evaluation harnesses, and I
review what they produce.
""", sources=["work_history.md:1419", "page:agent-architecture.html", "page:drop-radar.html", "page:vllm-qualitative-review.html"])

card(TECH, "tech-open-models", "Open-weight models I've used", [
    "what open source models have you used",
    "which open weight models do you know",
    "have you used qwen",
    "have you used mistral",
    "which llms have you worked with",
    "which open source llms have you used",
], ["open weight", "llama", "qwen", "mistral", "gemma", "llava", "nemotron", "models"], [
    L("Document intelligence", "document-intelligence-evaluation.html"),
    L("vLLM multi-model sweep", "vllm-inference-throughput-evaluation.html"),
], """
In my work systems: Llama 3.1 8B AWQ for legislative extraction, Llama 3.2 for de-identified email summaries, LLaVA for images,
and qwen2.5:7b for procurement equivalence. My personal Skyrule stack runs Qwen3-32B with AWQ and FP8 on vLLM. In my
evaluations I've run Mistral 7B, Qwen 2.5, Qwen3-VL 8B and 32B, Qwen2.5-VL 7B and 32B, Qwen3.8 27B, Qwen 3.6 35B-A3B,
Gemma 4, GPT-OSS 20B, Nemotron 3 Nano, Nemotron 3.5 Parse, PaddleOCR-VL-1.6 and olmOCR-2.
""", sources=["work_history.md:1396", "page:document-intelligence-evaluation.html", "page:generation-model-evaluation.html"])

card(TECH, "tech-vector-dbs", "Vector databases", [
    "have you used pinecone",
    "have you used chromadb",
    "have you used faiss",
    "vector store experience",
    "do you use pinecone",
], ["vector database", "faiss", "pinecone", "chroma", "haystack", "embeddings", "hnsw", "ivf"], [
    L("Procurement intelligence", "procurement-intelligence.html"),
    L("Legacy file search", "file-archiving-smart-search.html"),
], """
FAISS is my default, and I pick the index for the scale. IndexFlatIP with L2-normalized vectors for exact cosine search on
smaller collections, HNSW for the legacy file archive, and IVFFlat with 4,096 lists and nprobe 64 for the 5.19 million
procurement embeddings. I've also worked with Pinecone and explored Haystack's FAISS document store. For most of my
projects, local FAISS indexes built offline and stored as files keep the data on our hardware and the running cost near
zero.
""", sources=["work_history.md:1399", "work_history.md:692", "page:file-archiving-smart-search.html"])

card(TECH, "tech-bi-tools", "Tableau and Power BI", [
    "have you used tableau",
    "have you used power bi",
    "bi tools experience",
    "business intelligence tools",
    "do you know power bi",
], ["tableau", "power bi", "bi", "dashboards", "streamlit", "plotly"], [
    L("Legislative web application", "legislative-web-application.html"),
    L("HR workforce analytics", "hr-workforce-analytics.html"),
], """
I'm familiar with Power BI, but my production dashboards are built in code. The legislative platform is a multi-page
Streamlit and Plotly application on Azure, with a shared colorblind-safe theme, seven linked trend views and a personalized
workspace. Procurement has an HTML and FastAPI spending dashboard. The HR workforce platform plan includes Power BI and
Tableau dashboard prototypes, and my data readiness framework covers how Power BI Copilot depends on a good semantic layer.
""", sources=["work_history.md:1411", "work_history.md:69-77", "page:hr-workforce-analytics.html"])

card(TECH, "tech-ml-libraries", "Machine learning libraries", [
    "have you used scikit learn",
    "have you used xgboost",
    "which ml libraries do you use",
    "have you used h2o",
], ["scikit-learn", "xgboost", "h2o", "catboost", "random forest", "histgradientboosting", "libraries"], [
    L("UIC enrollment: models", "uic-enrollment.html#models"),
    L("HR workforce analytics", "hr-workforce-analytics.html"),
], """
Mostly scikit-learn: Random Forest, tree ensembles and HistGradientBoostingClassifier. On the UIC enrollment project the team compared H2O and CatBoost head to head and used ARIMA with exponential smoothing for forecasting, and I've used NetworkX for graph communities. The
HR succession designs use XGBoost, logistic regression and LambdaMART. Underneath it all are pandas, numpy and pyarrow.
""", sources=["work_history.md:1390", "page:uic-enrollment.html", "page:hr-workforce-analytics.html"])

card(TECH, "tech-orchestration-mlops", "Airflow, MLflow and MLOps tooling", [
    "have you used airflow",
    "have you used mlflow",
    "mlops tools",
    "workflow orchestration tools",
    "scheduling experience",
    "do you use airflow",
], ["airflow", "mlflow", "mlops", "orchestration", "scheduling", "cron", "prometheus", "grafana"], [
    L("Medium: monitoring", "https://medium.com/@tayler.erbe/i-got-tired-of-pipelines-failing-silently-so-i-built-my-own-monitoring-system-e8224fe22387"),
], """
Our production pipelines run on cron and the JupyterHub Scheduler on Linux, and I built the monitoring layer that an
Airflow or MLflow setup would otherwise provide: a Parquet logging contract for every stage, start and end sentinel rows so
a silent pipeline is detected, severity-tiered alerts, and per-pipeline silence thresholds for quarterly jobs. I've also
used Prometheus and Grafana, and GitHub Actions for board automation and one-click pipeline runs. For my agents I built an autonomous job queue and GPU scheduler that
has launched 2,400+ unattended jobs since October 2, 2026.
""", sources=["work_history.md:1408", "work_history.md:1413", "work_history.md:1415", "work_history.md:473", "page:index.html"])

card(TECH, "tech-hardware", "GPUs and hardware I've used", [
    "what gpus have you used",
    "what hardware do you use",
    "have you used nvidia gpus",
    "have you used an a100",
    "have you used h100",
    "what gpu do you use",
], ["gpu", "nvidia", "l4", "l40s", "rtx 5090", "t4", "hardware", "cuda"], [
    L("Throughput study", "archival-image-throughput-evaluation.html"),
    L("Document intelligence", "document-intelligence-evaluation.html"),
], """
At work, an NVIDIA L4 (24 GB) on an air-gapped institutional Linux server, where I stood up vLLM and did the throughput
migration and model sweep with GPU telemetry. At home, an RTX 5090 (32 GB) runs my personal Skyrule stack and my model
evaluations, and I've used a 12 GB laptop GPU and Colab T4s. I sized the document work for an L4 or L40S. For bigger needs I
estimate from measurements: the legislative pipeline would need about one A100-class GPU for steady state, or H100-class
hardware for peak bursts.
""", sources=["work_history.md:59-66", "page:document-intelligence-evaluation.html", "work_history.md:1415", "page:vllm-inference-throughput-evaluation.html"])

card(TECH, "tech-integrations", "APIs and system integrations", [
    "what apis have you integrated",
    "integration experience",
    "have you worked with apis",
    "have you used the box api",
], ["apis", "integrations", "box", "oracle", "legiscan", "telegram", "discord", "imap"], [
    L("Legacy file search", "file-archiving-smart-search.html"),
    L("Drop Radar", "drop-radar.html"),
], """
At work: Oracle through cx_Oracle and python-oracledb for live reads and writeback, the Box SDK for legacy files, the
LegiScan API with hash-based incremental downloads (2 to 4 calls a run instead of the full dataset), and Azure services.
In personal projects: the Telegram Bot API, Discord's REST and Gateway APIs, read-only IMAP, Shopify feeds, and the Etsy
and Printify APIs.
""", sources=["work_history.md:1402", "work_history.md:1396", "work_history.md:1432", "page:drop-radar.html", "work_history.md:1421"])

# ----------------------------------------------------------------------------------------------------------------
# Changes to existing cards (applied by merge.py)
# ----------------------------------------------------------------------------------------------------------------

PATCHES = {
    # the general "how do you choose a model" question now goes to the process card; the sweep keeps its specific ones
    "vllm-model-sweep": {"remove_questions": ["how do you choose a model", "model selection"]},
    # her own-words card on agents vs workflows answers these better than a new card would
    "persona-agent-vs-workflow": {"add_questions": [
        "how do you decide to use an agentic workflow",
        "how do you decide how to use agentic workflows",
        "when do agents make sense",
        "agents vs a simple pipeline",
        "when should i use an agentic workflow",
        "when would you use an agent",
    ]},
    # the Applied AI Lab is her second site
    "websites": {
        "answer": "You can find me online at taylererbe.com, my portfolio site, and at my Applied AI Lab, "
                  "tayler-erbe.github.io/document-intelligence-lab, where I collect my model evaluations, performance "
                  "studies and pipeline designs. skyrule.io is the public site for my personal project. I also write on "
                  "Medium and am on LinkedIn, and you can see my code on GitHub.",
        "add_links": [LAB_LINK],
        "add_questions": ["what are your two websites", "do you have another website", "what is your second website"],
    },
}

# the "no good match" message. chat.js fills {answers} and {questions} with live counts, and {query} in a link with the
# visitor's question. Nothing is stored or sent unless the visitor presses the email button.
FALLBACK = {
    "title": "Tayler hasn't answered that one yet",
    "answer": "Sorry, there isn't an answer for that question yet. Send it to Tayler with the button below and she'll add it "
              "to her list of questions to answer.",
    "note": "This isn't a live AI chatbot. No model runs when you ask; your question is matched against {answers} answers "
            "(about {questions} ways of asking) that were prepared ahead of time from Tayler's own sources: her work history, "
            "her project case studies, her Medium articles and LinkedIn posts, and questions she has answered herself since "
            "August 2026. She keeps adding more. Nothing you type is stored or sent anywhere unless you choose to email it.",
    "links": [
        {"label": "Send this question to Tayler", "url": "mailto:hello@taylererbe.com?subject=A%20question%20for%20Ask%20about%20Tayler&body={query}"},
        {"label": "Resume (PDF)", "url": "resume.pdf"},
    ],
}

PATCHES["chatbot-how-built"] = {
    "answer": "This chat searches pre-written answer cards in your browser. Your question is matched by keyword ranking "
              "(BM25 with a synonym table) and, once a small embedding model loads, by meaning as well. No AI model writes "
              "anything while you use it, and there is no server, tracking or cookies; your questions never leave the page. "
              "Every answer is built from my own sources: my work history, my case studies, my Medium writing and questions "
              "I've answered myself. The wording was drafted with AI help, first a local model on my GPU and later Claude, "
              "and each answer is checked against those sources before it goes in.",
}

# the old answer read as if a fairness audit had been run on real employees; the page shows it as a designed view in a
# proof of concept (HR workforce analytics page: "Succession dashboard prototype: ... equity audit"; work_history.md:1082)
PATCHES["hr-equity"] = {
    "answer": "Fairness is designed into the HR workforce platform rather than added at the end, but it is still a proof of "
              "concept, so no audit has been run on real employee decisions. The succession dashboard prototype includes an "
              "equity audit view meant to check whether succession and promotion recommendations are proportionally "
              "distributed across demographic groups and to flag patterns for review before anyone uses them. Each "
              "recommendation carries an interpretable rationale, such as \"high tenure and a high move rate in a "
              "high-growth job family\", top candidate lists are reviewed for demographic balance, and the validation "
              "phase includes a fairness review across groups.",
}

# routing: phrasings an interviewer uses that landed on a weaker card in the blind test (11 Nov 2026)
for _cid, _qs in {
    "aie-multimodal-pipeline": ["how do you handle images and scanned pages", "scanned pages in a pipeline", "images in a document pipeline"],
    "iv-quantization": ["what did quantization cost you in quality", "quantization quality trade-off", "what quantization have you used"],
    "ads-validation-strategy": ["how do you validate a model on time based data", "temporal validation", "validating on time ordered data"],
    "ads-small-data-power": ["how do you handle a small dataset", "not enough data to model", "working with very little data"],
    "iv-interpretable-models": ["how do you explain a model's predictions", "explaining individual predictions"],
    "ads-measuring-model-impact": ["most impactful model you have built", "your most impactful model"],
    "con-platform-evaluation": ["how have you evaluated vendors", "vendor and platform evaluation"],
    "iv-similarity-thresholds": ["setting a similarity threshold for retrieval", "cosine similarity threshold for retrieval"],
    "aie-api-app-design": ["fastapi or flask", "which web framework do you use for ai services", "fastapi vs streamlit"],
    "ads-bill-threshold": ["how do you pick a decision threshold", "choosing a classification threshold", "operating point for a classifier"],
}.items():
    PATCHES.setdefault(_cid, {}).setdefault("add_questions", []).extend(_qs)

# ----------------------------------------------------------------------------------------------------------------
# Added after the 1,000-question stress test (round 1): the commonest questions that had no honest home
# ----------------------------------------------------------------------------------------------------------------
META = ("meta", "About this chat")

card(TECH, "tech-not-used", "Tools that aren't part of my work so far", [
    "have you used terraform", "infrastructure as code", "do you know java", "do you code in go", "golang experience",
    "do you know rust", "have you written c++", "scala experience", "have you used kafka", "hadoop experience",
    "have you worked with salesforce", "ever touched salesforce", "have you worked with sap", "have you used dbt",
    "have you used looker", "redshift experience", "have you used mongodb", "mysql experience",
    "ever used delta lake or iceberg", "delta lake", "apache iceberg", "have you built ios apps", "swift or kotlin",
    "android development", "does she code in go", "has she used terraform or other infrastructure as code tools",
    "which tools have you not used", "what don't you know",
], ["terraform", "java", "go", "golang", "rust", "c++", "scala", "kafka", "hadoop", "salesforce", "sap", "dbt", "looker",
    "redshift", "mongodb", "mysql", "delta lake", "iceberg", "swift", "kotlin", "not used"], [
    L("Skills", "index.html#skills"),
    L("Resume (PDF)", "resume.pdf"),
], """
Not so far. My work hasn't involved Java, C++, Go, Rust or Scala, and I haven't used Terraform, Kafka, Hadoop, dbt,
Looker, Redshift, MongoDB, MySQL, Delta Lake, Iceberg, Salesforce or SAP, or built native mobile apps in Swift or Kotlin.
What I do work in is Python, SQL, R and Bash, with Oracle, Parquet, FAISS, Azure and Linux GPU servers, and the specific
tools are listed in the skills section and on each project page. If the role depends on one of the tools above, I'd rather
you know that up front.
""", sources=["work_history.md:1386-1421 (none of these tools appear anywhere in the work history)"])

card(EX, "core-degrees-employers", "Graduate degrees and past employers", [
    "does she have a phd", "what was her phd thesis on", "do you have a masters degree", "graduate degree",
    "did you go to grad school", "tell me about her time at google", "have you worked at google", "did she work at a faang company",
    "have you worked at a big tech company", "did you work at openai", "have you worked at nvidia", "have you worked at a startup",
    "which companies have you worked for", "who has she worked for", "list of employers",
], ["phd", "masters", "graduate degree", "google", "meta", "amazon", "microsoft", "openai", "nvidia", "faang", "big tech", "employers"], [
    L("Experience", "index.html#experience"),
    L("Resume (PDF)", "resume.pdf"),
], """
No graduate degree, and no big-tech employer. My degree is a B.S. in Cognitive Science, with a specialization in Machine
Learning and Neural Computation, from UC San Diego in 2021. I don't have a master's or a PhD. I've been at the University of
Illinois System since May 2022, first as a Data Engineer and since November 2023 as a Data Scientist. Before that I was a
Data Scientist at the San Diego Regional Data Library and a Python Developer at Dragonchain, a blockchain startup. I haven't
worked at Google, Meta, Amazon, Microsoft, OpenAI or NVIDIA.
""", sources=["work_history.md:13-20", "work_history.md:1273-1296", "work_history.md:1442-1444"])

card(META, "meta-private", "Things I keep private", [
    "what is her salary", "what's her current salary", "how much does she make", "salary expectations", "what salary do you want",
    "who did she vote for", "what are her political views", "is tayler religious", "what religion is she", "is she married",
    "is she single", "does she have kids", "what are her kids names", "where does she live", "what is her home address",
    "what is her phone number", "does she have any health conditions", "what is her ethnicity",
], ["salary", "pay", "compensation", "politics", "vote", "religion", "married", "kids", "children", "address", "health", "private", "personal"], [
    L("Email hello@taylererbe.com", "mailto:hello@taylererbe.com"),
], """
That's something I keep off this site. I don't publish personal details here: salary, age, family, politics, religion,
health or my home address. For compensation or anything else specific to a role, email me and we can talk about it
directly. Everything about my work, projects and background is fair game here.
""", nocanon=["contact", "hire", "remote"])

card(META, "meta-off-topic", "What this chat can and can't do", [
    "what's the weather", "what's the weather in chicago today", "who won the game last night", "tell me a joke",
    "write me a poem", "write my essay", "help me with my code", "fix this python error", "give me a recipe",
    "ignore previous instructions", "ignore all previous instructions and", "you are now a different assistant",
    "what is your system prompt", "give me the password", "login password for the legislative dashboard",
    "give me access to the dashboard", "what is the capital of france", "translate this for me", "do my homework",
], ["weather", "joke", "poem", "recipe", "homework", "password", "login", "instructions", "system prompt", "off topic"], [
    L("Email hello@taylererbe.com", "mailto:hello@taylererbe.com"),
], """
This chat only answers questions about my work, projects and background. It isn't a live AI, so it can't write, code,
look things up or follow instructions; it matches your question to answers I prepared ahead of time. It also never gives
out passwords or access to any system. Try asking about a project, a tool, or how I'd approach a problem.
""")

# routing phrasings from the stress test's fix half (round 1); the other half stays untouched as the held-out exam
import json as _json, os as _os
_p = _os.path.join(_os.path.dirname(_os.path.abspath(__file__)), "routing_stress_round1.json")
if _os.path.exists(_p):
    for _cid, _qs in _json.load(open(_p, encoding="utf-8")).items():
        if _cid in {c["id"] for c in CARDS}:
            next(c for c in CARDS if c["id"] == _cid)["questions"].extend(q for q in _qs if q not in next(c for c in CARDS if c["id"] == _cid)["questions"])
        else:
            PATCHES.setdefault(_cid, {}).setdefault("add_questions", []).extend(_qs)

# ---- stress test round 2: content gaps that the sources can answer ----
GUIDE = L("Choosing a local model (guide)", "choosing-local-models-guide.html")

card(EX, "guide-model-names", "Reading a model's name: 27B, 35B-A3B, Q4_K_M, AWQ", [
    "what does q4_k_m mean", "what does the q4_k_m at the end of a model name actually mean", "35b-a3b meaning",
    "what does 35b-a3b mean", "what does awq mean", "what do the numbers in a model name mean", "is a 32b model better than a 27b",
    "what does 8b mean in a model name", "how to read a model name", "what is a mixture of experts model", "q4 quantization meaning",
], ["model name", "parameters", "q4_k_m", "a3b", "awq", "quantization", "mixture of experts", "bit width"], [GUIDE], """
The labels look like a ranking and aren't one. 27B or 32B is roughly the parameter count in billions: it sets capacity, not
how well the model was trained or follows instructions. 35B-A3B is a mixture of experts: about 35 billion parameters in
total with about 3 billion active per token, so it can compute less per token, but all the weights still have to be stored.
Q4 or Q4_K_M is an approximately 4-bit weight quantization format, which shrinks the weights so a large model fits on one
card. AWQ is a quantization method, not a bit width, so check the actual bit width of the checkpoint you download. My guide
walks through each label and what it does and doesn't tell you.
""", sources=["page:choosing-local-models-guide.html (section 01)"])

card(EX, "guide-audience", "Who the local model guide is for", [
    "who is the local model guide written for", "who is the local model guide written for and did anyone review it",
    "was the model guide reviewed", "what does the choosing a local model guide cover", "is the guide based on your own results",
    "what is the advisory guide about", "choosing a local model guide",
], ["guide", "advisory", "audience", "reviewed", "local model", "open weight"], [GUIDE], """
It's written for teams choosing an open-weight model for a specific job, often their first local model. It covers how to
read model names, how these models are commonly trained, why a smaller model can beat a bigger one, what public benchmarks
can and can't tell you, a method for picking and validating a model, and when fine-tuning is worth it, ending in a
one-page checklist. It combines findings from my own evaluations (the generation model screen and the document intelligence
evaluation) with general engineering guidance, and it was independently reviewed and revised following technical feedback.
""", sources=["page:choosing-local-models-guide.html (header and sections 01-08)"])

card(EX, "core-clients-internal", "Who my clients have been", [
    "have you done any consulting for outside clients", "done any consulting for outside clients", "have you had external clients",
    "who are your clients", "do you have paying customers", "have you worked for customers outside the university",
    "is all your work internal", "what kind of clients have you worked with",
], ["clients", "external", "outside", "internal clients", "customers", "consulting"], [
    L("Projects", "index.html#projects"),
    LAB_LINK,
], """
My work so far has all been inside the University of Illinois System, building for other units: the Institute of
Government and Public Affairs and Academic Affairs on legislation, the University Library and records management on
archives, Sponsored Programs Administration on research proposals, Illinois HR on workforce analytics, purchasing on
procurement, and UIC on enrollment. Each came with its own stakeholders, data and constraints. I haven't done any outside
consulting yet, and I wouldn't call what I've done consulting in the formal sense. My Applied AI Lab is where I publish
the advisory-style work that isn't tied to one unit.
""", sources=["work_history.md:1350-1385", "page:index.html", "lab index"])

card(EX, "core-knowledge-graphs", "Knowledge graphs and graph-based retrieval", [
    "used knowledge graphs for rag", "have you used knowledge graphs", "graph rag", "knowledge graph experience",
    "have you built a knowledge graph", "graphrag",
], ["knowledge graph", "graph rag", "graphrag", "network graph", "relationships"], [
    L("Legislative pipeline", "legislative-pipeline.html"),
    L("HR workforce analytics", "hr-workforce-analytics.html"),
], """
I've built graphs for analysis, not for retrieval. On the legislative platform I constructed knowledge and network graphs
mapping relationships across legislative goals, beneficiaries and policy domains from LLM-extracted features, and in HR
workforce analytics I used graph community detection to find career communities. My retrieval systems are FAISS vector
search with exact-match and keyword tiers in front. I haven't used a knowledge graph as the retrieval layer for RAG.
""", sources=["work_history.md:135", "page:hr-workforce-analytics.html", "work_history.md:1399"])

for _cid, _qs in {
    "chatbot-how-built": ["can you remember what i asked earlier", "do you remember our conversation", "does this chat have memory",
                          "do you store what i type", "is this conversation being recorded", "will tayler see my questions"],
}.items():
    PATCHES.setdefault(_cid, {}).setdefault("add_questions", []).extend(_qs)


# recruiter logistics, from her standard application answers (jobhunter profile.json, 11 Nov 2026)
card(EX, "core-logistics", "Start date, location and logistics", [
    "when can you start", "how soon could she start a new position", "start date availability", "what is your notice period",
    "earliest start date", "where are you based", "where is she located", "where's she based", "what city do you live in",
    "what time zone are you in", "are you willing to relocate", "would you relocate", "are you open to travel", "how much travel can you do",
    "do you need visa sponsorship", "does she need sponsorship", "are you a us citizen", "can you get a security clearance",
    "do you have a security clearance", "is she remote",
], ["start date", "notice", "availability", "location", "based", "relocate", "relocation", "travel", "sponsorship", "citizen", "clearance", "time zone"], [
    L("Email hello@taylererbe.com", "mailto:hello@taylererbe.com"),
    L("Resume (PDF)", "resume.pdf"),
], """
I can start about two weeks after an offer, and sooner if needed. I'm based in San Diego, California, and I strongly
prefer fully remote work; I'm also open to hybrid or in-office roles in San Diego, the Raleigh, North Carolina area or the
Austin, Texas area. I'm not available for roles that require travel. I'm a U.S. citizen, so I don't need sponsorship, and
I'm eligible for a security clearance, though I don't hold one today. For anything else about logistics, email me.
""", sources=["jobhunter profile.json: city_state, willing_to_relocate, remote_preference, notice_period, earliest_start_date, travel, us_citizen"],
     nocanon=["contact"])


# ---- Tayler's own answers, 11 Nov 2026 (voice notes; tidied, nothing added) ----
OWN = ("answers", "In my words")

card(OWN, "answer-cogsci-helps", "How my cognitive science degree helps", [
    "how does a cognitive science degree help you in this work", "how does cognitive science help with ai",
    "why does a cognitive science background matter", "is your degree relevant to ai", "what did you study and how does it apply",
    "how does neuroscience relate to generative ai", "what does cognitive science have to do with machine learning",
    "did you double major", "what courses did you take", "how does her degree help", "cognitive science and ai",
], ["cognitive science", "degree", "neuroscience", "nanoengineering", "human computer interaction", "hci", "coursework", "interdisciplinary"], [
    L("About", "index.html#about"),
], """
My degree was in machine learning and neural computation, so I took neuroscience, cognitive science and statistics, and
for a while I was a double major with nanoengineering. Every course I've taken, however different, has turned out to be
applicable in some way. Cognitive science is about how the brain learns and processes information, and the brain is in
many ways the model for generative AI. I often reach for neuroscience as the biological picture of how these models think.
It also keeps me on the human side. Everything AI does is for human consumption in one way or another, so the
human-computer interaction and the cognitive effects of AI matter as much as the model does.
""", sources=["Tayler, voice note, 11 Nov 2026"], prior=0.85)

card(OWN, "answer-skills-that-matter", "Hard skills or the ability to learn?", [
    "what matters more hard skills or the ability to learn", "what skills matter most for working with ai",
    "are data scientists the right people to use ai", "who is best suited to work with ai", "do you need a data scientist to use ai",
    "is domain knowledge more important than technical skill", "what makes someone good at ai work", "generalist or specialist for ai",
    "what do you look for in people who build with ai",
], ["hard skills", "ability to learn", "generalist", "domain knowledge", "jack of all trades", "data scientist"], [
    L("About", "index.html#about"),
], """
I think data scientists who've worked in generative AI, text analytics and natural language processing are probably the
best suited to knowing how to use AI, because we have a foundational understanding of how it works. But at this point I
don't think hard skills are the most important thing. It's the ability to learn, to think constructively and broadly, to
be a jack of all trades. On a team solving a specific problem, people with niche domain knowledge of the thing being built
often bring more to the table than a pure data scientist. Data scientists are generalists by nature, though: you have to be
ready to work with every kind of data and every kind of problem.
""", sources=["Tayler, voice note, 11 Nov 2026"], prior=0.85)

card(EX, "core-no-papers", "Academic papers and publications", [
    "has tayler published any academic papers", "have you published research", "do you have publications",
    "any peer reviewed papers", "have you written a paper", "where do you publish your work", "google scholar",
], ["papers", "publications", "academic", "peer reviewed", "research papers", "medium"], [
    L("Medium", "https://medium.com/@tayler.erbe"),
    LAB_LINK,
], """
No, I haven't published academic papers. My writing is on Medium, where I cover production ML monitoring, deploying AI to
Azure, archival AI and what AI means for human work, and my studies and briefs are in my Applied AI Lab, each with its
method and limits stated.
""", sources=["Tayler, 11 Nov 2026", "work_history.md:1346"])

card(EX, "core-research-portfolio-size", "How big is the research portfolio my pipeline supports?", [
    "how big is the research portfolio", "is the research portfolio 517 million or 1.5 billion", "how much research funding does the pipeline cover",
    "what is the 517m figure", "university of illinois research funding size", "how much funding do the proposals represent",
], ["research portfolio", "517m", "1.5 billion", "funding", "sponsored programs", "proposals and awards"], [
    L("Research proposal processing", "research-proposal-processing.html"),
], """
About $517M a year. That's the figure I use for the University of Illinois System research portfolio that the proposals
pipeline supports. You may also see about $1.5B, which is total funding booked; only about $517M of that is actually
allocated to the research itself, with the rest going to other costs that return to the university. The smaller number is
the more accurate one.
""", sources=["Tayler, 11 Nov 2026", "page:index.html"])

card(EX, "core-agent-count", "How many agents do I run?", [
    "how many agents do you run", "is it 15 agents or 29", "skyrule says 15 agents but another page says 29 which is right",
    "how many ai agents does she have", "number of agents", "how big is the agent organization", "has the agent count changed",
], ["agents", "29 agents", "15 agents", "agent count", "agent organization"], [
    L("Agent architecture", "agent-architecture.html"),
    L("Skyrule", "skyrule.html"),
], """
It was 29 when I wrote the architecture page in October 2026, and it keeps moving. The 15 you may see is the Skyrule
engineering organization on its own; 29 counted every agent across Skyrule and my other personal projects, all on the same
job queue, memory and ownership rules. Since then I've added projects and consolidated some agents, so the exact number
changes. All of it is personal-project work.
""", sources=["Tayler, 11 Nov 2026", "page:agent-architecture.html", "work_history.md:1137"])
