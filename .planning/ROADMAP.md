# Roadmap: Lithuania Places Ranker

**Created:** 2026-03-28
**Granularity:** Coarse
**Execution:** Parallel where safe, sequential where dependencies require
**Coverage:** 12 / 12 v1 requirements mapped

## Phase Summary

| # | Phase | Goal | Requirements | Success Criteria |
|---|-------|------|--------------|------------------|
| 1 | Search Foundation | Capture valid user search inputs and establish the application shell | SRCH-01, SRCH-02, SRCH-03 | 3 |
| 2 | Places Retrieval Pipeline | Fetch and normalize live Google Places results reliably | RETR-01, RETR-02 | Complete (2/2 plans, 2026-03-28) |
| 3 | Ranking Engine | Produce trustworthy ordered results from normalized place data | RANK-01, RANK-02 | Complete (1/1 plans, 2026-03-28) |
| 4 | Results Experience | Present ranked results clearly with map, feedback states, and cached repeat searches | VIEW-01, VIEW-02, VIEW-03, PLAT-01 | Complete (1/1 plans, 2026-03-28) |
| 5 | Deployment Hardening | Make the app ready for public Streamlit Cloud deployment | PLAT-02 | 3 |

## Phase Details

### Phase 1: Search Foundation

**Goal:** Build the Streamlit entry flow for selecting city, category, and radius so searches can be initiated consistently.

**Requirements:** SRCH-01, SRCH-02, SRCH-03

**UI hint**: yes

**Success criteria:**
1. User can select a supported Lithuanian city, enter a category, and set a radius from the app UI.
2. Search inputs are validated and transformed into a stable internal query shape.
3. The app structure separates UI orchestration from future fetch/ranking logic.

### Phase 2: Places Retrieval Pipeline

**Goal:** Retrieve live Google Places data with pagination support and normalize it into a clean internal dataset.

**Requirements:** RETR-01, RETR-02

**UI hint**: no

**Success criteria:**
1. Searches fetch beyond the first API page when more results are available.
2. Normalized results remove duplicate places deterministically.
3. Retrieval logic is testable without the Streamlit UI layer.

### Phase 3: Ranking Engine

**Goal:** Implement Bayesian scoring so ranked results prefer strong ratings with meaningful review volume.

**Requirements:** RANK-01, RANK-02

**UI hint**: no

**Success criteria:**
1. Bayesian score calculation is isolated in its own module with tests around low-review edge cases.
2. Ranked output orders places by the computed score consistently.
3. Ranking metadata needed for user trust, including rating and review count, is preserved for presentation.

### Phase 4: Results Experience

**Goal:** Deliver the visible value of the app through clear results presentation, status handling, and efficient repeated searches.

**Requirements:** VIEW-01, VIEW-02, VIEW-03, PLAT-01

**UI hint**: yes

**Success criteria:**
1. Ranked results appear in a clear table/dataframe with the expected ordering and fields.
2. Ranked places can be inspected on a map view.
3. Loading, no-results, and API/configuration failure states are handled clearly.
4. Repeating an identical search reuses cached data within the session.

### Phase 5: Deployment Hardening

**Goal:** Make the application safe and ready for public Streamlit Cloud deployment.

**Requirements:** PLAT-02

**UI hint**: no

**Success criteria:**
1. Secrets are loaded from Streamlit secrets or environment variables without hardcoding.
2. The dependency list and repo hygiene support clean deployment.
3. Deployment instructions or configuration assumptions are explicit enough to publish the app without restructuring.

## Coverage Check

- All v1 requirements map to exactly one phase.
- Dependencies flow from search inputs -> retrieval -> ranking -> presentation -> deployment.
- No phase introduces deferred v2 scope.

## Next Step

Run `$gsd-discuss-phase 5` to clarify deployment and Streamlit Cloud hardening details.

---
*Last updated: 2026-03-28 after Phase 4 completion*
