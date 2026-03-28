from ranking import RankedPlace
from results_view import (
    TOP_RANKED_LIMIT,
    build_map_points_frame,
    build_ranked_results_frame,
    build_unranked_results_frame,
    format_distance_km,
    format_open_now,
    format_price_level,
)


def _ranked_place(
    place_id: str,
    *,
    is_ranked: bool = True,
    rank_order: int | None = 1,
    score: float | None = 4.56,
    rating: float | None = 4.7,
    reviews: int | None = 120,
    price_level: int | None = 2,
    opening_hours: bool | None = True,
    lat: float | None = 54.6872,
    lng: float | None = 25.2797,
    distance_m: float | None = 850,
) -> RankedPlace:
    return RankedPlace(
        place_id=place_id,
        name=f"Place {place_id}",
        formatted_address=f"{place_id} Street",
        lat=lat,
        lng=lng,
        distance_m=distance_m,
        rating=rating,
        user_ratings_total=reviews,
        types=["restaurant"],
        business_status="OPERATIONAL",
        price_level=price_level,
        opening_hours=opening_hours,
        score=score,
        is_ranked=is_ranked,
        rank_order=rank_order,
    )


def test_format_helpers_return_human_readable_values() -> None:
    assert format_price_level(None) == "-"
    assert format_price_level(3) == "$$$"
    assert format_distance_km(850) == "0.85 km"
    assert format_open_now(True) == "Open"
    assert format_open_now(False) == "Closed"
    assert format_open_now(None) == "Unknown"


def test_build_ranked_results_frame_limits_to_top_20_ranked_rows() -> None:
    places = [
        _ranked_place(f"ranked-{index}", rank_order=index)
        for index in range(1, TOP_RANKED_LIMIT + 3)
    ]
    places.append(_ranked_place("unranked", is_ranked=False, rank_order=None, score=None, rating=None, reviews=None))

    frame = build_ranked_results_frame(places)

    assert len(frame) == TOP_RANKED_LIMIT
    assert list(frame.columns) == [
        "Rank",
        "Name",
        "Score",
        "Rating",
        "Reviews",
        "Distance (km)",
        "Address",
        "Price",
        "Open Now",
    ]
    assert frame.iloc[0]["Rank"] == 1
    assert frame.iloc[0]["Distance (km)"] == "0.85 km"
    assert frame.iloc[-1]["Rank"] == TOP_RANKED_LIMIT


def test_build_unranked_and_map_frames_filter_expected_rows() -> None:
    places = [
        _ranked_place("ranked-a", rank_order=1),
        _ranked_place("ranked-b", rank_order=2, lat=None, lng=None),
        _ranked_place("unranked-a", is_ranked=False, rank_order=None, score=None, rating=None, reviews=None),
    ]

    unranked_frame = build_unranked_results_frame(places)
    map_frame = build_map_points_frame(places)

    assert len(unranked_frame) == 1
    assert unranked_frame.iloc[0]["Rank"] == "-"
    assert len(map_frame) == 1
    assert map_frame.iloc[0]["rank"] == 1
    assert map_frame.iloc[0]["distance"] == "0.85 km"
