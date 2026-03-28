# Lithuania Places Ranker

## What This Is

Lithuania Places Ranker is a Python-based Streamlit web application that finds and ranks the best places in Lithuania using the Google Places API. It is designed for both local residents and tourists who want a faster way to compare places like kebab shops, museums, or cafes by combining rating quality and popularity into a more trustworthy ranking. In v1, the main experience is city-first search with a ranked results table and a map view.

## Core Value

Turn messy Google Maps browsing into a reliable ranked list where highly rated places with meaningful review volume beat misleading low-sample results.

## Requirements

### Validated

- [x] User can enter a Lithuanian city search as free text and submit a normalized query shell - Phase 1
- [x] User can enter a freeform category/query term and have it validated before search execution - Phase 1
- [x] User can set a search radius and hand off a stable query object with kilometer and meter values - Phase 1

### Active

- [ ] App fetches live Google Places results, including pagination where needed.
- [ ] App deduplicates fetched places before ranking them.
- [ ] App ranks places using a Bayesian weighted score based on Google rating and review count.
- [ ] App displays ranked results as a sortable table/dataframe.
- [ ] App displays the top ranked results on a map.
- [ ] App caches repeated searches within a session to reduce redundant API calls and cost.
- [ ] App is structured for public deployment on Streamlit Cloud.
- [ ] API credentials are loaded from `st.secrets` or environment variables rather than hardcoded.

### Out of Scope

- User accounts - not needed for validating the core ranking workflow.
- Permanent database storage - live queries plus session caching are sufficient for v1.
- Place detail pages - the v1 value is ranking and comparison, not deep place exploration.
- Saved favorites - not needed until the basic search-and-rank loop proves useful.
- Advanced filters such as price, open-now, or distance-based sorting - deferred to keep v1 focused on ranking quality.
- Lithuania-wide precomputed rankings - each search should be a fresh live query in v1.
- Mobile-specific optimization beyond normal Streamlit responsiveness - good enough for early validation.
- Multilingual interface - English UI is enough for v1, while query text may be any language.

## Context

- The product replaces manual Google Maps searching and "mental math" across rating and review counts.
- Primary users split into two overlapping groups:
  local residents tend to care about the "best" places by quality, while tourists often care about "most popular" places by social proof.
- The ranking model is the core differentiator. A Bayesian average is preferred to avoid overvaluing places with very few reviews.
- The UI should prioritize city/category search such as "Kebabai in Vilnius" or "Museums in Kaunas".
- Lithuania-wide ranking may be possible later through aggregation, but it is not the primary v1 experience.
- The application is expected to work across arbitrary city/category combinations as long as Google Places returns results.
- Streamlit is the intended framework, with `st.map` suitable for the initial map view.
- Deployment target is Streamlit Cloud, which implies clean dependency management, ignored local secrets, and environment-based API configuration.
- Current state: Phase 1 is complete, and the app now provides a validated search shell plus a normalized `SearchQuery` handoff for later retrieval and ranking phases.

## Constraints

- **Tech stack**: Python + Streamlit - chosen for fast iteration, simple deployment, and built-in table/map UI primitives.
- **API dependency**: Google Places API - ranking depends on live external search data.
- **Secrets handling**: No hardcoded API key - required for safe public deployment and repository hygiene.
- **Data model**: No permanent database in v1 - keeps the first release lean and avoids unnecessary persistence complexity.
- **Caching**: Session/local caching only - reduces repeated API spend without adding database infrastructure.
- **Ranking scope**: Rating + review count only in v1 - keeps the scoring logic focused and explainable.
- **Deployment**: Streamlit Cloud compatibility - project structure should support straightforward hosted deployment.

## Key Decisions

| Decision | Rationale | Outcome |
|----------|-----------|---------|
| Use Streamlit for the web app | Fastest path to a usable public-facing tool with built-in table and map support | - Pending |
| Optimize ranking with a Bayesian weighted score | Avoids naive "5.0 with 2 reviews" results outranking well-established places | - Pending |
| Prioritize city/category search in v1 | Matches the most concrete and useful user workflow | ✓ Good |
| Use live Google Places queries with session caching | Keeps data fresh while avoiding unnecessary repeated API calls | - Pending |
| Prepare the repo for Streamlit Cloud deployment from the start | Prevents rework around secrets and packaging later | ✓ Good |

## Evolution

This document evolves at phase transitions and milestone boundaries.

**After each phase transition** (via `$gsd-transition`):
1. Requirements invalidated? -> Move to Out of Scope with reason
2. Requirements validated? -> Move to Validated with phase reference
3. New requirements emerged? -> Add to Active
4. Decisions to log? -> Add to Key Decisions
5. "What This Is" still accurate? -> Update if drifted

**After each milestone** (via `$gsd-complete-milestone`):
1. Full review of all sections
2. Core Value check - still the right priority?
3. Audit Out of Scope - reasons still valid?
4. Update Context with current state

---
*Last updated: 2026-03-28 after Phase 1 completion*
