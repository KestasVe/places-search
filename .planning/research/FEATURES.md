# Features Research

## V1 Table-Stakes

### Search Inputs

- Select a Lithuanian city
- Enter a freeform category/query term
- Set search radius
- Submit and rerun searches clearly

### Results Quality

- Fetch more than the first page of Google Places results
- Normalize and deduplicate returned places
- Rank results with a transparent Bayesian weighted score
- Show rating and review count alongside rank so users can trust the outcome

### Results Presentation

- Ranked table/dataframe of results
- Map view of the ranked set
- Clear handling for no-results and partial-results cases

### Operational Basics

- Secrets-based API configuration
- Session caching for repeated identical searches
- Public-deployment-friendly packaging and repo hygiene

## Strong V1 Additions If Cheap

- Short explanation of how the score works
- User-selectable sort toggle between Bayesian score, raw rating, and review count
- Basic loading/error states around API calls

## Good V2 Candidates

- Additional ranking factors such as distance, price level, or open-now
- City aggregation across multiple Lithuanian locations
- Saved result snapshots or export
- Place detail drill-down
- Favorites/bookmarks

## Explicitly Deferred

- User accounts
- Permanent database storage
- Multilingual UI
- Background nationwide scraping/precomputation
- Mobile-specific custom UX

## Scope Guidance

- The differentiator is ranking quality, not breadth of platform features.
- V1 should optimize for "search -> fetch -> rank -> inspect on map" with as little extra product surface area as possible.
- If a feature does not improve ranking trust, search completion, or public deployment readiness, it likely belongs after v1.
