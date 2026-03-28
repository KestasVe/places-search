from query import build_search_query, normalize_text_input, validate_search_inputs


def test_normalize_text_input() -> None:
    assert normalize_text_input("  Vilnius   City  ") == "vilnius city"


def test_build_search_query() -> None:
    query = build_search_query("Vilnius", "Kebabai", 10)

    assert query.city_raw == "Vilnius"
    assert query.city_normalized == "vilnius"
    assert query.category_raw == "Kebabai"
    assert query.category_normalized == "kebabai"
    assert query.radius_km == 10
    assert query.radius_m == 10000


def test_validate_search_inputs_requires_city() -> None:
    assert validate_search_inputs("", "Kebabai") == {
        "city": "Enter a city before searching."
    }


def test_validate_search_inputs_requires_category() -> None:
    assert validate_search_inputs("Vilnius", "") == {
        "category": "Enter a category before searching."
    }


def test_validate_search_inputs_allows_normalized_values() -> None:
    assert validate_search_inputs("  Vilnius  ", "  Kebabai  ") == {}
