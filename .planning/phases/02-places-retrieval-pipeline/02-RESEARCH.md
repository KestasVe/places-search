# Phase 2: Places Retrieval Pipeline - Research

**Date:** 2026-03-28
**Phase:** 02-places-retrieval-pipeline
**Requirements:** RETR-01, RETR-02

## Research Question

What needs to be true for Phase 2 to retrieve live Google Places data from the Phase 1 `SearchQuery`, paginate reliably, normalize the results into a clean dataset, and remove duplicate or non-operational entries without pulling ranking or UI concerns into the retrieval layer?

## Recommended Build Shape

### Keep retrieval behind a service boundary

- `app.py` should continue to act as orchestration only.
- Retrieval work should live behind a service entry point that accepts a `SearchQuery` and returns a structured retrieval result.
- Phase 2 should not expose raw Google API responses directly to the UI.

### Split geocoding, places access, and normalization

- Use a small geocoding helper/client to resolve the city string into a center point plus formatted address.
- Use a dedicated Places client to execute the category query and paginate up to three pages.
- Use pure normalization/deduplication helpers to shape place records and retrieval metadata.

### Return one structured retrieval envelope

- Phase 2 should return:
  - `places`: normalized place records
  - `metadata`: resolved city/address, center coordinates, requested radius, page count, and warnings
  - `error`: structured failure details only when geocoding/search setup fails
- This keeps later phases from reinterpreting partial failure states ad hoc.

## Current Codebase Implications

### Existing contract to preserve

- `query.py` already defines the Phase 1 `SearchQuery` contract and should remain the only search-input source of truth.
- `app.py` already stores `SearchQuery` in `st.session_state["search_query"]`, so retrieval should consume that object rather than reconstructing inputs from widgets.
- Current patterns favor pure helpers and thin UI code; retrieval should follow that shape.

### Recommended new module boundaries

- `places_client.py`
  - Google Places requests
  - pagination token handling
  - raw response collection
- `geocoding.py` or `location_client.py`
  - city resolution
  - structured geocoding success/error return
- `retrieval.py`
  - orchestration from `SearchQuery` -> geocode -> places pages -> normalization -> metadata
- `place_models.py` or colocated dataclasses
  - normalized place record
  - retrieval metadata / result envelope

If introducing a `src/` package feels premature, flat root-level modules are still preferable to embedding retrieval logic in `app.py`.

## Retrieval Strategy Guidance

### Geocode first, then search by radius

- This is the correct fit for the user decisions because the radius must remain meaningful.
- Use the city text only to resolve a center point and formatted location.
- Use the category text as the actual Places search term.
- Do not concatenate `"category in city"` into the places query because that weakens the explicit radius contract.

### Ambiguous geocoding behavior

- If multiple geocoding results appear, Phase 2 should auto-pick the first result and record a warning or resolution note in metadata.
- If geocoding fails entirely, return a structured retrieval error object instead of raising raw transport exceptions up into the UI.
- Because the user explicitly removed Lithuania bias, planners should avoid region restriction assumptions in the default implementation.

## Pagination Guidance

### Always exhaust up to the cap

- Phase 2 should fetch all pages up to three pages whenever the API exposes them.
- The stopping conditions should be explicit:
  1. no next-page token
  2. three pages reached
  3. a subsequent page call fails

### Handle partial page failure as degraded success

- If page 1 succeeds and page 2 or 3 fails, the retrieval result should still return normalized data from successful pages.
- That failure should be represented as a warning in metadata rather than an exception that discards useful data.
- Tests should assert this degraded-success path because it is part of the locked contract.

## Normalization And Deduplication Guidance

### Minimum normalized place shape

Each normalized place record should carry at least:

- `place_id`
- `name`
- `formatted_address`
- `lat`
- `lng`
- `rating`
- `user_ratings_total`
- `types`
- `business_status`
- `price_level`
- `opening_hours` or open-now value when available

### Keep retrieval metadata separate

Search-level metadata should not be repeated into every place row. Keep it once in the result envelope:

- `resolved_city_address`
- `center_lat`
- `center_lng`
- `requested_radius_m`
- `requested_radius_km`
- warnings / resolution notes

### Strict duplicate identity for v1

- Deduplicate by `place_id` only in Phase 2.
- If the same `place_id` appears multiple times, keep the most complete record rather than the first.
- A simple completeness heuristic is enough for planning:
  - prefer more non-null required fields
  - prefer records with richer optional fields when required fields tie

### Filter non-operational places during retrieval

- This is a retrieval concern now, not a ranking concern later.
- Drop any place whose `business_status` is present and not `OPERATIONAL`.
- Keep places with missing rating/review-count values; Phase 3 will decide whether they are rankable.

## Error And Empty-State Shape

### Geocoding failure

- Return a structured error object with at least:
  - `code`
  - `message`
  - `query_context`
- This should be deterministic and UI-safe, not a raw `requests` exception string.

### Empty result after successful geocode

- Treat as a normal retrieval result with:
  - empty `places`
  - filled metadata
  - no fatal error
- This distinction matters because later UI and caching phases need to treat true empty search results differently from failed lookups.

## Testing And Planning Implications

### What the planner should ensure

- One plan should establish the retrieval models and pure normalization/deduplication rules.
- One plan should cover external clients and pagination/error-handling logic.
- At least one plan should prove retrieval remains testable without Streamlit UI execution.

### Useful test targets

- geocoding success returns resolved center + formatted address
- geocoding failure returns a structured error object
- pagination stops at three pages even if more tokens appear
- partial page failure returns normalized data plus warning metadata
- duplicate `place_id` rows collapse to one normalized record
- non-operational businesses are removed before returning the dataset
- missing `rating` or `user_ratings_total` survives normalization

## Risks And Pitfalls For This Phase

### Mixing transport logic with normalization

- If Google response parsing, deduplication, and orchestration all live in one large function, the phase becomes hard to test and hard to evolve in Phase 3/4.

### Treating ambiguous geocoding as a UI problem only

- The retrieval layer itself must encode the selected resolved location and warning, otherwise downstream code cannot explain why results were chosen from a particular location.

### Assuming Places responses are uniform

- Optional fields like `price_level`, `opening_hours`, `rating`, or `user_ratings_total` may be absent.
- Normalizers should tolerate sparse data rather than failing on missing keys.

### Letting deduplication creep into heuristics too early

- The user explicitly chose strict `place_id` dedupe in Phase 2.
- Heuristic duplicate matching belongs to a later phase only if real evidence demands it.

## Validation Architecture

### What planning should verify

- The phase must consume the existing `SearchQuery` instead of reading raw widget values.
- The retrieval layer must geocode first, then run category-only Places search bounded by radius.
- The returned data must include a normalized place list plus separate metadata.
- Duplicate handling and non-operational filtering must be deterministic and testable.

### Concrete verification targets

- retrieval code imports and accepts `SearchQuery`
- a normalized place model contains `place_id`, `name`, `formatted_address`, `lat`, `lng`, `rating`, and `user_ratings_total`
- retrieval metadata contains resolved location and warnings
- pagination code enforces a three-page maximum
- deduplication is keyed on `place_id`
- non-operational businesses are excluded from returned places

### Suggested tests

- unit tests for normalization and deduplication
- mocked client tests for three-page pagination and partial page failure
- service-level tests for geocoding error vs empty-result behavior

## Research Summary

Plan Phase 2 around a geocode-first retrieval service that accepts the Phase 1 `SearchQuery`, calls Google clients behind clean module boundaries, and returns one structured retrieval envelope containing normalized places plus search metadata. The critical planning risk is not API wiring itself; it is preserving a clean separation between UI, transport, normalization, and future ranking concerns.
