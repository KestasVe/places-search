# Architecture Research

## Major Components

### UI Layer

- Collects city, category, and radius inputs
- Triggers searches
- Displays ranked table, map, and user-facing errors/status

### Query Builder

- Converts UI inputs into Google Places request parameters
- Normalizes search terms and location/radius handling

### Places Client

- Calls Google Places API
- Handles pagination, retries, and response normalization

### Transform Layer

- Flattens API responses into tabular records
- Deduplicates places
- Filters incomplete or unusable records

### Ranking Engine

- Computes Bayesian weighted score from rating and review count
- Produces a final ordered result set
- Keeps scoring logic isolated so future factors can be added without rewriting fetch logic

### Cache Layer

- Reuses identical query results for a limited duration/session scope
- Sits between UI triggers and outbound API calls

## Data Flow

1. User selects city, category, and radius in Streamlit.
2. UI sends normalized search inputs to the query/fetch layer.
3. Cache checks whether an identical search result already exists.
4. If cache misses, Places client fetches paginated Google results.
5. Transform layer normalizes and deduplicates place records.
6. Ranking engine computes Bayesian scores and sorts results.
7. UI renders the ranked dataframe and map.

## Build Order Implications

1. Define the normalized internal place record shape.
2. Implement the Places client and pagination behavior.
3. Implement transform/deduplication helpers.
4. Implement and test Bayesian ranking logic.
5. Wire caching around the fetch path.
6. Build Streamlit UI on top of stable data contracts.
7. Add error handling and polish last.

## Modularity Guidance

- Keep API fetching separate from scoring so ranking changes do not touch transport code.
- Keep transform/deduplication separate from UI so the logic is testable.
- Treat the score formula as its own module with explicit inputs and outputs.
- Avoid embedding business logic directly in `app.py`; keep it as orchestration only.
