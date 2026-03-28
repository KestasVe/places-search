from __future__ import annotations

from dataclasses import dataclass
import re


_WHITESPACE_RE = re.compile(r"\s+")


@dataclass(frozen=True)
class SearchQuery:
    city_raw: str
    city_normalized: str
    category_raw: str
    category_normalized: str
    radius_km: int
    radius_m: int


def normalize_text_input(raw: str) -> str:
    return _WHITESPACE_RE.sub(" ", raw.strip()).lower()


def build_search_query(city_raw: str, category_raw: str, radius_km: int) -> SearchQuery:
    return SearchQuery(
        city_raw=city_raw,
        city_normalized=normalize_text_input(city_raw),
        category_raw=category_raw,
        category_normalized=normalize_text_input(category_raw),
        radius_km=radius_km,
        radius_m=radius_km * 1000,
    )


def validate_search_inputs(city_raw: str, category_raw: str) -> dict[str, str]:
    errors: dict[str, str] = {}

    if not normalize_text_input(city_raw):
        errors["city"] = "Enter a city before searching."

    if not normalize_text_input(category_raw):
        errors["category"] = "Enter a category before searching."

    return errors
