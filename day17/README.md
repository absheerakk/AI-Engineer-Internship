# Day 17 — Capstone Day 3: Add the Interface
Today, I built the user interface layer for the Capstone project (**Cohort IQ**) using Streamlit and custom CSS styling.
## Key Work Completed
1. **Thin UI Architecture (Exercise 1):** Built the Streamlit interface inside `app.py`, ensuring all backend calculations and semantic database operations are imported directly from `core.py` without code duplication.
2. **Telemetry & Loading States (Exercise 2):** Wrapped all slow operations (embedding model loading, document indexing, and generative response synthesis) in specific, user-friendly `st.spinner` states.
3. **Structured Error Handling (Exercise 3):** Replaced raw Python tracebacks with clean UI callout boxes, gracefully handling API key errors and internet disconnection issues.
4. **obvious Edge Cases (Exercise 4):**
   - **Empty Inputs:** Warns the user if they submit a query with whitespace or empty text.
   - **No Data Loaded:** Natively disables the input box and search button if the Chroma database is empty.
   - **Very Long Input:** Displays a warning callout if a query exceeds 1,000 characters.
   - **Repeated Rapid Submissions:** Implemented a `st.session_state.busy` lock to prevent multiple button clicks from flooding the Gemini API.
   - **No Good Answer:** Gracefully displays the fallback warning and hides the source citation grid.
5. **Incremental Commits (Exercise 5):** Committed the progress incrementally to build a granular development history.
## Code Location
All actual source code files for the Capstone project (**Cohort IQ**) are managed in a standalone repository and linked directly to this workspace:
* **Standalone Repository:** [CohortIQ](https://github.com/absheerakk/CohortIQ)
* **Local Submodule Path:** Linked as a Git submodule inside the `day15/` directory.
