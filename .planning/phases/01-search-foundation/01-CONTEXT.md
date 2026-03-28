# Phase 1: Search Foundation - Context

**Gathered:** 2026-03-28
**Status:** Ready for planning

<domain>
## Phase Boundary

Build the Streamlit entry flow for collecting valid search inputs for city, category, and radius, and shape them into a stable internal query object. This phase does not perform Google Places retrieval, geocoding, ranking, caching, or result presentation.

</domain>

<decisions>
## Implementation Decisions

### City Input
- **D-01:** City is a required free-text input, not a predefined dropdown or curated city list.
- **D-02:** The UI should make it clear that both Lithuanian and English city names are acceptable.
- **D-03:** Phase 1 should store city input in a stable internal query shape now, while deferring geocoding and location resolution to Phase 2.

### Category Input
- **D-04:** Category/query is a required free-text field.
- **D-05:** The field should use a placeholder only, with examples such as `Kebabai`, `Museums`, and `Cafes`, rather than visible suggestions.
- **D-06:** Category input should use light normalization only: trim edges, collapse repeated spaces, preserve original display text, and generate a normalized lowercase value for internal use.

### Radius Input
- **D-07:** Radius uses a Streamlit slider control.
- **D-08:** Radius defaults to 10 km, with an allowed range from 1 km to 50 km.
- **D-09:** The internal query object should store both `radius_km` and `radius_m`, with meters treated as the API-ready value.

### Search Trigger and Validation
- **D-10:** Search runs only when the user clicks a `Search` button, never automatically on input changes.
- **D-11:** City and category are mandatory; the UI should show inline validation and keep the search action disabled until required fields are valid.
- **D-12:** The normalized query object for this phase should contain only `city_raw`, `city_normalized`, `category_raw`, `category_normalized`, `radius_km`, and `radius_m`.

### the agent's Discretion
- Exact visual layout between main content area and sidebar, as long as the chosen controls remain clear and consistent with the decisions above.
- Exact helper/error copy wording for the input fields.

</decisions>

<canonical_refs>
## Canonical References

**Downstream agents MUST read these before planning or implementing.**

### Phase scope and product intent
- `.planning/ROADMAP.md` - Phase 1 goal, requirements mapping, and success criteria for Search Foundation
- `.planning/PROJECT.md` - Product framing, deployment constraints, and v1 boundaries
- `.planning/REQUIREMENTS.md` - Source requirements `SRCH-01`, `SRCH-02`, and `SRCH-03`

### Research that shapes implementation
- `.planning/research/SUMMARY.md` - Recommended build shape, especially the thin UI boundary and stable search flow
- `.planning/research/ARCHITECTURE.md` - Search service boundary, normalized query flow, and build-order guidance

</canonical_refs>

<code_context>
## Existing Code Insights

### Reusable Assets
- `app.py`: existing Streamlit shell with page config, title/caption, placeholder city/category/radius controls, and secrets-loading helper that can be extended rather than replaced

### Established Patterns
- Streamlit is already the chosen UI framework, and the current scaffold keeps application logic thin at the top level
- Secrets are already resolved through `st.secrets` with environment fallback, which should remain untouched by Phase 1 search input work

### Integration Points
- `app.py` is the immediate integration point for the Phase 1 search form and normalized query object
- Future retrieval logic should consume the normalized query shape produced by this phase rather than reading raw widget state directly

</code_context>

<specifics>
## Specific Ideas

- Users may enter either Lithuanian or English city names, so the UI should signal that both are valid
- Example category placeholders should feel concrete and local, such as `Kebabai`, `Museums`, and `Cafes`
- The radius choice should feel practical for Lithuanian city searches: 10 km default, but broad enough to reach nearby towns or parks when needed

</specifics>

<deferred>
## Deferred Ideas

None - discussion stayed within phase scope

</deferred>

---
*Phase: 01-search-foundation*
*Context gathered: 2026-03-28*
