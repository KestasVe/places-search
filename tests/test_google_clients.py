from geocoding import geocode_city
from places_client import search_text_places


class _FakeResponse:
    def __init__(self, payload: dict):
        self._payload = payload

    def raise_for_status(self) -> None:
        return None

    def json(self) -> dict:
        return self._payload


class _FakeSession:
    def __init__(self, payload: dict):
        self.payload = payload
        self.last_post_args = None
        self.last_post_kwargs = None

    def get(self, *args, **kwargs):
        return _FakeResponse(self.payload)

    def post(self, *args, **kwargs):
        self.last_post_args = args
        self.last_post_kwargs = kwargs
        return _FakeResponse(self.payload)


def test_geocode_city_raises_friendly_runtime_error_for_google_status_failure() -> None:
    session = _FakeSession({"status": "REQUEST_DENIED", "error_message": "API key invalid"})

    try:
        geocode_city("Vilnius", api_key="test-key", session=session)
    except RuntimeError as exc:
        assert "REQUEST_DENIED" in str(exc)
        assert "API key invalid" in str(exc)
    else:  # pragma: no cover
        raise AssertionError("Expected a RuntimeError for failed geocoding status")


def test_search_text_places_raises_friendly_runtime_error_for_google_status_failure() -> None:
    session = _FakeSession({"error": {"status": "RESOURCE_EXHAUSTED", "message": "Quota exceeded"}})

    try:
        search_text_places("Kebabai", "Vilnius", 54.6872, 25.2797, 10000, api_key="test-key", session=session)
    except RuntimeError as exc:
        assert "RESOURCE_EXHAUSTED" in str(exc)
        assert "Quota exceeded" in str(exc)
    else:  # pragma: no cover
        raise AssertionError("Expected a RuntimeError for failed places status")


def test_search_text_places_uses_text_search_with_location_bias_and_keyword_query() -> None:
    session = _FakeSession(
        {
            "places": [
                {
                    "id": "abc123",
                    "displayName": {"text": "Express Pizza"},
                    "formattedAddress": "Vilnius Street 1",
                    "location": {"latitude": 54.6872, "longitude": 25.2797},
                    "rating": 4.7,
                    "userRatingCount": 120,
                    "types": ["pizza_restaurant", "establishment"],
                    "businessStatus": "OPERATIONAL",
                    "priceLevel": "PRICE_LEVEL_MODERATE",
                    "currentOpeningHours": {"openNow": True},
                }
            ],
            "nextPageToken": "token-1",
        }
    )

    payload = search_text_places("Express Pizza", "Vilnius", 54.6872, 25.2797, 3000, api_key="test-key", session=session)

    assert session.last_post_kwargs is not None
    assert session.last_post_kwargs["json"]["textQuery"] == "Express Pizza near Vilnius"
    assert "locationBias" in session.last_post_kwargs["json"]
    assert "locationRestriction" not in session.last_post_kwargs["json"]
    assert "type" not in session.last_post_kwargs["json"]
    assert payload["next_page_token"] == "token-1"
    assert payload["results"][0]["place_id"] == "abc123"
    assert payload["results"][0]["name"] == "Express Pizza"
