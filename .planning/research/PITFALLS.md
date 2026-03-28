# Pitfalls Research

## Pitfall 1: Naive Ranking Creates Misleading Results

**Risk**
Sorting directly by star rating will overvalue places with very few reviews and undermine the product's core claim.

**Warning signs**
- Top results have tiny review counts
- Users question why obvious popular places rank below sparse-review entries

**Prevention**
- Implement Bayesian scoring first, before polishing the UI
- Show review count and score beside rating so the ranking is understandable

**Phase focus**
- Address in the ranking/domain logic phase

## Pitfall 2: Google Places Pagination And Deduplication Are Incomplete

**Risk**
Only using the first page or failing to merge duplicates produces weak and inconsistent rankings.

**Warning signs**
- Queries plateau at 20 results unexpectedly
- Duplicate businesses appear in the ranked output

**Prevention**
- Build explicit pagination handling into the Places client
- Deduplicate by stable place identifier before scoring

**Phase focus**
- Address in the API integration phase

## Pitfall 3: Streamlit Reruns Burn API Quota

**Risk**
Reactive reruns can trigger repeated live API calls, increasing cost and making the app feel unstable.

**Warning signs**
- Repeated identical searches cause noticeable delays
- API usage rises unexpectedly during simple UI interactions

**Prevention**
- Cache search service results by normalized input tuple
- Keep API calls behind one cached function boundary

**Phase focus**
- Address in the service/integration phase

## Pitfall 4: Ranking Logic Gets Entangled With UI Code

**Risk**
If scoring lives inside dataframe transformations or Streamlit callbacks, future ranking factors become hard to add and hard to test.

**Warning signs**
- Formula edits require UI refactors
- No isolated unit tests can validate the score

**Prevention**
- Put scoring in pure functions under a dedicated ranking module
- Keep `app.py` thin and orchestration-only

**Phase focus**
- Address in the project structure phase

## Pitfall 5: Public Deployment Leaks Secrets Or Fails Config Lookup

**Risk**
Hardcoded keys or inconsistent secret-loading logic block safe deployment.

**Warning signs**
- API key appears in repo files
- Local execution works but Streamlit Cloud deployment fails

**Prevention**
- Standardize on `st.secrets` plus environment variable fallback
- Keep `.env` ignored and document the required key name once

**Phase focus**
- Address in the project scaffold/deployment phase

## Pitfall 6: Scope Expands Before Core Search Quality Is Proven

**Risk**
Adding filters, accounts, persistence, or country-wide crawling too early delays validation of the main ranking value.

**Warning signs**
- Roadmap phases are dominated by infrastructure or feature sprawl
- Ranking logic is still provisional while secondary features multiply

**Prevention**
- Keep v1 focused on city/category search, ranking, table, and map
- Treat new ranking factors and persistence as explicit later phases

**Phase focus**
- Address in requirements and roadmap scoping
