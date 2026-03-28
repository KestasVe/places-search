from __future__ import annotations

from typing import Any

from geocoding import get_google_api_key


PLACES_TEXT_SEARCH_API_URL = "https://places.googleapis.com/v1/places:searchText"
TEXT_SEARCH_FIELD_MASK = ",".join(
    [
        "places.id",
        "places.displayName",
        "places.formattedAddress",
        "places.location",
        "places.rating",
        "places.userRatingCount",
        "places.types",
        "places.businessStatus",
        "places.priceLevel",
        "places.currentOpeningHours.openNow",
        "nextPageToken",
    ]
)
PRICE_LEVEL_MAP = {
    "PRICE_LEVEL_FREE": 0,
    "PRICE_LEVEL_INEXPENSIVE": 1,
    "PRICE_LEVEL_MODERATE": 2,
    "PRICE_LEVEL_EXPENSIVE": 3,
    "PRICE_LEVEL_VERY_EXPENSIVE": 4,
}


def _normalize_price_level(value: Any) -> int | None:
    if value is None:
        return None
    if isinstance(value, int):
        return value
    return PRICE_LEVEL_MAP.get(str(value))


def _normalize_text_search_place(place: dict[str, Any]) -> dict[str, Any]:
    location = place.get("location") or {}
    display_name = place.get("displayName") or {}
    current_opening_hours = place.get("currentOpeningHours") or {}

    normalized_place: dict[str, Any] = {
        "place_id": place.get("id"),
        "name": display_name.get("text"),
        "formatted_address": place.get("formattedAddress"),
        "geometry": {
            "location": {
                "lat": location.get("latitude"),
                "lng": location.get("longitude"),
            }
        },
        "rating": place.get("rating"),
        "user_ratings_total": place.get("userRatingCount"),
        "types": place.get("types") or [],
        "business_status": place.get("businessStatus"),
        "price_level": _normalize_price_level(place.get("priceLevel")),
        "opening_hours": {"open_now": current_opening_hours.get("openNow")},
    }

    return normalized_place


def search_text_places(
    category_query: str,
    center_lat: float,
    center_lng: float,
    radius_m: int,
    api_key: str | None = None,
    page_token: str | None = None,
    session: Any = None,
    timeout: int = 15,
) -> dict[str, Any]:
    import requests

    resolved_api_key = get_google_api_key(api_key)
    if not resolved_api_key:
        raise ValueError("Missing Google Places API key.")

    headers = {
        "Content-Type": "application/json",
        "X-Goog-Api-Key": resolved_api_key,
        "X-Goog-FieldMask": TEXT_SEARCH_FIELD_MASK,
    }
    payload: dict[str, Any] = {
        "textQuery": category_query,
        "locationBias": {
            "circle": {
                "center": {
                    "latitude": center_lat,
                    "longitude": center_lng,
                },
                "radius": float(radius_m),
            }
        },
    }
    if page_token:
        payload["pageToken"] = page_token

    http = session or requests.Session()
    response = http.post(PLACES_TEXT_SEARCH_API_URL, json=payload, headers=headers, timeout=timeout)
    response.raise_for_status()
    response_payload = response.json()

    error = response_payload.get("error")
    if error:
        error_status = str(error.get("status") or "UNKNOWN")
        error_message = str(error.get("message") or "").strip()
        detail = f" {error_message}" if error_message else ""
        raise RuntimeError(f"Google Places request failed with status '{error_status}'.{detail}")

    places = response_payload.get("places") or []
    normalized_results = [_normalize_text_search_place(place) for place in places]

    return {
        "results": normalized_results,
        "next_page_token": response_payload.get("nextPageToken"),
    }
