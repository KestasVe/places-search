from __future__ import annotations

import pandas as pd

from ranking import RankedPlace


TOP_RANKED_LIMIT = 20


def format_price_level(price_level: int | None) -> str:
    if price_level is None or price_level <= 0:
        return "-"
    return "$" * price_level


def format_open_now(opening_hours: bool | None) -> str:
    if opening_hours is True:
        return "Open"
    if opening_hours is False:
        return "Closed"
    return "Unknown"


def _format_score(score: float | None) -> str:
    if score is None:
        return "-"
    return f"{score:.2f}"


def _format_rating(rating: float | None) -> str:
    if rating is None:
        return "-"
    return f"{rating:.1f}"


def _build_table_row(place: RankedPlace) -> dict[str, object]:
    return {
        "Rank": place.rank_order if place.rank_order is not None else "-",
        "Name": place.name,
        "Score": _format_score(place.score),
        "Rating": _format_rating(place.rating),
        "Reviews": place.user_ratings_total if place.user_ratings_total is not None else "-",
        "Address": place.formatted_address,
        "Price": format_price_level(place.price_level),
        "Open Now": format_open_now(place.opening_hours),
    }


def build_ranked_results_frame(places: list[RankedPlace], limit: int = TOP_RANKED_LIMIT) -> pd.DataFrame:
    ranked_places = [place for place in places if place.is_ranked][:limit]
    return pd.DataFrame([_build_table_row(place) for place in ranked_places])


def build_unranked_results_frame(places: list[RankedPlace]) -> pd.DataFrame:
    unranked_places = [place for place in places if not place.is_ranked]
    return pd.DataFrame([_build_table_row(place) for place in unranked_places])


def build_map_points_frame(places: list[RankedPlace], limit: int = TOP_RANKED_LIMIT) -> pd.DataFrame:
    ranked_places = [
        place for place in places if place.is_ranked and place.lat is not None and place.lng is not None
    ][:limit]

    return pd.DataFrame(
        [
            {
                "rank": place.rank_order,
                "name": place.name,
                "score": _format_score(place.score),
                "rating": _format_rating(place.rating),
                "reviews": place.user_ratings_total if place.user_ratings_total is not None else "-",
                "address": place.formatted_address,
                "lat": place.lat,
                "lng": place.lng,
            }
            for place in ranked_places
        ]
    )
