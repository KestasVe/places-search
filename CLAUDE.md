<!-- GSD:project-start source:PROJECT.md -->
## Project

**Lithuania Places Ranker**

Lithuania Places Ranker is a Python-based Streamlit web application that finds and ranks the best places in Lithuania using the Google Places API. It is designed for both local residents and tourists who want a faster way to compare places like kebab shops, museums, or cafes by combining rating quality and popularity into a more trustworthy ranking. In v1, the main experience is city-first search with a ranked results table and a map view.

**Core Value:** Turn messy Google Maps browsing into a reliable ranked list where highly rated places with meaningful review volume beat misleading low-sample results.

### Constraints

- **Tech stack**: Python + Streamlit - chosen for fast iteration, simple deployment, and built-in table/map UI primitives.
- **API dependency**: Google Places API - ranking depends on live external search data.
- **Secrets handling**: No hardcoded API key - required for safe public deployment and repository hygiene.
- **Data model**: No permanent database in v1 - keeps the first release lean and avoids unnecessary persistence complexity.
- **Caching**: Session/local caching only - reduces repeated API spend without adding database infrastructure.
- **Ranking scope**: Rating + review count only in v1 - keeps the scoring logic focused and explainable.
- **Deployment**: Streamlit Cloud compatibility - project structure should support straightforward hosted deployment.
<!-- GSD:project-end -->

<!-- GSD:stack-start source:research/STACK.md -->
## Technology Stack

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
### Requests + pandas
### Small custom scoring module
### Secrets via `st.secrets` and env vars
## Recommended Project Structure
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
<!-- GSD:stack-end -->

<!-- GSD:conventions-start source:CONVENTIONS.md -->
## Conventions

Conventions not yet established. Will populate as patterns emerge during development.
<!-- GSD:conventions-end -->

<!-- GSD:architecture-start source:ARCHITECTURE.md -->
## Architecture

Architecture not yet mapped. Follow existing patterns found in the codebase.
<!-- GSD:architecture-end -->

<!-- GSD:workflow-start source:GSD defaults -->
## GSD Workflow Enforcement

Before using Edit, Write, or other file-changing tools, start work through a GSD command so planning artifacts and execution context stay in sync.

Use these entry points:
- `/gsd:quick` for small fixes, doc updates, and ad-hoc tasks
- `/gsd:debug` for investigation and bug fixing
- `/gsd:execute-phase` for planned phase work

Do not make direct repo edits outside a GSD workflow unless the user explicitly asks to bypass it.
<!-- GSD:workflow-end -->



<!-- GSD:profile-start -->
## Developer Profile

> Profile not yet configured. Run `/gsd:profile-user` to generate your developer profile.
> This section is managed by `generate-claude-profile` -- do not edit manually.
<!-- GSD:profile-end -->
