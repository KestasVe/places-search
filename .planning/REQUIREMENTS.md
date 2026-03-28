# Requirements: Lithuania Places Ranker

**Defined:** 2026-03-28
**Core Value:** Turn messy Google Maps browsing into a reliable ranked list where highly rated places with meaningful review volume beat misleading low-sample results.

## v1 Requirements

### Search

- [ ] **SRCH-01**: User can select a Lithuanian city before running a search.
- [ ] **SRCH-02**: User can enter a freeform place category or query term such as `Kebabai`, `Muzejai`, or `Kavines`.
- [ ] **SRCH-03**: User can choose a search radius in kilometers.

### Retrieval

- [ ] **RETR-01**: User can run a live Google Places search and receive results beyond the first page when additional results exist.
- [ ] **RETR-02**: User sees each place only once in the ranked results even when the API returns duplicates or overlapping entries.

### Ranking

- [ ] **RANK-01**: User sees places ranked by a Bayesian weighted score based on Google rating and review count.
- [ ] **RANK-02**: User can inspect each ranked place's rating and review count alongside its final order so the ranking is understandable.

### Results

- [ ] **VIEW-01**: User can view the ranked results in a sortable table/dataframe.
- [ ] **VIEW-02**: User can view the ranked results on a map.
- [ ] **VIEW-03**: User receives clear feedback when a search is loading, returns no results, or fails due to an API/configuration issue.

### Platform

- [ ] **PLAT-01**: Repeating the same search within a session reuses cached data to reduce unnecessary API calls and improve perceived responsiveness.
- [ ] **PLAT-02**: The application can be deployed publicly on Streamlit Cloud with the Google Places API key loaded from secrets or environment variables.

## v2 Requirements

### Ranking Enhancements

- **RANK-03**: User can rank by additional signals such as distance, price level, or open-now availability.
- **RANK-04**: User can compare alternate ranking modes such as Bayesian score, raw rating, and review count.

### Discovery

- **DISC-01**: User can generate Lithuania-wide aggregated rankings across multiple cities.
- **DISC-02**: User can export ranked results for later use.

### Exploration

- **EXPL-01**: User can open a dedicated place detail view with more context.
- **EXPL-02**: User can save favorite places across sessions.

## Out of Scope

| Feature | Reason |
|---------|--------|
| User accounts | Not required to validate the ranking workflow |
| Permanent database storage | Live queries plus session caching are enough for v1 |
| Multilingual UI | English UI is sufficient for initial release |
| Advanced filters beyond rating/review-count scoring | Deferred to keep v1 focused on trustworthy ranking |
| Background nationwide scraping/precomputed rankings | Conflicts with the live-query-first v1 approach |
| Mobile-specific custom optimization | Standard Streamlit responsiveness is enough initially |

## Traceability

| Requirement | Phase | Status |
|-------------|-------|--------|
| SRCH-01 | Phase 1 | Pending |
| SRCH-02 | Phase 1 | Pending |
| SRCH-03 | Phase 1 | Pending |
| RETR-01 | Phase 2 | Pending |
| RETR-02 | Phase 2 | Pending |
| RANK-01 | Phase 3 | Pending |
| RANK-02 | Phase 3 | Pending |
| VIEW-01 | Phase 4 | Pending |
| VIEW-02 | Phase 4 | Pending |
| VIEW-03 | Phase 4 | Pending |
| PLAT-01 | Phase 4 | Pending |
| PLAT-02 | Phase 5 | Pending |

**Coverage:**
- v1 requirements: 12 total
- Mapped to phases: 12
- Unmapped: 0

---
*Requirements defined: 2026-03-28*
*Last updated: 2026-03-28 after initial definition*
