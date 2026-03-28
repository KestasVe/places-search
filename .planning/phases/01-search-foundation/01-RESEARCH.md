# Phase 1: Search Foundation - Research

**Date:** 2026-03-28
**Phase:** 01-search-foundation
**Requirements:** SRCH-01, SRCH-02, SRCH-03

## Research Question

What needs to be true for Phase 1 to produce a clean, testable Streamlit search shell that captures city, category, and radius inputs and converts them into a stable internal query shape?

## Recommended Build Shape

### Keep `app.py` as UI orchestration only

- `app.py` should render the page, collect widget state, display validation messages, and trigger a single orchestration function on `Search`.
- Input normalization and query-shaping logic should live outside the Streamlit widget code so it can be tested independently and reused by later phases.

### Introduce a lightweight query model now

- Phase 1 should define a small query representation that later phases consume instead of reading raw widget state directly.
- The normalized query payload should match the locked context decisions:
  - `city_raw`
  - `city_normalized`
  - `category_raw`
  - `category_normalized`
  - `radius_km`
  - `radius_m`
- Phase 1 should not add API-specific fields such as coordinates, geocoding output, pagination tokens, or request IDs.

### Separate normalization from validation

- Validation answers: "Can the user search yet?"
- Normalization answers: "What stable values will downstream code use?"
- This split matters because city/category requiredness is a UI concern, while trimming/collapsing/lowercasing is a data-shaping concern.

## Streamlit-Specific Guidance

### Form behavior

- An explicit `Search` button aligns with the requirement to avoid automatic reruns and future API cost waste.
- A form-style grouping keeps the interaction predictable even before real search execution exists.
- Inline field feedback is a better fit than global top-of-page errors for required city/category validation.

### Widget choices

- City: text input with English-first label plus a hint that Lithuanian and English names are both acceptable.
- Category: text input with placeholder examples only.
- Radius: slider with `1` to `50` km and default `10` km.

### Session-state boundary

- It is reasonable for Phase 1 to keep the normalized query in local session state or a returned local object after submit.
- Do not add caching, persistence, or retrieval triggers in this phase; that belongs later.

## Code Structure Recommendations

### Modules worth creating in Phase 1

- `app.py`
  - UI layout, widgets, submit flow, rendering validation feedback
- `src/query.py` or `query.py`
  - query dataclass / typed dict and normalization helpers
- `src/validation.py` or colocated helper module
  - field validation helpers for required input and radius range guarantees

If a `src/` package feels premature, a small local helper module beside `app.py` is still better than embedding normalization logic directly in the widget section.

### Stable function boundaries

- `normalize_text_input(raw: str) -> str`
- `build_search_query(city_raw: str, category_raw: str, radius_km: int) -> SearchQuery`
- `validate_search_inputs(city_raw: str, category_raw: str) -> dict[str, str]` or similar

These functions should remain independent of Streamlit APIs so they can be unit tested.

## Risks And Pitfalls For This Phase

### Over-coupling UI and future retrieval

- If the plan puts normalization or query construction inline inside the button handler, Phase 2 will need to untangle it before integrating retrieval.

### Premature geocoding assumptions

- The user explicitly deferred geocoding/location resolution to Phase 2.
- Phase 1 should not infer coordinates, city IDs, or Places request shapes beyond the normalized query object.

### Weak normalization rules

- If normalization is underspecified now, later phases may treat `" Vilnius "` and `"vilnius"` differently.
- The plan should make normalization behavior explicit and testable.

### Validation that blocks UX clarity

- Disabled submit plus inline guidance is the chosen interaction.
- Avoid plans that rely only on post-submit generic errors, because they conflict with the phase context.

## Planning Implications

- At least one plan should establish the query model and normalization helpers.
- At least one plan should wire the Streamlit UI to the query model and validation behavior.
- If the planner splits work into multiple plans, the query/validation foundation should precede the final UI wiring.
- Plans should preserve a thin `app.py` and avoid introducing retrieval, ranking, or caching concerns.

## Validation Architecture

### What should be verified in planning

- The generated plan must explicitly cover `SRCH-01`, `SRCH-02`, and `SRCH-03`.
- Plan tasks should prove the app can collect city, category, and radius inputs from the UI.
- Plan tasks should prove raw inputs are transformed into the agreed normalized query shape.
- Plan tasks should prove UI orchestration remains separated from future fetch/ranking logic.

### Concrete verification targets

- `app.py` contains a text input for city and a text input for category.
- `app.py` contains a slider configured for 1-50 km with a default of 10 km.
- A helper module defines the normalized query structure with the six required fields.
- A normalization/helper function lowercases normalized text while preserving raw display text.
- Validation logic blocks empty city/category searches and exposes inline feedback behavior.

### Suggested tests

- Unit tests for text normalization:
  - trims leading/trailing whitespace
  - collapses repeated internal spaces
  - lowercases normalized values
- Unit tests for query construction:
  - stores `radius_km`
  - converts `radius_m` correctly
  - preserves raw field values
- Lightweight UI-level check:
  - search action remains disabled or blocked when required fields are empty

## Research Summary

Plan Phase 1 around a small, testable query model plus a thin Streamlit form. The success condition is not visual polish; it is a clean boundary where validated user inputs become a stable normalized query object that later phases can consume without reworking the UI.
