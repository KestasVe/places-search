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

    def get(self, *args, **kwargs):
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
    session = _FakeSession({"status": "OVER_QUERY_LIMIT", "error_message": "Quota exceeded"})

    try:
        search_text_places("Kebabai", 54.6872, 25.2797, 10000, api_key="test-key", session=session)
    except RuntimeError as exc:
        assert "OVER_QUERY_LIMIT" in str(exc)
        assert "Quota exceeded" in str(exc)
    else:  # pragma: no cover
        raise AssertionError("Expected a RuntimeError for failed places status")
