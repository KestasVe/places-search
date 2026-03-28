from geocoding import GeocodingResolution
from query import build_search_query
from retrieval import retrieve_places


def _resolution() -> GeocodingResolution:
    return GeocodingResolution(
        formatted_address="Kalnenai, Vilnius",
        lat=54.6650,
        lng=25.3400,
        warnings=[],
    )


def _raw_place(place_id: str, lat: float, lng: float) -> dict[str, object]:
    return {
        "place_id": place_id,
        "name": f"Place {place_id}",
        "formatted_address": f"{place_id} Street",
        "geometry": {"location": {"lat": lat, "lng": lng}},
        "business_status": "OPERATIONAL",
        "rating": 4.5,
        "user_ratings_total": 100,
    }


def test_retrieve_places_filters_out_results_beyond_requested_radius() -> None:
    query = build_search_query("Kalnenai", "Pica", 3)

    def fake_search(
        category_query: str,
        user_location_name: str,
        center_lat: float,
        center_lng: float,
        radius_m: int,
        api_key: str | None,
        page_token: str | None,
    ) -> dict[str, object]:
        return {
            "results": [
                _raw_place("inside", 54.6660, 25.3420),
                _raw_place("outside", 54.7140, 25.2390),
            ]
        }

    result = retrieve_places(query, api_key="test-key", geocode_fn=lambda *_: _resolution(), places_search_fn=fake_search)

    assert [place.place_id for place in result.places] == ["inside"]
    assert result.places[0].distance_m is not None
    assert result.places[0].distance_m <= 3000
