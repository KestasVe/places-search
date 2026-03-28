---
phase: 05
slug: deployment-hardening
created: 2026-03-28
status: finalized
---

# Phase 05 Context

## Goal

Make the application safe and ready for public Streamlit Cloud deployment without changing the core search, retrieval, ranking, or results experience.

## Locked Decisions

- Support both Streamlit Cloud secrets and local `.env` files for API key configuration.
- Keep the API key precedence as:
  - `st.secrets["GOOGLE_PLACES_API_KEY"]`
  - environment variable fallback
- Check for the API key at app startup and stop execution before the search form appears if it is missing.
- Keep the Bayesian constants in code for now, but surface them clearly in a dedicated constants section.
- Add basic Google API error handling so provider failures become friendly user-facing messages rather than crashes.

## Inputs Available From Prior Phases

- Working Streamlit app shell with search, retrieval, ranking, table, map, and session caching
- Existing `.gitignore` with local secrets ignored
- Existing local `.env` placeholder path

## Constraints

- Do not introduce a permanent backend or config service.
- Keep Streamlit Cloud as the primary public deployment target.
- Preserve local developer ergonomics for `.env`-based startup.

## Implementation Boundary

- In scope:
  - startup configuration gating
  - deployment/setup documentation
  - secret-template files
  - Google API client error handling
  - repo hygiene for local secret placeholders
- Out of scope:
  - usage analytics
  - advanced quota management
  - infrastructure-as-code
