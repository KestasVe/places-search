---
phase: 03
slug: ranking-engine
created: 2026-03-28
status: finalized
---

# Phase 03 Context

## Goal

Produce a trustworthy ordered result set from normalized Google Places data using a stable Bayesian ranking contract.

## Locked Decisions

- Use the Bayesian weighted-score formula:
  - `score = (v / (v + m)) * R + (m / (v + m)) * C`
- Fix `C = 4.2` as the global baseline rating.
- Fix `m = 50` as the minimum reviews threshold used by the formula.
- Keep scores on the same `0-5` scale as the raw Google rating.
- If `rating` or `user_ratings_total` is missing:
  - keep the place in the dataset
  - mark it as unranked
  - do not assign a score
- Do not add any extra minimum-review filter beyond the Bayesian formula itself.
- Break ties by `user_ratings_total`.
- Return the full dataset with:
  - `is_ranked`
  - `rank_order`
- Preserve ranking metadata needed for later UI trust and explanation.

## Inputs Available From Prior Phases

- Normalized places from `RetrievalResult.places`
- Preserved nullable `rating` and `user_ratings_total` values from Phase 2

## Constraints

- Keep the ranking layer separate from retrieval transport and Streamlit UI orchestration.
- Keep ranking deterministic for repeated identical inputs.
- Preserve original place fields so later phases do not need to rejoin ranking data with retrieval data.

## Implementation Boundary

- In scope:
  - score calculation
  - ranked vs unranked eligibility handling
  - deterministic ordering
  - ranking result metadata
  - ranking tests
- Out of scope:
  - final table/map presentation
  - alternate ranking modes
  - user-tunable weighting
