# Architecture Research

## Major Components

### Streamlit UI

Collects city, category, and radius inputs, triggers searches, and renders results. This layer should not contain API-specific pagination logic or scoring formulas.

### Places Client

Responsible for all Google Places requests, pagination handling, request parameter construction, and response normalization. This boundary isolates external API behavior from the rest of the application.

### Search Service

Coordinates the search flow:

1. build query inputs
2. fetch all result pages
3. normalize and deduplicate places
4. compute ranking scores
5. return a result object ready for UI display

### Ranking Module

Pure functions for Bayesian weighted scoring and future ranking factors. This should accept normalized place data and return deterministic score outputs.

### Data Model

A lightweight place representation should carry the normalized fields used by the UI and ranking logic: place id, name, coordinates, rating, review count, address, query metadata.

## Data Flow

1. User submits city, category, and radius from the Streamlit UI.
2. UI calls the cached search service function.
3. Search service asks the Places client for all matching pages.
4. Places client returns normalized raw places.
5. Search service deduplicates and validates the result set.
6. Ranking module computes weighted scores.
7. Search service sorts and returns ranked places.
8. UI renders the dataframe and map from the same ranked dataset.

## Modularity For Future Ranking Factors

- Keep the score calculation separate from the search orchestration.
- Represent ranking factors as explicit inputs so price, distance, or open-now logic can be added later without rewriting the UI or API client.
- Avoid coupling dataframe column names directly to ranking internals.

## Suggested Build Order

1. Define normalized place model and ranking function.
2. Implement Google Places client with pagination and error handling.
3. Implement search service with deduplication and score computation.
4. Connect service to Streamlit UI.
5. Add caching and user-facing error states.
6. Add tests around ranking and search orchestration.

## Architectural Cautions

- Do not let Streamlit reruns trigger repeated uncached API traffic.
- Do not bury deduplication or score logic inside UI callbacks.
- Do not design around a database before live-query behavior is validated.
