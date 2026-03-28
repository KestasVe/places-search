from pathlib import Path

from query import build_search_query, can_submit_search


def test_can_submit_search_requires_city_and_category() -> None:
    assert can_submit_search("", "Kebabai") is False
    assert can_submit_search("Vilnius", "") is False


def test_valid_submit_path_builds_six_field_query() -> None:
    query = build_search_query("Vilnius", "Kebabai", 10)

    assert set(query.__dict__.keys()) == {
        "city_raw",
        "city_normalized",
        "category_raw",
        "category_normalized",
        "radius_km",
        "radius_m",
    }
    assert query.radius_m == 10000


def test_search_cta_label_is_locked() -> None:
    app_source = Path("app.py").read_text(encoding="utf-8")

    assert 'SEARCH_CTA_LABEL = "Search places"' in app_source
