# Pitfalls Research

## Google Places Pagination Assumptions

### Warning Signs

- Searches return suspiciously few places
- Results stop at the first page

### Prevention

- Implement explicit pagination handling and test with mocked multi-page responses
- Log page counts and total fetched records during development

### Phase To Address

- Phase 1 or earliest backend/data phase

## Weak Ranking Trust

### Warning Signs

- Places with one or two reviews frequently rank at the top
- Users cannot tell why one place outranked another

### Prevention

- Isolate and test the Bayesian score formula
- Display rating and review count next to the computed rank
- Optionally include a short score explanation in the UI

### Phase To Address

- Ranking logic phase

## Duplicate or Messy Results

### Warning Signs

- Same place appears multiple times in the top results
- Map and table counts do not match user expectations

### Prevention

- Define a deterministic deduplication strategy early
- Use stable identifiers when available and fallback rules when not
- Add fixture-based tests for duplicate scenarios

### Phase To Address

- Data normalization phase

## API Cost Surprises

### Warning Signs

- Re-running the same search repeatedly causes avoidable API usage
- Development becomes expensive or rate-limited quickly

### Prevention

- Use `st.cache_data` around the fetch path
- Keep search input keys stable and explicit
- Avoid background refreshes in v1

### Phase To Address

- Fetch/caching phase

## UI-Coupled Business Logic

### Warning Signs

- Ranking rules and fetch logic become embedded inside `app.py`
- Small logic changes require editing the UI layer directly

### Prevention

- Move API, transform, and ranking logic into separate modules
- Treat `app.py` as an orchestration layer only

### Phase To Address

- Initial project structure phase

## Secrets Leakage

### Warning Signs

- API key appears in source files, commits, or logs
- Local setup depends on hardcoded credentials

### Prevention

- Use `st.secrets` and environment variables only
- Keep `.env` ignored
- Avoid printing secrets in debugging output

### Phase To Address

- Setup/deployment phase
