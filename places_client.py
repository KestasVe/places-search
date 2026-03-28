from __future__ import annotations

from typing import Any

from geocoding import get_google_api_key


PLACES_TEXT_SEARCH_API_URL = "https://maps.googleapis.com/maps/api/place/textsearch/json"


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

    params: dict[str, Any] = {
        "query": category_query,
        "location": f"{center_lat},{center_lng}",
        "radius": radius_m,
        "key": resolved_api_key,
    }
    if page_token:
        params["pagetoken"] = page_token

    http = session or requests.Session()
    response = http.get(PLACES_TEXT_SEARCH_API_URL, params=params, timeout=timeout)
    response.raise_for_status()
    return response.json()
