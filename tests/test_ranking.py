from retrieval_models import NormalizedPlace
from ranking import MIN_REVIEWS_THRESHOLD, GLOBAL_MEAN_RATING, calculate_bayesian_score, rank_places


def _place(
    place_id: str,
    *,
    rating: float | None,
    user_ratings_total: int | None,
    name: str | None = None,
) -> NormalizedPlace:
    return NormalizedPlace(
        place_id=place_id,
        name=name or place_id,
        formatted_address=f"{place_id} Street",
        lat=54.6872,
        lng=25.2797,
        rating=rating,
        user_ratings_total=user_ratings_total,
        types=["restaurant"],
        business_status="OPERATIONAL",
        price_level=2,
        opening_hours=True,
    )


def test_calculate_bayesian_score_uses_global_mean_and_fixed_threshold() -> None:
    score = calculate_bayesian_score(4.8, 100)

    expected = ((100 / (100 + MIN_REVIEWS_THRESHOLD)) * 4.8) + (
        (MIN_REVIEWS_THRESHOLD / (100 + MIN_REVIEWS_THRESHOLD)) * GLOBAL_MEAN_RATING
    )

    assert score == expected


def test_rank_places_orders_by_score_then_user_ratings_total() -> None:
    # These two places have the same score because their ratings match.
    result = rank_places(
        [
            _place("lower-reviews", rating=4.5, user_ratings_total=120, name="Alpha"),
            _place("higher-reviews", rating=4.5, user_ratings_total=300, name="Beta"),
            _place("best-score", rating=4.9, user_ratings_total=250, name="Gamma"),
        ]
    )

    assert [place.place_id for place in result.places[:3]] == [
        "best-score",
        "higher-reviews",
        "lower-reviews",
    ]
    assert [place.rank_order for place in result.places[:3]] == [1, 2, 3]
    assert all(place.is_ranked for place in result.places[:3])


def test_rank_places_keeps_missing_rating_data_as_unranked() -> None:
    result = rank_places(
        [
            _place("ranked", rating=4.7, user_ratings_total=180),
            _place("missing-rating", rating=None, user_ratings_total=180),
            _place("missing-reviews", rating=4.8, user_ratings_total=None),
        ]
    )

    assert [place.place_id for place in result.places] == [
        "ranked",
        "missing-rating",
        "missing-reviews",
    ]
    assert result.places[0].is_ranked is True
    assert result.places[0].rank_order == 1
    assert result.places[1].is_ranked is False
    assert result.places[1].rank_order is None
    assert result.places[1].score is None
    assert result.places[2].is_ranked is False
    assert result.places[2].rank_order is None
    assert result.metadata.ranked_count == 1
    assert result.metadata.unranked_count == 2
