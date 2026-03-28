# Phase 03 Discussion Log

**Date:** 2026-03-28
**Phase:** 03 - Ranking Engine

## User Decisions

- Use the Bayesian average formula for ranking.
- Fix the global baseline `C` to `4.2`.
- Fix the minimum reviews threshold `m` to `50`.
- Keep scores on the `0-5` scale.
- If ranking data is missing, keep the place but mark it unranked.
- Do not add any additional minimum-review filter beyond `m=50` inside the formula.
- Break ties using `user_ratings_total`.
- Return the full dataset with `is_ranked` and `rank_order`.

## Outcome

Discussion fully specified the Phase 3 ranking contract and was sufficient to implement directly.
