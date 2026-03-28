# Stack Research

## Recommended Core Stack

- **Frontend/App shell**: Streamlit
- **Language/runtime**: Python 3.11+
- **HTTP client**: `requests`
- **Tabular processing**: `pandas`
- **Config/secrets**: `st.secrets` in deployed environments, environment variables for local development
- **Local env helper**: `python-dotenv`
- **Testing**: `pytest`
- **Linting/formatting**: `ruff`

## Why This Fits

### Streamlit

- Fastest path to a usable public-facing app for search, ranking, table display, and map display.
- Streamlit Cloud is a direct deployment target, reducing infrastructure overhead for v1.
- Built-in caching (`st.cache_data`) matches the requirement for live-on-demand queries with session-friendly reuse.

### requests + pandas

- `requests` is sufficient for Google Places API calls in v1 without introducing async or client complexity too early.
- `pandas` is a good fit for deduplication, score calculation, ranking, and dataframe display.

### st.secrets + environment variables

- Keeps the Google API key out of source control.
- Works cleanly across local development and Streamlit Cloud deployment.

## Suggested Project Structure

- `app.py` - Streamlit entry point
- `src/places_client.py` - Google Places API fetching and pagination
- `src/ranking.py` - Bayesian scoring and sorting logic
- `src/transform.py` - normalization and deduplication helpers
- `src/ui.py` or `src/view_models.py` - presentation helpers for table/map shaping
- `tests/` - unit tests for ranking and data transformation

## Deployment Notes

- Keep dependencies minimal to avoid slow Streamlit Cloud cold starts.
- Expect Google API quotas and billing to matter earlier than app hosting cost.
- Prefer small, deterministic caching keys based on city/category/radius inputs.

## Testing and Tooling Guidance

- Unit-test Bayesian score behavior, especially low-review edge cases.
- Unit-test pagination and duplicate handling with mocked API responses.
- Add lightweight smoke coverage for the app entry point once the core modules exist.

## Avoid In V1

- Premature database integration
- Async/concurrent fetch complexity unless API limits force it
- Heavy geospatial packages when simple latitude/longitude handling is enough
- Over-engineered deployment layers beyond Streamlit Cloud
