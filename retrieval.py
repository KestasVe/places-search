from __future__ import annotations

from dataclasses import asdict
from typing import Any, Callable

from geocoding import GeocodingResolution, geocode_city
from places_client import search_text_places
from query import SearchQuery
from retrieval_models import RetrievalError, RetrievalMetadata, RetrievalResult
from retrieval_normalization import (
    deduplicate_places,
    filter_operational_places,
    filter_places_within_radius,
    normalize_place_payload,
)


MAX_PLACES_PAGES = 3


GeocodeFn = Callable[[str, str | None], GeocodingResolution]
PlacesSearchFn = Callable[[str, float, float, int, str | None, str | None], dict[str, Any]]


def build_query_context(search_query: SearchQuery) -> dict[str, Any]:
    return {
        "city_raw": search_query.city_raw,
        "city_normalized": search_query.city_normalized,
        "category_raw": search_query.category_raw,
        "category_normalized": search_query.category_normalized,
        "radius_km": search_query.radius_km,
        "radius_m": search_query.radius_m,
    }


def _build_metadata(
    search_query: SearchQuery,
    resolution: GeocodingResolution,
    warnings: list[str],
) -> RetrievalMetadata:
    return RetrievalMetadata(
        resolved_city_address=resolution.formatted_address,
        center_lat=resolution.lat,
        center_lng=resolution.lng,
        requested_radius_km=search_query.radius_km,
        requested_radius_m=search_query.radius_m,
        warnings=warnings,
    )


def retrieve_places(
    search_query: SearchQuery,
    api_key: str | None = None,
    geocode_fn: GeocodeFn = geocode_city,
    places_search_fn: PlacesSearchFn = search_text_places,
) -> RetrievalResult:
    query_context = build_query_context(search_query)

    try:
        resolution = geocode_fn(search_query.city_raw, api_key)
    except Exception as exc:  # pragma: no cover - exercised by service tests
        return RetrievalResult(
            error=RetrievalError(
                code="geocoding_not_found",
                message=str(exc),
                query_context=query_context,
            )
        )

    warnings = list(resolution.warnings)
    raw_places: list[dict[str, Any]] = []
    page_token: str | None = None

    for page_number in range(1, MAX_PLACES_PAGES + 1):
        try:
            payload = places_search_fn(
                search_query.category_raw,
                resolution.lat,
                resolution.lng,
                search_query.radius_m,
                api_key,
                page_token,
            )
        except Exception as exc:  # pragma: no cover - exercised by service tests
            warnings.append(f"Places page {page_number} failed: {exc}")
            break

        raw_places.extend(payload.get("results") or [])
        page_token = payload.get("next_page_token")
        if not page_token:
            break

    print(f"[debug] Google raw results before radius filter: {len(raw_places)}")

    normalized_places = [normalize_place_payload(raw_place) for raw_place in raw_places]
    normalized_places = filter_operational_places(normalized_places)
    normalized_places = filter_places_within_radius(
        normalized_places,
        resolution.lat,
        resolution.lng,
        search_query.radius_m,
    )
    normalized_places = deduplicate_places(normalized_places)

    metadata = _build_metadata(search_query, resolution, warnings)
    return RetrievalResult(places=normalized_places, metadata=metadata, error=None)


def serialize_retrieval_result(result: RetrievalResult) -> dict[str, Any]:
    return {
        "places": [asdict(place) for place in result.places],
        "metadata": asdict(result.metadata) if result.metadata else None,
        "error": asdict(result.error) if result.error else None,
    }
