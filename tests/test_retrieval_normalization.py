from retrieval_models import RetrievalError, RetrievalMetadata, RetrievalResult
from retrieval_normalization import (
    deduplicate_places,
    filter_operational_places,
    normalize_place_payload,
)


def test_normalize_place_payload_maps_required_fields() -> None:
    place = normalize_place_payload(
        {
            "place_id": "abc123",
            "name": "Best Kebab",
            "formatted_address": "Vilnius Street 1",
            "geometry": {"location": {"lat": 54.6872, "lng": 25.2797}},
            "rating": 4.8,
            "user_ratings_total": 512,
            "types": ["restaurant", "food"],
            "business_status": "OPERATIONAL",
            "price_level": 2,
            "opening_hours": {"open_now": True},
        }
    )

    assert place.place_id == "abc123"
    assert place.formatted_address == "Vilnius Street 1"
    assert place.lat == 54.6872
    assert place.lng == 25.2797
    assert place.rating == 4.8
    assert place.user_ratings_total == 512


def test_deduplicate_places_keeps_most_complete_duplicate() -> None:
    less_complete = normalize_place_payload(
        {
            "place_id": "dup-1",
            "name": "Duplicate Place",
            "formatted_address": "Old Address",
            "geometry": {"location": {"lat": 54.0, "lng": 25.0}},
        }
    )
    more_complete = normalize_place_payload(
        {
            "place_id": "dup-1",
            "name": "Duplicate Place",
            "formatted_address": "New Address",
            "geometry": {"location": {"lat": 54.0, "lng": 25.0}},
            "rating": 4.5,
            "user_ratings_total": 200,
            "price_level": 1,
            "business_status": "OPERATIONAL",
        }
    )

    deduped = deduplicate_places([less_complete, more_complete])

    assert len(deduped) == 1
    assert deduped[0].formatted_address == "New Address"
    assert deduped[0].user_ratings_total == 200


def test_filter_operational_places_removes_non_operational_entries() -> None:
    open_place = normalize_place_payload(
        {
            "place_id": "open-1",
            "name": "Open Place",
            "formatted_address": "Open Street",
            "geometry": {"location": {"lat": 54.1, "lng": 25.1}},
            "business_status": "OPERATIONAL",
        }
    )
    closed_place = normalize_place_payload(
        {
            "place_id": "closed-1",
            "name": "Closed Place",
            "formatted_address": "Closed Street",
            "geometry": {"location": {"lat": 54.2, "lng": 25.2}},
            "business_status": "CLOSED_TEMPORARILY",
        }
    )

    filtered = filter_operational_places([open_place, closed_place])

    assert [place.place_id for place in filtered] == ["open-1"]


def test_normalize_place_payload_keeps_missing_rating_fields() -> None:
    place = normalize_place_payload(
        {
            "place_id": "no-rating",
            "name": "No Ratings Yet",
            "formatted_address": "Quiet Street",
            "geometry": {"location": {"lat": 54.3, "lng": 25.3}},
            "business_status": "OPERATIONAL",
        }
    )

    assert place.rating is None
    assert place.user_ratings_total is None


def test_retrieval_models_can_be_instantiated_with_agreed_fields() -> None:
    metadata = RetrievalMetadata(
        resolved_city_address="Vilnius, Lithuania",
        center_lat=54.6872,
        center_lng=25.2797,
        requested_radius_km=10,
        requested_radius_m=10000,
        warnings=["Picked first geocoding result."],
    )
    error = RetrievalError(
        code="geocoding_not_found",
        message="Location not found.",
        query_context={"city": "Unknown"},
    )
    result = RetrievalResult(places=[], metadata=metadata, error=error)

    assert result.metadata is metadata
    assert result.error is error
    assert result.places == []
