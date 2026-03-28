---
phase: 04
slug: results-experience
status: approved
created: 2026-03-28
---

# Phase 04 - UI Design Contract

## Layout Contract

- Keep the existing single-page Streamlit shell and search form at the top.
- After a successful search, present a split view with the ranked tables on the left and the map on the right.
- Place summary metrics above the split view so users can understand result volume quickly.
- Keep raw retrieval and ranking payloads collapsed under an expander rather than exposing JSON inline by default.

## Results Table Contract

- Default table shows only ranked results.
- Cap the visible ranked table at 20 rows.
- Use these columns in this order:
  - `Rank`
  - `Name`
  - `Score`
  - `Rating`
  - `Reviews`
  - `Address`
  - `Price`
  - `Open Now`
- Values must be display-formatted:
  - score to 2 decimals
  - rating to 1 decimal
  - missing scalar values shown as `-`
  - price shown as `$`, `$$`, `$$$`, etc.
  - open status shown as `Open`, `Closed`, or `Unknown`

## Map Contract

- Plot ranked places only.
- Limit plotted markers to the same Top 20 ranked set shown in the main table.
- Use the resolved search center when available for initial map centering.
- Marker popups must expose rank, name, score, rating and review count, and address.

## State Contract

- Missing API key is a blocking error and prevents search execution.
- Search execution shows a loading spinner while the pipeline runs.
- Retrieval warnings are visible but non-blocking.
- Zero-results and zero-rankable-results states must be explicit and readable.
- Unranked places remain accessible through an expander, not mixed into the top-ranked table.

## Visual Tone

- Preserve the warm neutral shell established earlier.
- Keep the results view tool-like and dense enough to be useful, without dashboard clutter.
- The map should support inspection, not dominate the page.
