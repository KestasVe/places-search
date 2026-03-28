from __future__ import annotations

from geocoding import GeocodingResolution
from query import build_search_query
from retrieval import MAX_PLACES_PAGES, retrieve_places


def _resolution() -> GeocodingResolution:
    return GeocodingResolution(
        formatted_address="Vilnius, Lithuania",
        lat=54.6872,
        lng=25.2797,
        warnings=[],
    )


def _raw_place(
    place_id: str,
    *,
    rating: float | None = 4.5,
    user_ratings_total: int | None = 100,
    business_status: str = "OPERATIONAL",
    price_level: int | None = 2,
    lat: float = 54.6880,
    lng: float = 25.2805,
) -> dict[str, object]:
    payload: dict[str, object] = {
        "place_id": place_id,
        "name": f"Place {place_id}",
        "formatted_address": f"{place_id} Street",
        "geometry": {"location": {"lat": lat, "lng": lng}},
        "business_status": business_status,
        "types": ["restaurant"],
        "price_level": price_level,
    }
    if rating is not None:
        payload["rating"] = rating
    if user_ratings_total is not None:
        payload["user_ratings_total"] = user_ratings_total
    return payload


def test_retrieve_places_returns_structured_error_when_geocoding_fails() -> None:
    query = build_search_query("Unknown City", "Kebabai", 10)

    def geocode_fail(city: str, api_key: str | None) -> GeocodingResolution:
        raise LookupError(f"Location not found for '{city}'.")

    result = retrieve_places(query, api_key="test-key", geocode_fn=geocode_fail)

    assert result.error is not None
    assert result.error.code == "geocoding_not_found"
    assert result.error.query_context["city_raw"] == "Unknown City"


def test_retrieve_places_stops_after_three_pages_even_if_more_tokens_exist() -> None:
    query = build_search_query("Vilnius", "Kebabai", 10)
    calls: list[str | None] = []

    def fake_search(
        category_query: str,
        user_location_name: str,
        center_lat: float,
        center_lng: float,
        radius_m: int,
        api_key: str | None,
        page_token: str | None,
    ) -> dict[str, object]:
        calls.append(page_token)
        return {
            "results": [_raw_place(f"page-{len(calls)}")],
            "next_page_token": f"token-{len(calls)}",
        }

    result = retrieve_places(query, api_key="test-key", geocode_fn=lambda *_: _resolution(), places_search_fn=fake_search)

    assert len(calls) == MAX_PLACES_PAGES
    assert len(result.places) == MAX_PLACES_PAGES


def test_retrieve_places_returns_partial_results_with_warning_on_later_page_failure() -> None:
    query = build_search_query("Vilnius", "Kebabai", 10)

    def fake_search(
        category_query: str,
        user_location_name: str,
        center_lat: float,
        center_lng: float,
        radius_m: int,
        api_key: str | None,
        page_token: str | None,
    ) -> dict[str, object]:
        if page_token is None:
            return {"results": [_raw_place("page-1")], "next_page_token": "token-1"}
        raise RuntimeError("page 2 failed")

    result = retrieve_places(query, api_key="test-key", geocode_fn=lambda *_: _resolution(), places_search_fn=fake_search)

    assert result.error is None
    assert [place.place_id for place in result.places] == ["page-1"]
    assert result.metadata is not None
    assert any("page 2 failed" in warning for warning in result.metadata.warnings)


def test_retrieve_places_returns_empty_success_result_with_metadata() -> None:
    query = build_search_query("Vilnius", "Kebabai", 10)

    def fake_search(
        category_query: str,
        user_location_name: str,
        center_lat: float,
        center_lng: float,
        radius_m: int,
        api_key: str | None,
        page_token: str | None,
    ) -> dict[str, object]:
        return {"results": []}

    result = retrieve_places(query, api_key="test-key", geocode_fn=lambda *_: _resolution(), places_search_fn=fake_search)

    assert result.error is None
    assert result.places == []
    assert result.metadata is not None
    assert result.metadata.resolved_city_address == "Vilnius, Lithuania"


def test_retrieve_places_collapses_duplicate_place_ids_across_pages() -> None:
    query = build_search_query("Vilnius", "Kebabai", 10)

    pages = [
        {
            "results": [_raw_place("dup-1", rating=None, user_ratings_total=None, price_level=None)],
            "next_page_token": "token-1",
        },
        {
            "results": [_raw_place("dup-1", rating=4.8, user_ratings_total=250, price_level=1)],
        },
    ]

    def fake_search(
        category_query: str,
        user_location_name: str,
        center_lat: float,
        center_lng: float,
        radius_m: int,
        api_key: str | None,
        page_token: str | None,
    ) -> dict[str, object]:
        if page_token is None:
            return pages[0]
        return pages[1]

    result = retrieve_places(query, api_key="test-key", geocode_fn=lambda *_: _resolution(), places_search_fn=fake_search)

    assert len(result.places) == 1
    assert result.places[0].place_id == "dup-1"
    assert result.places[0].user_ratings_total == 250
