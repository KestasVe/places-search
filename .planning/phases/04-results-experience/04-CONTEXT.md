---
phase: 04
slug: results-experience
created: 2026-03-28
status: finalized
---

# Phase 04 Context

## Goal

Deliver the visible value of the app through clear ranked-results presentation, map inspection, feedback states, and cached repeat searches.

## Locked Decisions

- The main results surface uses a split view with a formatted ranked table on the left and an interactive map on the right.
- The main table shows the Top 20 ranked places by default.
- Table columns are `Rank`, `Name`, `Score`, `Rating`, `Reviews`, `Address`, `Price`, and `Open Now`.
- Formatting is human-readable:
  - price uses `$` repetition
  - open state uses `Open`, `Closed`, or `Unknown`
  - score and rating are rounded for display
- Unranked places stay in the dataset but are hidden by default behind a reveal control.
- Repeating an identical search should reuse cached results within the session via Streamlit caching.
- Runtime feedback must clearly cover missing API key, loading, retrieval warnings, zero-results state, retrieval/configuration failures, and rankable-data-missing state.

## Inputs Available From Prior Phases

- `SearchQuery` from Phase 1
- `RetrievalResult` from Phase 2
- `RankingResult` from Phase 3

## Constraints

- Do not change the Bayesian ranking formula in this phase.
- Keep the results formatting layer separate from retrieval and ranking logic.
- Preserve the Phase 2 and Phase 3 debug envelopes for inspection.
- Support a graceful map fallback if Folium dependencies are unavailable locally.

## Implementation Boundary

- In scope:
  - result formatting helpers
  - app layout for table and map
  - session caching through `st.cache_data`
  - clear feedback/status rendering
- Out of scope:
  - permanent storage
  - saved favorites
  - place details pages
  - alternate ranking modes
  - deployment documentation hardening beyond dependency declaration
