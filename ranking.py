from __future__ import annotations

from dataclasses import asdict, dataclass, field
from typing import Any

from retrieval_models import NormalizedPlace


# Ranking constants
GLOBAL_MEAN_RATING = 4.2
MIN_REVIEWS_THRESHOLD = 50


@dataclass(frozen=True)
class RankedPlace:
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
    distance_m: float | None = None
    score: float | None = None
    is_ranked: bool = False
    rank_order: int | None = None


@dataclass(frozen=True)
class RankingMetadata:
    mean_rating: float
    min_reviews_threshold: int
    ranked_count: int
    unranked_count: int


@dataclass(frozen=True)
class RankingResult:
    places: list[RankedPlace]
    metadata: RankingMetadata


def calculate_bayesian_score(
    rating: float,
    user_ratings_total: int,
    *,
    mean_rating: float = GLOBAL_MEAN_RATING,
    min_reviews_threshold: int = MIN_REVIEWS_THRESHOLD,
) -> float:
    review_weight = user_ratings_total / (user_ratings_total + min_reviews_threshold)
    baseline_weight = min_reviews_threshold / (user_ratings_total + min_reviews_threshold)
    return (review_weight * rating) + (baseline_weight * mean_rating)


def is_rankable(place: NormalizedPlace) -> bool:
    return place.rating is not None and place.user_ratings_total is not None


def _to_ranked_place(
    place: NormalizedPlace,
    *,
    score: float | None,
    is_ranked_flag: bool,
    rank_order: int | None,
) -> RankedPlace:
    return RankedPlace(
        place_id=place.place_id,
        name=place.name,
        formatted_address=place.formatted_address,
        lat=place.lat,
        lng=place.lng,
        distance_m=place.distance_m,
        rating=place.rating,
        user_ratings_total=place.user_ratings_total,
        types=list(place.types),
        business_status=place.business_status,
        price_level=place.price_level,
        opening_hours=place.opening_hours,
        score=score,
        is_ranked=is_ranked_flag,
        rank_order=rank_order,
    )


def rank_places(
    places: list[NormalizedPlace],
    *,
    mean_rating: float = GLOBAL_MEAN_RATING,
    min_reviews_threshold: int = MIN_REVIEWS_THRESHOLD,
) -> RankingResult:
    ranked_candidates = [place for place in places if is_rankable(place)]
    unranked_places = [place for place in places if not is_rankable(place)]

    ranked_with_scores = [
        (
            place,
            calculate_bayesian_score(
                place.rating or 0.0,
                place.user_ratings_total or 0,
                mean_rating=mean_rating,
                min_reviews_threshold=min_reviews_threshold,
            ),
        )
        for place in ranked_candidates
    ]

    ranked_with_scores.sort(
        key=lambda item: (
            -item[1],
            -(item[0].user_ratings_total or 0),
            item[0].name.lower(),
            item[0].place_id,
        )
    )

    ranked_output = [
        _to_ranked_place(
            place,
            score=score,
            is_ranked_flag=True,
            rank_order=index,
        )
        for index, (place, score) in enumerate(ranked_with_scores, start=1)
    ]

    unranked_output = [
        _to_ranked_place(
            place,
            score=None,
            is_ranked_flag=False,
            rank_order=None,
        )
        for place in unranked_places
    ]

    return RankingResult(
        places=ranked_output + unranked_output,
        metadata=RankingMetadata(
            mean_rating=mean_rating,
            min_reviews_threshold=min_reviews_threshold,
            ranked_count=len(ranked_output),
            unranked_count=len(unranked_output),
        ),
    )


def serialize_ranking_result(result: RankingResult) -> dict[str, Any]:
    return {
        "places": [asdict(place) for place in result.places],
        "metadata": asdict(result.metadata),
    }
