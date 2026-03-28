# Research Summary

## Stack

Use a lean Python stack centered on Streamlit, `requests`, `pandas`, and isolated scoring/service modules. Secrets should load from `st.secrets` in deployment with environment-variable fallback locally.

## Table Stakes

The essential v1 loop is:

1. city/category/radius input
2. live Google Places fetch with pagination
3. deduplication
4. Bayesian ranking
5. ranked table plus map
6. caching to control repeat API cost

## Recommended Build Shape

- Keep `app.py` thin
- Isolate Google Places access in a client
- Isolate ranking math in pure functions
- Use a search service to orchestrate fetch, clean, rank, and return

## Watch Out For

- Naive sorting by raw rating
- Incomplete pagination
- Duplicate results
- Streamlit reruns causing repeated API calls
- Secrets/config drift between local and Streamlit Cloud
- Scope creep into accounts, persistence, or advanced filters before ranking quality is validated

## Implications For Requirements And Roadmap

- Early phases should establish project structure, secrets handling, and thin UI boundaries.
- A dedicated phase should cover API integration, pagination, deduplication, and caching.
- A dedicated phase should cover ranking logic and score explainability.
- The roadmap should defer persistence, social features, and advanced filters.
