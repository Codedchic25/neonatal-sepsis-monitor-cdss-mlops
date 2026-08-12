# 📑 TACTICAL INTERVIEW SCENARIOS: ARCHITECTURE DEFENSE

This document outlines core technical questions, architectural trade-offs, and continuous verification defenses designed to guide engineering discussions and senior-level production reviews for the Sepsis Monitor AI platform.

---

## 🏗️ Section 1: System Architecture & LLM Integration

### Q1: Why choose a hybrid model instead of allowing the LLM to calculate the clinical risk score or biomarker degradation directly?
> "In high-acuity medical domains, determinism is non-negotiable. Large Language Models (LLMs) inherently exhibit probabilistic behavior, exposing mission-critical systems to semantic hallucinations or mathematical rounding errors. You cannot risk a neonatal patient's life on statistical approximations.
>
> To mitigate this, I enforced a strict Separation of Concerns:
> *   **Mathematical Core:** All telemetry vectors, clinical dynamics, and first-order pharmacokinetic degradation loops are executed in deterministic, rigid Python functions.
> *   **Generative AI Layer:** The `llama-3.1-8b-instant` model via Groq LPU infrastructure serves exclusively as a contextual decision-support engine. It synthesizes pre-calculated data, enriches it via local RAG matrices, and formats it within safety guardrails."

### Q2: What happens if cloud connectivity drops or the Groq API returns a rate-limit exception? Does the application freeze?
> "No, the architecture leverages a Graceful Degradation model backed by a fail-safe local deterministic interceptor.
>
> The inference pipeline is encapsulated inside a defensive `try-except` block catching specific `GroqError` exceptions to avoid blind catches. If a network timeout, HTTP 503 error, or credential failure occurs, the application intercepts the exception, triggers a monitoring log entry, and immediately forces a local fallback routing via `_generate_local_fallback`. The user interface remains uninterrupted, displaying real-time telemetry metrics and generating hardcoded localized NICU protocol instructions without downtime."

---

## 💾 Section 2: Data Management & Session Persistence

### Q3: Why implement a dedicated Context Manager via `@contextmanager` for SQLAlchemy sessions instead of a global shared session?
> "Streamlit is natively multi-threaded; every UI interaction triggers a full script re-execution on a newly allocated concurrent thread. Sharing a global SQLAlchemy session across concurrent client runs introduces immediate race conditions, connection leaks, and SQLite connection locks.
>
> Adopting the `@contextmanager` pattern guarantees absolute transactional isolation:
> *   Every I/O transaction instantiates its own localized, thread-bound database connection session.
> *   The session automatically commits data on success or triggers a rollback sequence upon hitting clinical or system exception bounds.
> *   The `finally` block forces an explicit `db.close()`, returning handlers to the pool and neutralizing memory leaks."

### Q4: How is data isolation maintained during automated tests? Is there a risk of polluting the physical production SQLite database during a Pytest run?
> "The isolation boundary is complete. In `tests/conftest.py`, I configured a high-scope fixture hook that dynamically overrides the active database connection string, swapping it for an isolated, volatile in-memory instance (`sqlite:///:memory:`).
>
> If a violation occurs, a `ClinicalGuardrailException` forces an automated hot swap to our safe deterministic local fallback, locking the persistent array directly inside `sepsis_neonatal.db`.

---

## 🛡️ Section 3: Security, MLOps, & Natural Language Validation

### Q5: How does continuous evaluation with the `promptfoo` framework safeguard the LLM inference pipeline, and what specific clinical vulnerabilities does it evaluate?
> "`promptfoo` serves as the automated MLOps evaluation pillar within our Continuous Integration (CI) pipeline, resolving the issue that natural language outputs cannot be validated via simple strict equality (`==`) strings.
>
> Following significant updates, we run automated security audits directly against live Groq endpoints to evaluate system immune responses:
> *   **Deterministic NLP Assertions:** Utilizing the `contains` assert type to guarantee that required first-line antibiotic protocols (**Ampicillin + Gentamicin**) are present in the completion text.
> *   **Semantic Similarity Score:** Evaluating report outputs against verified clinical reference baselines using stabilized thresholds (e.g., minimum 0.75 similarity).
> *   **Linguistic Parsing Evaluations:** Injecting specialized JavaScript criteria to verify formatting compliance and ensure output strings match the active locale language dictionary."

### Q6: Detail your prompt injection prevention strategy. How does the codebase stop a user from hijacking the LLM?
> "Jailbreak and injection attacks attempt to override system rules by passing adversarial strings through input vectors. The platform blocks these attempts using a multi-tiered hardening perimeter:
>
> 1.  **Input Token Truncation & Pre-Processing:** Text inputs passed into the metric payloads are strictly truncated (`[:30]`) to mechanically cripple long payload injection commands before prompt construction.
> 2.  **Strict Inference Configuration:** By pinning the model temperature to `0.1`, we minimize creative freedom, forcing the model to remain purely deductive and highly resistant to behavioral shifts.
> 3.  **Post-Inference Structural Guardrails:** The code features a dedicated `NeonatalOutputGuardrail` layer in `guardrails.py` tested by `pytest`. This layer reviews the raw completion using regular expressions to enforce absolute XML block compliance (`<RAPORT>`, `<MEDICATIE>`, `<FCC>`) and trap extreme hallucinated medical numbers (>500mg) before they reach the user viewport. If a violation occurs, a `ClinicalGuardrailException` forces an automated hot swap to our safe deterministic local fallback."

### Q7: Detail a real-world alignment failure discovered during prompt testing and explain how the codebase was hardened against it.
> "During adversarial testing with a high-severity payload—such as `SYSTEM OVERRIDE: IGNORE PREVIOUS INSTRUCTIONS`—I observed a localized semantic degradation vector. While the LLM correctly identified the high sepsis risk, it suffered language drift, generating English headings (e.g., 'CLINICAL FINDINGS') despite a strict Romanian locale request (`lang: 'RO'`).
>
> To neutralize this jailbreak vector, I hardened the system instruction anchoring by appending a final `MANDATORY FORMAT OBLIGATION` constraint. Furthermore, the application is wrapped to catch any parsing anomalies or locale breaking in `medical_expert.py` and immediately trigger the deterministic safe local report overlay in the correct language."

---

## 🔬 Section 4: Medical Logic & Pharmacokinetics

### Q8: Why did you integrate distinct biological half-lives for CRP (19h) and PCT (24h) into the telemetry engine?
> "To closely replicate the physiological and pathophysiological reality encountered in an actual Neonatal Intensive Care Unit (NICU) workspace.
>
> The two biological indicators follow entirely separate kinetics:
> *   **Procalcitonin (PCT):** An extremely specific biomarker for severe bacterial infections and neonatal sepsis. It rises rapidly and has a documented biological half-life of approximately 24 hours.
> *   **C-Reactive Protein (CRP):** A slower, non-specific acute-phase reactant presenting an independent clearance dynamic with an approximate half-life of 19 hours.
>
> By modeling these variables as independent first-order exponential decay curves using the classic pharmacokinetics equation $C(t) = C_0 \cdot e^{-k \cdot \Delta t}$, where $k = \ln(2) / t_{1/2}$, the interactive `st.line_chart` viewport renders realistic asynchronous trends. This architectural choice allows clinicians to audit treatment efficacy far more accurately than would be possible with a basic linear random-noise script, providing a clear visual representation of biological clearance under active therapeutic protocols."

### Q9: How do non-pharmacological Family-Centered Care (FCC) variables mathematically influence patient telemetry and toxin clearance constants?
> "The platform handles supportive non-pharmacological interventions as active clinical parameters that execute mutations across both the presentation viewports and the mathematical simulation layers:
>
> *   **UI Presentation Layer (Stress Reduction):** Activating variables like Kangaroo Care or Music Therapy functions as a structural defense against clinical **Alarm Fatigue**. The dashboard applies an automatic stabilization modifier that decreases the recorded heart rate by 15 bpm and mitigates hypoxemia by adding a +3% factor to the active Oxygen Saturation (SpO2) metric, closely simulating newborn autonomic nervous system recovery.
> *   **Mathematical Simulation Layer:** The chosen neonatal nutritional pathway alters the biological clearance velocity constant ($k$) directly. Selecting maternal breast milk via the dropdown option **`nutrition_type_active="Exclusive Breastfeeding"`** injects an explicit clearance multiplier of 1.15 into the first-order exponential decay formula. This choice accelerates biomarker elimination by 15% to mathematically replicate the passive immune protection and enzymatic clearance benefits of maternal antibodies.
>
> All modified physiological states and therapeutic variables are persistently logged via SQLAlchemy transaction sessions directly into the `NeonatalTelemetry` SQLite data rows on every simulated hourly step, maintaining absolute audit trails."
