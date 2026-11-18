# AI Engineering Project Portfolio

A reviewer-oriented guide to the engineering work in my public GitHub repositories. The projects are presented as inspectable code and technical documentation—not as unsupported claims about production scale or business impact.

> **Suggested review path:** start with the open-source contribution, then inspect one backend/system-design project, one LLM evaluation project, and the document-intelligence workflow. Each section links to the source repository so you can verify implementation details directly.

---

## 1. Enterprise Analytics Copilot

<a href="https://github.com/todkarsant/Enterprise-Analytics-Copilot">
  <img src="https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white" height="28" alt="Python" />
  <img src="https://img.shields.io/badge/FastAPI-009688?style=for-the-badge&logo=fastapi&logoColor=white" height="28" alt="FastAPI" />
  <img src="https://img.shields.io/badge/DuckDB-FFF000?style=for-the-badge&logo=duckdb&logoColor=black" height="28" alt="DuckDB" />
</a>

**Problem:** Turn natural-language business questions into controlled, evidence-grounded analytical answers without treating model-generated SQL as inherently safe.

**Engineering focus**
- Schema retrieval and analytical planning.
- Deterministic SQL paths for known intents, with an LLM path for less constrained questions.
- SQL guard and read-only database execution boundary.
- Tests, evaluation scripts, API and Streamlit interface.
- Explicit distinction between demo/reference safeguards and production security requirements.

**What to inspect**
- `app/services/analytical_planner.py`
- `app/services/intent_planner.py`
- `app/services/sql_guard.py`
- `tests/`
- `docs/ARCHITECTURE_DECISIONS.md` and `docs/EVALUATION.md`

[Open repository](https://github.com/todkarsant/Enterprise-Analytics-Copilot)

---

## 2. LLM Evaluation & Observability Platform

<a href="https://github.com/todkarsant/LLM-Evaluation-Observability-Platform">
  <img src="https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white" height="28" alt="Python" />
  <img src="https://img.shields.io/badge/FastAPI-009688?style=for-the-badge&logo=fastapi&logoColor=white" height="28" alt="FastAPI" />
  <img src="https://img.shields.io/badge/Ollama-111111?style=for-the-badge&logo=ollama&logoColor=white" height="28" alt="Ollama" />
</a>

**Problem:** Model, prompt, retrieval or orchestration changes can silently improve one metric while degrading another. Teams need repeatable evaluation and release evidence.

**Engineering focus**
- Application-agnostic adapters for HTTP JSON, Ollama RAG, custom Python applications and deterministic fixtures.
- Dataset/version identity and experiment metadata.
- Quality measures alongside latency, token and estimated-cost telemetry.
- Failure taxonomy, baseline comparison and configurable release gates.
- Bounded concurrency, retries and asynchronous job execution in the later implementation.

**What to inspect**
- `app/services/evaluator.py`
- `app/services/runner.py`
- `app/services/quality_gate.py`
- `app/services/adapters/`
- `docs/PLUG_AND_PLAY.md` and `docs/EVALUATION.md`

[Open repository](https://github.com/todkarsant/LLM-Evaluation-Observability-Platform)

---

## 3. Trade Finance Document Intelligence

<a href="https://github.com/todkarsant/Trade-Finance-Document-Intelligence">
  <img src="https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white" height="28" alt="Python" />
  <img src="https://img.shields.io/badge/Azure_OpenAI-0078D4?style=for-the-badge&logo=microsoftazure&logoColor=white" height="28" alt="Azure OpenAI / Azure" />
  <img src="https://img.shields.io/badge/FastAPI-009688?style=for-the-badge&logo=fastapi&logoColor=white" height="28" alt="FastAPI" />
</a>

**Problem:** Letters of Credit contain semi-structured trade-finance fields and clauses across PDF pages and amendments. Extraction must preserve document context and support review.

**Engineering focus documented in the repository**
- Email/PDF ingestion and document parsing into SWIFT MT700 structure.
- Amendment handling before downstream extraction.
- Tiered field extraction: deterministic rules, keyword-gated LLM, hybrid logic and verification.
- Post-processing, structural/semantic verification and confidence scoring.
- Human-in-the-loop review and audit-oriented workflow.

**What to inspect**
- `architecture.md`
- `flows.md`
- `infrastructure.md`
- `integrations.md`
- `cicd_pipelines.md`

**Confidentiality boundary:** this public portfolio describes the repository's architecture at a high level. It does not disclose customer documents, private prompts, credentials, tenant data or employer-confidential implementation details.

[Open repository](https://github.com/todkarsant/Trade-Finance-Document-Intelligence)

---

## 4. SWARM — Multi-agent Analytics

<a href="https://github.com/todkarsant/Multi-agent-orchestration">
  <img src="https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white" height="28" alt="Python" />
  <img src="https://img.shields.io/badge/LangGraph-1C3C3C?style=for-the-badge&logo=langchain&logoColor=white" height="28" alt="LangGraph / LangChain ecosystem" />
  <img src="https://img.shields.io/badge/DuckDB-FFF000?style=for-the-badge&logo=duckdb&logoColor=black" height="28" alt="DuckDB" />
</a>

**Problem:** Analytical questions may span multiple datasets and require intent interpretation, canonical dimension resolution, controlled SQL execution and clear presentation.

**Engineering focus described in the repository**
- Specialist-agent routing across financial and document-search domains.
- Intent, context and clarification stages.
- Deterministic dimension resolution and SQL validation.
- Structured analytics and document retrieval paths.
- Reporting, audit traces and operational workflows.

[Open repository](https://github.com/todkarsant/Multi-agent-orchestration)

---

## 5. AI Agent Evidence-to-Action Reliability — Research

<a href="https://github.com/todkarsant/AI-Agent-Evidence-to-Action-Reliability">
  <img src="https://img.shields.io/badge/Research-Methodology-6A5ACD?style=for-the-badge" height="28" alt="Research methodology" />
  <img src="https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white" height="28" alt="Python" />
</a>

**Research question:** Does decision-time evidence sufficiency provide measurable information about consequential agent action errors beyond existing decision-time signals?

**Research discipline**
- Explicit separation of discovery evidence and confirmatory evidence.
- Construct identifiability and measurement reliability gates.
- Adversarial methodological checks and falsification-first principles.
- Provenance, preregistration and preservation of null/failure evidence.
- Clear statement that the work remains in methodological validation / pre-confirmatory status.

This repository is research in progress, not a claim that the proposed construct has already been validated or that agent safety has been improved.

[Open research repository](https://github.com/todkarsant/AI-Agent-Evidence-to-Action-Reliability)

---

## 6. Upstream open-source engineering

The strongest external code-review evidence is my contribution to AMD ROCm's hipDNN Python bindings.

<a href="https://github.com/ROCm/rocm-libraries/pull/15453">
  <img src="https://github.com/ROCm.png?size=128" width="76" height="76" alt="AMD ROCm logo" />
</a>

**[ROCm/rocm-libraries — PR #15453](https://github.com/ROCm/rocm-libraries/pull/15453)**

The change exposes Graph lifecycle, tensor inspection, compiled-plan serialization and runtime shape-override APIs to Python. The maintainer approved the latest revision; the PR status should be checked live on GitHub before describing it as merged.

[Read the contribution case study](case-studies/amd-rocm-hipdnn-python-bindings.md) · [View the complete contribution index](open-source-contributions.md)

---

## How to evaluate this portfolio

| Hiring signal | Best starting point | Evidence to inspect |
|---|---|---|
| Python/backend engineering | Enterprise Analytics Copilot | Service boundaries, SQL guard, tests, API |
| Applied AI / RAG engineering | Trade Finance Document Intelligence | Parsing, retrieval/extraction workflow, verification |
| LLM evaluation / reliability | LLM Evaluation & Observability | Adapters, evaluator design, regression and release gates |
| Agent orchestration | SWARM | Routing, specialist agents, clarification and execution |
| Research ability | Evidence-to-Action Reliability | Hypotheses, methodological gates, provenance and limitations |
| External code review | AMD ROCm PR | Diff, review history, tests and maintainer response |

## Contact

- [Email](mailto:todkarsant@gmail.com)
- [LinkedIn](https://in.linkedin.com/in/santosh-sadashiv-todkar)
- [Phone: +91 77440 04068](tel:+917744004068)

**All technical claims should be judged against the linked source code, tests, documentation and upstream review records.** This portfolio is intended to make that verification straightforward.
