# Phase 2: Places Retrieval Pipeline - Discussion Log

> **Audit trail only.** Do not use as input to planning, research, or execution agents.
> Decisions are captured in CONTEXT.md - this log preserves the alternatives considered.

**Date:** 2026-03-28
**Phase:** 2-places-retrieval-pipeline
**Areas discussed:** Places API flow, Pagination rules, Normalization shape, Deduplication policy, Failure handling

---

## Places API flow

| Option | Description | Selected |
|--------|-------------|----------|
| Text Search + geocode-first | Geocode the city, then run a radius-bound places query using the category text | x |
| Text query with city phrase | Use combined text like `category in city` as the main retrieval strategy | |
| Hybrid fallback | Mix both approaches as first-class retrieval modes | |

**User's choice:** Geocode first, then use a Text Search-style places flow with the category text and the resolved center/radius.
**Notes:** No Lithuania bias should be added. If multiple geocoding results appear, auto-pick the first and log the choice. If geocoding fails, return a structured error object. Balanced recall/locality is preferred.

---

## Pagination rules

| Option | Description | Selected |
|--------|-------------|----------|
| Up to 3 pages, always fetch | Retrieve all available pages up to the cap | x |
| Adaptive stop | Stop early when later pages look low-value | |
| Single-page only | Keep retrieval cheap but incomplete | |

**User's choice:** Fetch up to 3 pages and always exhaust that cap when pages are available.
**Notes:** If a later page fails, return the partial normalized dataset with a warning rather than failing the whole search.

---

## Normalization shape

| Option | Description | Selected |
|--------|-------------|----------|
| Lean ranking/map baseline | Keep only `place_id`, name, address, coordinates, rating, and review count | |
| Baseline plus future-useful fields | Keep the baseline and preserve additional status/filtering fields | x |
| Presentation-heavy payload | Keep large UI-oriented payloads in retrieval | |

**User's choice:** Keep the ranking/map baseline plus `types`, `business_status`, `price_level`, and `opening_hours` / open-now when available.
**Notes:** Search-level metadata should be separate from place rows and include resolved city/address, center coordinates, requested radius, and warnings. Missing `rating` or `user_ratings_total` should be preserved for Phase 3 to decide on ranking eligibility.

---

## Deduplication policy

| Option | Description | Selected |
|--------|-------------|----------|
| Strict `place_id` dedupe | Treat only identical `place_id` values as duplicates | x |
| Heuristic dedupe | Merge near-identical name/address/location records even if IDs differ | |
| No dedupe in Phase 2 | Push duplicate handling later | |

**User's choice:** Strict `place_id` dedupe only.
**Notes:** When duplicates appear across pages, keep the most complete occurrence. Drop non-operational businesses during retrieval.

---

## Failure handling

| Option | Description | Selected |
|--------|-------------|----------|
| Structured error/empty handling | Return typed metadata-driven outcomes for ambiguous, failed, or empty retrievals | x |
| Raw exception flow | Let retrieval errors bubble up directly | |
| Hard-fail partials | Fail the whole search on later-page or geocoding issues | |

**User's choice:** Structured retrieval outcomes.
**Notes:** Zero place results after successful geocoding should be treated as a normal empty result with metadata. Geocoding failures should return structured errors. Multiple geocoding matches should auto-pick the first result and log it.

---

## the agent's Discretion

- Internal module boundaries for geocoding, places retrieval, and normalization
- Exact warning/error schema details

## Deferred Ideas

None
