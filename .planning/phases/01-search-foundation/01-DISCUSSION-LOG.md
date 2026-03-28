# Phase 1: Search Foundation - Discussion Log

> **Audit trail only.** Do not use as input to planning, research, or execution agents.
> Decisions are captured in CONTEXT.md - this log preserves the alternatives considered.

**Date:** 2026-03-28
**Phase:** 1-search-foundation
**Areas discussed:** Supported cities, Category input, Radius UX, Search trigger and validation

---

## Supported cities

| Option | Description | Selected |
|--------|-------------|----------|
| Predefined top cities | Restrict city choice to a short curated list such as the largest Lithuanian cities | |
| Broader curated list | Offer a larger maintained list of Lithuanian cities | |
| Free-text city input | Let the user type any city name and normalize it later in the pipeline | x |

**User's choice:** Any city can be entered by the user as free text.
**Notes:** The UI should indicate that both Lithuanian and English city names are acceptable. City is required before search. Phase 1 should define the stable city query fields now, but actual geocoding/location resolution belongs in Phase 2.

---

## Category input

| Option | Description | Selected |
|--------|-------------|----------|
| Free-text with placeholder | Plain input field with concrete examples in the placeholder | x |
| Free-text with visible suggestions | Plain input plus suggestion chips or example list | |
| Loose/optional field | Allow empty or partially structured category input for future broader search behavior | |

**User's choice:** Free-text only, with a placeholder and no visible suggestions.
**Notes:** Category is required. Light normalization should trim edges, collapse repeated spaces, preserve original display casing, and store a normalized lowercase value for internal logic.

---

## Radius UX

| Option | Description | Selected |
|--------|-------------|----------|
| Slider | Intuitive interactive control for choosing search radius | x |
| Number input | Precise manual numeric entry | |
| Fixed dropdown | Select from a small set of preset distances | |

**User's choice:** Slider control.
**Notes:** Radius defaults to 10 km and allows 1-50 km. Internal storage should keep both kilometers and meters, with meters aligned to the Google Places API contract.

---

## Search trigger and validation

| Option | Description | Selected |
|--------|-------------|----------|
| Explicit button trigger | Search runs only after pressing `Search` | x |
| Auto-run on change | Search reruns whenever an input changes | |
| Extra request metadata | Include timestamp/request id in the normalized query object | |

**User's choice:** Explicit button trigger with a minimal normalized query object.
**Notes:** Validation should be inline and the search button should stay disabled until city and category are present. The normalized query object should contain only `city_raw`, `city_normalized`, `category_raw`, `category_normalized`, `radius_km`, and `radius_m`.

---

## the agent's Discretion

- Exact visual placement of the search form controls
- Final helper/error copy wording

## Deferred Ideas

None
