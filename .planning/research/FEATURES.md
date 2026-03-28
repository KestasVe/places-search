# Feature Research

## Table Stakes For V1

### Search Inputs

- Select a Lithuanian city
- Enter a freeform category or place type query
- Set a search radius

### Search Execution

- Call Google Places with live data
- Handle pagination when a query spans multiple pages
- Normalize and deduplicate repeated places
- Show empty and error states clearly

### Ranking Output

- Calculate Bayesian weighted score from rating and review count
- Sort places by weighted score
- Show enough columns for trust: name, rating, reviews, score, address
- Limit the default display to a top-ranked slice while keeping full result visibility possible

### Visualization

- Render a ranked table
- Render matching places on a map
- Keep the table and map tied to the same result set

### Cost And Reliability

- Cache identical searches during a session
- Avoid duplicate API calls caused by Streamlit reruns

## Good V1 Additions If Cheap

- Score explanation text so users understand why 4.8/500 beats 5.0/2
- Simple loading/progress state for multi-page fetches
- Sort toggle between weighted score, raw rating, and review count for comparison

## Defer To V2

- Saved searches or favorites
- Place detail pages
- Persistent storage
- Precomputed Lithuania-wide rankings
- User accounts
- Multilingual UI
- Advanced filters such as price, open now, distance weighting, or business status ranking

## Feature Boundaries That Protect The Core Value

- Keep the product centered on ranking quality, not discovery social features.
- Avoid adding filters that undermine the claim that the score is the main differentiator.
- Prefer explainability over configurability in early versions.
