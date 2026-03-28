# Phase 2: Places Retrieval Pipeline - Context

**Gathered:** 2026-03-28
**Status:** Ready for planning

<domain>
## Phase Boundary

Retrieve live Google Places data from the Phase 1 `SearchQuery`, resolve the user-entered city to a location center, fetch up to three pages of place results, normalize them into a clean dataset, and remove duplicate or non-operational results. This phase does not rank places, cache searches, or present the final results UI beyond providing structured retrieval outputs for later phases.

</domain>

<decisions>
## Implementation Decisions

### Retrieval Strategy
- **D-01:** Phase 2 should geocode the city name first, then use the resolved center point plus radius to drive places retrieval.
- **D-02:** The places query should use only the category text, not a combined `"category in city"` query string.
- **D-03:** Retrieval should aim for balanced behavior between recall and locality rather than aggressively favoring one extreme.

### Geocoding Resolution
- **D-04:** Do not bias geocoding to Lithuania or any specific region; city input is now effectively global.
- **D-05:** If geocoding returns multiple plausible results, auto-pick the first result and continue, but log that choice in retrieval metadata.
- **D-06:** If geocoding cannot resolve a clear location, return a structured error object for the UI instead of raising a raw exception.

### Pagination
- **D-07:** Fetch up to three pages of Google Places results per search.
- **D-08:** Always fetch all available pages up to that three-page cap rather than stopping early based on intermediate quality judgments.
- **D-09:** If a later page fails after earlier pages succeeded, return the partial normalized dataset together with a warning.

### Normalized Dataset
- **D-10:** Every normalized place record must include `place_id`, `name`, `formatted_address`, `lat`, `lng`, `rating`, and `user_ratings_total`.
- **D-11:** Also preserve `types`, `business_status`, `price_level`, and `opening_hours` / open-now information when available in the source response.
- **D-12:** Keep missing `rating` or `user_ratings_total` values as null/empty in Phase 2 and let Phase 3 decide ranking eligibility.

### Search-Level Metadata
- **D-13:** Retrieval should return search-level metadata separately from the normalized place list.
- **D-14:** That metadata object must include `resolved_city_address`, geocoded center latitude/longitude, requested radius, and warning messages.
- **D-15:** Do not include source formatted location text separately beyond the resolved search metadata.

### Deduplication And Filtering
- **D-16:** Identify duplicates strictly by `place_id` in Phase 2; do not add heuristic duplicate matching yet.
- **D-17:** When the same `place_id` appears multiple times across pages, keep the most complete occurrence.
- **D-18:** Drop non-operational businesses during retrieval instead of passing them downstream.

### Empty And Failure States
- **D-19:** A successful geocode followed by zero place results is a normal empty result with metadata, not an error.
- **D-20:** Partial page failures should be surfaced as warnings in metadata rather than aborting the entire retrieval flow.

### the agent's Discretion
- Exact internal module layout for geocoding client, places client, and normalization helpers.
- Exact representation shape for warnings and logging fields, as long as it remains structured and testable.

</decisions>

<canonical_refs>
## Canonical References

**Downstream agents MUST read these before planning or implementing.**

### Phase scope and requirements
- `.planning/ROADMAP.md` - Phase 2 goal, requirement mapping, and success criteria for Places Retrieval Pipeline
- `.planning/PROJECT.md` - Product framing, global city-query context, and v1 boundaries
- `.planning/REQUIREMENTS.md` - Source requirements `RETR-01` and `RETR-02`

### Upstream phase contract
- `.planning/phases/01-search-foundation/01-CONTEXT.md` - Locked search-input decisions and `SearchQuery` boundary inherited by Phase 2
- `.planning/phases/01-search-foundation/01-UI-SPEC.md` - Phase 1 UI/query handoff expectations that the retrieval layer must consume cleanly

### Research and architecture guidance
- `.planning/research/SUMMARY.md` - Recommended build shape and separation of UI from service/retrieval logic
- `.planning/research/ARCHITECTURE.md` - Places client, search service, normalization flow, and build-order guidance

</canonical_refs>

<code_context>
## Existing Code Insights

### Reusable Assets
- `query.py`: defines the six-field `SearchQuery` dataclass plus normalization and validation helpers that should remain the input contract for retrieval
- `app.py`: already stores a successful `SearchQuery` in `st.session_state["search_query"]`, giving Phase 2 a clean integration point

### Established Patterns
- Query construction and validation are already isolated from Streamlit APIs
- The codebase favors thin UI orchestration with pure helper modules behind it
- Tests already exist around the query boundary, so retrieval logic should follow the same pure/helper-first pattern

### Integration Points
- Retrieval should consume `SearchQuery` rather than raw widget state
- A retrieval result object should be designed so later ranking and results phases can consume normalized places plus metadata without reopening this phase's decisions
- `app.py` should remain a caller of retrieval logic, not the place where pagination, deduplication, or geocoding rules live

</code_context>

<specifics>
## Specific Ideas

- City lookup is now effectively global, not Lithuania-biased, so resolved-location metadata matters for user trust
- The user wants radius control to remain meaningful, which is why the pipeline should geocode first and use radius-bound location search
- The pipeline should keep enough place detail for future ranking/filtering work without bloating v1 with presentation-only fields

</specifics>

<deferred>
## Deferred Ideas

None - discussion stayed within phase scope

</deferred>

---
*Phase: 02-places-retrieval-pipeline*
*Context gathered: 2026-03-28*
