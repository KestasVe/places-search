# AGENTS

## Project

**Lithuania Places Ranker**

Lithuania Places Ranker is a Python-based Streamlit web application that finds and ranks the best places in Lithuania using the Google Places API. It is designed for both local residents and tourists who want a faster way to compare places like kebab shops, museums, or cafes by combining rating quality and popularity into a more trustworthy ranking. In v1, the main experience is city-first search with a ranked results table and a map view.

**Core Value:** Turn messy Google Maps browsing into a reliable ranked list where highly rated places with meaningful review volume beat misleading low-sample results.

## Stack

- Streamlit app shell
- Python 3.11+
- `requests` for Google Places API calls
- `pandas` for shaping and ranking result data
- `python-dotenv` for local environment loading
- `st.secrets` or environment variables for secrets

## Architecture Guidance

- Keep `app.py` thin and focused on UI orchestration.
- Put Google Places fetching behind a dedicated client module.
- Keep Bayesian scoring in a separate pure-Python module.
- Keep normalization and deduplication logic separate from the UI.

## Workflow Guidance

- Prefer working through GSD commands so planning artifacts stay in sync.
- Current project state is defined in `.planning/PROJECT.md`, `.planning/REQUIREMENTS.md`, `.planning/ROADMAP.md`, and `.planning/STATE.md`.
- Start with `$gsd-discuss-phase 1` or `$gsd-plan-phase 1` for implementation work.
