import os

import streamlit as st
from dotenv import load_dotenv

from ranking import rank_places, serialize_ranking_result
from query import build_search_query, can_submit_search, normalize_text_input, validate_search_inputs
from results_view import build_map_points_frame, build_ranked_results_frame, build_unranked_results_frame
from retrieval import retrieve_places, serialize_retrieval_result

try:
    import folium
    from streamlit_folium import st_folium
except ImportError:  # pragma: no cover - runtime fallback for local environments without Phase 4 deps
    folium = None
    st_folium = None


load_dotenv()

PAGE_TITLE = "Lithuania Places Ranker"
PAGE_CAPTION = "Find and rank the best places in Lithuania with Google Places data."
CITY_HELP = "Lithuanian and English city names are both acceptable."
CATEGORY_PLACEHOLDER = "Kebabai, Museums, Cafes"
SEARCH_CTA_LABEL = "Search places"
RESULTS_LIMIT = 20
QUERY_STATE_KEY = "search_query"
RETRIEVAL_STATE_KEY = "retrieval_result"
RANKING_STATE_KEY = "ranking_result"
CITY_TOUCHED_KEY = "city_touched"
CATEGORY_TOUCHED_KEY = "category_touched"


def get_google_places_api_key() -> str:
    if "GOOGLE_PLACES_API_KEY" in st.secrets:
        return st.secrets["GOOGLE_PLACES_API_KEY"]
    return os.getenv("GOOGLE_PLACES_API_KEY", "")


def mark_city_touched() -> None:
    st.session_state[CITY_TOUCHED_KEY] = True


def mark_category_touched() -> None:
    st.session_state[CATEGORY_TOUCHED_KEY] = True


def render_inline_error(field_key: str, message: str) -> None:
    if not message:
        return
    if field_key == "city" and st.session_state.get(CITY_TOUCHED_KEY):
        st.error(message)
    if field_key == "category" and st.session_state.get(CATEGORY_TOUCHED_KEY):
        st.error(message)


@st.cache_data(show_spinner=False)
def run_search_pipeline(search_query, api_key: str):
    retrieval_result = retrieve_places(search_query, api_key=api_key)
    ranking_result = rank_places(retrieval_result.places)
    return retrieval_result, ranking_result


def render_result_metrics(ranking_result) -> None:
    metric_one, metric_two, metric_three = st.columns(3)
    with metric_one:
        st.metric("Ranked places", ranking_result.metadata.ranked_count)
    with metric_two:
        st.metric("Unranked kept", ranking_result.metadata.unranked_count)
    with metric_three:
        st.metric("Bayesian baseline", f"{ranking_result.metadata.mean_rating:.1f}")


def render_results_table(ranking_result) -> None:
    ranked_frame = build_ranked_results_frame(ranking_result.places, limit=RESULTS_LIMIT)
    if ranked_frame.empty:
        st.info("No ranked places were available for this search.")
    else:
        st.subheader("Top ranked places")
        st.dataframe(ranked_frame, use_container_width=True, hide_index=True)

    unranked_frame = build_unranked_results_frame(ranking_result.places)
    if not unranked_frame.empty:
        with st.expander(f"Show unranked places ({len(unranked_frame)})"):
            st.dataframe(unranked_frame, use_container_width=True, hide_index=True)


def render_results_map(ranking_result, retrieval_result) -> None:
    map_points = build_map_points_frame(ranking_result.places, limit=RESULTS_LIMIT)
    st.subheader("Map")

    if map_points.empty:
        st.info("No ranked places with coordinates are available to plot on the map.")
        return

    if folium is None or st_folium is None:
        st.warning("Install `folium` and `streamlit-folium` to enable the interactive map view.")
        st.map(map_points.rename(columns={"lat": "latitude", "lng": "longitude"})[["latitude", "longitude"]])
        return

    center_lat = retrieval_result.metadata.center_lat if retrieval_result.metadata else map_points.iloc[0]["lat"]
    center_lng = retrieval_result.metadata.center_lng if retrieval_result.metadata else map_points.iloc[0]["lng"]
    results_map = folium.Map(location=[center_lat, center_lng], zoom_start=12, tiles="CartoDB positron")

    for point in map_points.to_dict("records"):
        popup_html = (
            f"<strong>#{point['rank']} {point['name']}</strong><br>"
            f"Score: {point['score']}<br>"
            f"Rating: {point['rating']} ({point['reviews']} reviews)<br>"
            f"{point['address']}"
        )
        folium.Marker(
            location=[point["lat"], point["lng"]],
            popup=popup_html,
            tooltip=f"#{point['rank']} {point['name']}",
        ).add_to(results_map)

    st_folium(results_map, use_container_width=True, height=520)


def render_feedback_states(retrieval_result, ranking_result) -> bool:
    if retrieval_result.error:
        st.error(retrieval_result.error.message)
        return False

    if retrieval_result.metadata:
        for warning in retrieval_result.metadata.warnings:
            st.warning(warning)

    if not retrieval_result.places:
        resolved_label = (
            retrieval_result.metadata.resolved_city_address
            if retrieval_result.metadata and retrieval_result.metadata.resolved_city_address
            else "the selected location"
        )
        st.info(f"No places matched this search near {resolved_label}.")
        return False

    if ranking_result.metadata.ranked_count == 0:
        st.info("Places were found, but none had enough rating data to be ranked.")
    return True


st.set_page_config(page_title=PAGE_TITLE, layout="wide")

api_key = get_google_places_api_key()

st.markdown(
    """
    <style>
    :root {
        --shell-bg: #F6F3EC;
        --surface-bg: #E4DCCB;
        --surface-border: #D6CAB5;
        --accent: #C46A2D;
        --text: #2F241B;
        --muted: #5F5246;
        --danger: #B13A2E;
    }

    .stApp {
        background: var(--shell-bg);
        color: var(--text);
    }

    .phase-shell {
        background: var(--surface-bg);
        border: 1px solid var(--surface-border);
        border-radius: 18px;
        padding: 24px;
        margin-top: 24px;
        box-shadow: 0 12px 28px rgba(47, 36, 27, 0.08);
    }

    .phase-shell h2 {
        margin-bottom: 8px;
    }

    .phase-shell p {
        color: var(--muted);
        margin-bottom: 0;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

st.title(PAGE_TITLE)
st.caption(PAGE_CAPTION)

if not api_key:
    st.warning(
        "Set `GOOGLE_PLACES_API_KEY` in Streamlit secrets or environment variables before running live searches."
    )

st.markdown(
    """
    <div class="phase-shell">
        <h2>Find the strongest places fast</h2>
        <p>Search by city, category, and radius to see a Bayesian-ranked table and map without manual Google Maps triage.</p>
    </div>
    """,
    unsafe_allow_html=True,
)

st.session_state.setdefault(CITY_TOUCHED_KEY, False)
st.session_state.setdefault(CATEGORY_TOUCHED_KEY, False)

with st.container():
    city = st.text_input("City", help=CITY_HELP, key="city_input", on_change=mark_city_touched)
    city_normalized = normalize_text_input(city)
    if not city_normalized and city:
        st.session_state[CITY_TOUCHED_KEY] = True

    category = st.text_input(
        "Category",
        placeholder=CATEGORY_PLACEHOLDER,
        key="category_input",
        on_change=mark_category_touched,
    )
    category_normalized = normalize_text_input(category)
    if not category_normalized and category:
        st.session_state[CATEGORY_TOUCHED_KEY] = True

    radius_km = st.slider("Radius (km)", min_value=1, max_value=50, value=10)

    current_errors = validate_search_inputs(city, category)
    render_inline_error("city", current_errors.get("city", ""))
    render_inline_error("category", current_errors.get("category", ""))

    button_disabled = not can_submit_search(city, category)
    search_clicked = st.button(
        SEARCH_CTA_LABEL,
        use_container_width=True,
        disabled=button_disabled,
        type="primary",
    )

if search_clicked:
    current_errors = validate_search_inputs(city, category)
    if current_errors:
        st.session_state[CITY_TOUCHED_KEY] = True
        st.session_state[CATEGORY_TOUCHED_KEY] = True
        render_inline_error("city", current_errors.get("city", ""))
        render_inline_error("category", current_errors.get("category", ""))
    else:
        search_query = build_search_query(city, category, radius_km)
        st.session_state[QUERY_STATE_KEY] = search_query
        if not api_key:
            st.session_state[RETRIEVAL_STATE_KEY] = None
            st.session_state[RANKING_STATE_KEY] = None
            st.error("A Google Places API key is required before searches can run.")
        else:
            with st.spinner("Fetching Google Places results and ranking them..."):
                retrieval_result, ranking_result = run_search_pipeline(search_query, api_key)
            st.session_state[RETRIEVAL_STATE_KEY] = retrieval_result
            st.session_state[RANKING_STATE_KEY] = ranking_result

if QUERY_STATE_KEY in st.session_state:
    search_query = st.session_state[QUERY_STATE_KEY]
    st.success(
        f"Showing results for {search_query.category_raw} near {search_query.city_raw} within {search_query.radius_km} km."
    )

if RETRIEVAL_STATE_KEY in st.session_state and st.session_state[RETRIEVAL_STATE_KEY] is not None:
    retrieval_result = st.session_state[RETRIEVAL_STATE_KEY]
    ranking_result = st.session_state.get(RANKING_STATE_KEY)
    if ranking_result is not None:
        should_render_results = render_feedback_states(retrieval_result, ranking_result)
        render_result_metrics(ranking_result)

        if should_render_results:
            results_column, map_column = st.columns([1.15, 1], gap="large")
            with results_column:
                render_results_table(ranking_result)
            with map_column:
                render_results_map(ranking_result, retrieval_result)

        with st.expander("Debug envelopes"):
            st.caption("Phase 2 retrieval")
            st.json(serialize_retrieval_result(retrieval_result))
            st.caption("Phase 3 ranking")
            st.json(serialize_ranking_result(ranking_result))
