# Day 18 — Capstone Day 4: Add Guardrails and Caching

Today, I built the security, privacy, and caching layer for the Capstone project (**Cohort IQ**) and deployed the application live.

## Key Work Completed

1. **Prompt Injection Guard (Exercise 3):** Wired the standalone `is_injection_attempt()` validation function into `app.py` to intercept and block adversarial queries (such as jailbreaks, DAN prompts, and system prompts leaks) before they touch Chroma or the Gemini API, returning a friendly warning: *"Couldn't process that question — try rephrasing it."*
2. **Double-Layer Caching (Exercise 4):** 
   - **Resource Caching:** Verified Streamlit `@st.cache_resource` caching for expensive model-loading and database connection setups.
   - **Response Caching:** Added a session-state query response cache that intercepts identical queries and serves answers instantly in **0.02 seconds**, bypassing the LLM pipeline entirely.
3. **PII Check & Upload Policy (Exercise 5):** Evaluated PII checking on uploads. Since Cohort IQ reads static coursework documents directly from the local disk and does not expose a document upload widget in the UI, we documented this exception in `SPEC.md` and added input PII checks directly onto the user's search queries.
4. **Architecture Diagram (Exercise 6):** Developed a visual 2D system architecture diagram (`architecture.png`) outlining the components and exact data flows, and integrated it into the repository.
5. **Live Deployment (Exercise 8):** Added fallback configuration for `st.secrets` inside `core.py` and successfully deployed the RAG companion live on Streamlit Cloud.

## Code Location

All actual source code files for the Capstone project (**Cohort IQ**) are managed in a standalone repository and linked directly to this workspace:
* **Standalone Repository:** [CohortIQ](https://github.com/absheerakk/CohortIQ)
* **Live Application:** [cohort-iq.streamlit.app](https://cohort-iq.streamlit.app/)
* **Local Submodule Path:** Linked as a Git submodule inside the `day15/` directory.