from __future__ import annotations

import math
from dataclasses import replace
from typing import Any, Iterable

from retrieval_models import NormalizedPlace

EARTH_RADIUS_M = 6_371_000


def _coerce_float(value: Any) -> float | None:
    if value is None:
        return None
    try:
        return float(value)
    except (TypeError, ValueError):
        return None


def _coerce_int(value: Any) -> int | None:
    if value is None:
        return None
    try:
        return int(value)
    except (TypeError, ValueError):
        return None


def _extract_open_now(raw_place: dict[str, Any]) -> bool | None:
    opening_hours = raw_place.get("opening_hours")
    if isinstance(opening_hours, dict):
        open_now = opening_hours.get("open_now")
        if isinstance(open_now, bool):
            return open_now
    return None


def normalize_place_payload(raw_place: dict[str, Any]) -> NormalizedPlace:
    geometry = raw_place.get("geometry") or {}
    location = geometry.get("location") or {}

    types = raw_place.get("types")
    if not isinstance(types, list):
        types = []

    return NormalizedPlace(
        place_id=str(raw_place.get("place_id") or ""),
        name=str(raw_place.get("name") or ""),
        formatted_address=str(raw_place.get("formatted_address") or raw_place.get("vicinity") or ""),
        lat=_coerce_float(location.get("lat")),
        lng=_coerce_float(location.get("lng")),
        distance_m=None,
        rating=_coerce_float(raw_place.get("rating")),
        user_ratings_total=_coerce_int(raw_place.get("user_ratings_total")),
        types=[str(item) for item in types if item is not None],
        business_status=(
            str(raw_place.get("business_status"))
            if raw_place.get("business_status") is not None
            else None
        ),
        price_level=_coerce_int(raw_place.get("price_level")),
        opening_hours=_extract_open_now(raw_place),
    )


def completeness_score(place: NormalizedPlace) -> int:
    required_values = [
        place.place_id,
        place.name,
        place.formatted_address,
        place.lat,
        place.lng,
        place.rating,
        place.user_ratings_total,
    ]
    optional_values = [
        place.types if place.types else None,
        place.business_status,
        place.price_level,
        place.opening_hours,
    ]
    return sum(value not in (None, "", []) for value in required_values + optional_values)


def is_operational(place: NormalizedPlace) -> bool:
    return place.business_status in (None, "OPERATIONAL")


def filter_operational_places(places: Iterable[NormalizedPlace]) -> list[NormalizedPlace]:
    return [place for place in places if is_operational(place)]


def calculate_haversine_distance_m(
    origin_lat: float,
    origin_lng: float,
    destination_lat: float,
    destination_lng: float,
) -> float:
    origin_lat_rad = math.radians(origin_lat)
    destination_lat_rad = math.radians(destination_lat)
    delta_lat_rad = math.radians(destination_lat - origin_lat)
    delta_lng_rad = math.radians(destination_lng - origin_lng)

    haversine_term = (
        math.sin(delta_lat_rad / 2) ** 2
        + math.cos(origin_lat_rad) * math.cos(destination_lat_rad) * math.sin(delta_lng_rad / 2) ** 2
    )
    central_angle = 2 * math.atan2(math.sqrt(haversine_term), math.sqrt(1 - haversine_term))
    return EARTH_RADIUS_M * central_angle


def filter_places_within_radius(
    places: Iterable[NormalizedPlace],
    center_lat: float,
    center_lng: float,
    radius_m: int,
) -> list[NormalizedPlace]:
    filtered_places: list[NormalizedPlace] = []

    for place in places:
        if place.lat is None or place.lng is None:
            continue

        distance_m = calculate_haversine_distance_m(center_lat, center_lng, place.lat, place.lng)
        if distance_m <= radius_m:
            filtered_places.append(replace(place, distance_m=distance_m))

    return filtered_places


def deduplicate_places(places: Iterable[NormalizedPlace]) -> list[NormalizedPlace]:
    deduped: dict[str, NormalizedPlace] = {}

    for place in places:
        key = place.place_id
        if not key:
            continue
        current = deduped.get(key)
        if current is None or completeness_score(place) > completeness_score(current):
            deduped[key] = place

    return list(deduped.values())
