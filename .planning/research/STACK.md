# Stack Research

## Recommended Core Stack

- **UI/runtime**: Streamlit
- **Language/runtime**: Python 3.11+
- **HTTP client**: `requests` for v1
- **Data shaping**: `pandas`
- **Ranking/math**: standard library + small pure-Python scoring helpers
- **Secrets/config**: `st.secrets` for Streamlit Cloud, environment variables for local use
- **Local env loading**: `python-dotenv`
- **Testing**: `pytest`
- **Lint/format**: `ruff`

## Why This Fits This Project

### Streamlit

Streamlit is the right v1 choice because the product value is search, ranking, and comparison, not bespoke frontend interaction. It gives fast iteration, built-in tabular display, and a low-friction map primitive.

### Requests + pandas

The API surface is simple enough that a general HTTP client is sufficient. `pandas` is useful for shaping results into a table and sorting by score without introducing database or ORM complexity.

### Small custom scoring module

The ranking logic is the differentiator, so it should live in an isolated scoring module rather than being embedded in UI code or dataframe transformations. That keeps Bayesian scoring testable and makes later factors like price or distance additive rather than invasive.

### Secrets via `st.secrets` and env vars

This matches the deployment target directly. Streamlit Cloud prefers `st.secrets`, while local development benefits from `.env` and environment variables. Supporting both avoids branching deployment logic later.

## Recommended Project Structure

```text
app.py
src/
  clients/google_places.py
  ranking/bayesian.py
  services/search.py
  models/place.py
tests/
```

- Keep `app.py` thin and UI-focused.
- Put API calls behind a client module.
- Put ranking math in a separate module with pure functions.
- Put deduplication and result orchestration in a service layer.

## Deployment Considerations

- Pin dependencies in `requirements.txt` once the first implementation pass stabilizes.
- Keep secrets out of git and load them only from environment or Streamlit secrets.
- Prefer lightweight session/data caching over persistent infrastructure.
- Handle API quota failures and empty-result responses visibly in the UI.

## Testing And Tooling Suggestions

- Unit test Bayesian scoring separately from UI.
- Unit test deduplication and result normalization with fixture payloads.
- Add small integration tests around the search orchestration layer with mocked Google API responses.
- Use `ruff` for both linting and formatting where possible to keep tooling minimal.

## Tradeoffs

- **Streamlit** is fast to ship but less flexible if the product later needs a richer public UX.
- **`requests`** is sufficient now; switching to `httpx` only matters if async or more advanced client behavior becomes necessary.
- **No database** keeps v1 lean but means no historical comparisons, scheduled refreshes, or persistent analytics yet.

## Avoid In V1

- ORMs or persistence layers
- Background jobs or country-wide scraping
- Custom frontend frameworks
- Premature async complexity
- Overly generic ranking configuration before the core score is proven
