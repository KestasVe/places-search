# Research Summary

## Stack

Use a minimal Python + Streamlit stack with `requests`, `pandas`, `python-dotenv`, and deployment via Streamlit Cloud. Keep secrets in `st.secrets` or environment variables, and add testing around ranking, pagination, and deduplication before expanding the app surface area.

## Table Stakes

The v1 product needs reliable city/category/radius search, paginated Google Places fetching, deduplication, Bayesian ranking, ranked table output, map output, and session caching. The core value is ranking trust, so every feature should reinforce "better than manual Google Maps sorting."

## Watch Out For

- Missing pagination will undercut result quality immediately.
- Weak or opaque ranking logic will make the app feel untrustworthy.
- Duplicate records will make the output look sloppy.
- Poor caching will waste API credits.
- Logic trapped inside `app.py` will slow future ranking enhancements.

## Planning Implications

- Build the fetch, transform, and ranking layers before investing in UI polish.
- Keep the score formula isolated and testable.
- Defer platform features that do not improve ranking trust or deployment readiness.
