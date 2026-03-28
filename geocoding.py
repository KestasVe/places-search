from __future__ import annotations

import os
from dataclasses import dataclass, field
from typing import Any


GEOCODING_API_URL = "https://maps.googleapis.com/maps/api/geocode/json"


@dataclass(frozen=True)
class GeocodingResolution:
    formatted_address: str
    lat: float
    lng: float
    warnings: list[str] = field(default_factory=list)


def get_google_api_key(explicit_api_key: str | None = None) -> str:
    api_key = explicit_api_key or os.getenv("GOOGLE_PLACES_API_KEY", "")
    return api_key.strip()


def geocode_city(
    city_query: str,
    api_key: str | None = None,
    session: Any = None,
    timeout: int = 15,
) -> GeocodingResolution:
    import requests

    resolved_api_key = get_google_api_key(api_key)
    if not resolved_api_key:
        raise ValueError("Missing Google Places API key.")

    http = session or requests.Session()
    response = http.get(
        GEOCODING_API_URL,
        params={"address": city_query, "key": resolved_api_key},
        timeout=timeout,
    )
    response.raise_for_status()

    payload = response.json()
    results = payload.get("results") or []
    if not results:
        raise LookupError(f"Location not found for '{city_query}'.")

    selected_result = results[0]
    location = selected_result.get("geometry", {}).get("location", {})

    warnings: list[str] = []
    if len(results) > 1:
        warnings.append("Multiple geocoding results returned; selected the first result.")

    return GeocodingResolution(
        formatted_address=str(selected_result.get("formatted_address") or city_query),
        lat=float(location["lat"]),
        lng=float(location["lng"]),
        warnings=warnings,
    )
