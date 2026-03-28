from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass(frozen=True)
class NormalizedPlace:
    place_id: str
    name: str
    formatted_address: str
    lat: float | None
    lng: float | None
    rating: float | None
    user_ratings_total: int | None
    types: list[str] = field(default_factory=list)
    business_status: str | None = None
    price_level: int | None = None
    opening_hours: bool | None = None


@dataclass(frozen=True)
class RetrievalMetadata:
    resolved_city_address: str | None
    center_lat: float | None
    center_lng: float | None
    requested_radius_km: int
    requested_radius_m: int
    warnings: list[str] = field(default_factory=list)


@dataclass(frozen=True)
class RetrievalError:
    code: str
    message: str
    query_context: dict[str, Any] = field(default_factory=dict)


@dataclass(frozen=True)
class RetrievalResult:
    places: list[NormalizedPlace] = field(default_factory=list)
    metadata: RetrievalMetadata | None = None
    error: RetrievalError | None = None
