---
phase: 01
slug: search-foundation
status: draft
nyquist_compliant: false
wave_0_complete: false
created: 2026-03-28
---

# Phase 01 - Validation Strategy

> Per-phase validation contract for feedback sampling during execution.

---

## Test Infrastructure

| Property | Value |
|----------|-------|
| **Framework** | pytest |
| **Config file** | none - Wave 0 installs and configures it if needed |
| **Quick run command** | `pytest tests/test_query.py -q` |
| **Full suite command** | `pytest -q` |
| **Estimated runtime** | ~10 seconds |

---

## Sampling Rate

- **After every task commit:** Run `pytest tests/test_query.py -q`
- **After every plan wave:** Run `pytest -q`
- **Before `$gsd-verify-work`:** Full suite must be green
- **Max feedback latency:** 15 seconds

---

## Per-Task Verification Map

| Task ID | Plan | Wave | Requirement | Test Type | Automated Command | File Exists | Status |
|---------|------|------|-------------|-----------|-------------------|-------------|--------|
| 01-01-01 | 01 | 0 | SRCH-01 | unit | `pytest tests/test_query.py -q` | ❌ W0 | ⬜ pending |
| 01-01-02 | 01 | 0 | SRCH-02 | unit | `pytest tests/test_query.py -q` | ❌ W0 | ⬜ pending |
| 01-02-01 | 02 | 1 | SRCH-03 | unit | `pytest tests/test_query.py -q` | ❌ W0 | ⬜ pending |
| 01-02-02 | 02 | 1 | SRCH-01, SRCH-02, SRCH-03 | integration | `pytest -q` | ❌ W0 | ⬜ pending |

*Status: ⬜ pending · ✅ green · ❌ red · ⚠️ flaky*

---

## Wave 0 Requirements

- [ ] `tests/test_query.py` - normalization and query-shape coverage for city/category/radius
- [ ] `pytest` added to the development workflow if not already available
- [ ] minimal test package structure created if `tests/` does not exist

---

## Manual-Only Verifications

| Behavior | Requirement | Why Manual | Test Instructions |
|----------|-------------|------------|-------------------|
| Search button disabled until city and category are present | SRCH-01, SRCH-02 | Streamlit widget enabled/disabled behavior is easiest to confirm interactively in this small app | Run `streamlit run app.py`, verify empty fields keep search disabled, then fill both fields and confirm it enables |
| Inline validation copy appears near the relevant fields | SRCH-01, SRCH-02 | UI placement/copy is better checked by human inspection than unit tests at this phase | Run the app, attempt invalid submission or inspect empty form state, confirm field-level guidance is visible |

---

## Validation Sign-Off

- [ ] All tasks have `<automated>` verify or Wave 0 dependencies
- [ ] Sampling continuity: no 3 consecutive tasks without automated verify
- [ ] Wave 0 covers all MISSING references
- [ ] No watch-mode flags
- [ ] Feedback latency < 15s
- [ ] `nyquist_compliant: true` set in frontmatter

**Approval:** pending
