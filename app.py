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

PAGE_TITLE = "Places Ranker"
PAGE_CAPTION = "Find and rank the best places with Google Places data."
GOOGLE_API_KEY_NAME = "GOOGLE_PLACES_API_KEY"
CITY_HELP = "Lithuanian and English city names are both acceptable."
CATEGORY_PLACEHOLDER = "Museums, Cafes"
SEARCH_CTA_LABEL = "Search places"
RESULTS_LIMIT = 20
QUERY_STATE_KEY = "search_query"
RETRIEVAL_STATE_KEY = "retrieval_result"
RANKING_STATE_KEY = "ranking_result"
CITY_TOUCHED_KEY = "city_touched"
CATEGORY_TOUCHED_KEY = "category_touched"


def get_google_places_api_key() -> str:
    if GOOGLE_API_KEY_NAME in st.secrets:
        return st.secrets[GOOGLE_API_KEY_NAME]
    return os.getenv(GOOGLE_API_KEY_NAME, "")


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
    results_map = folium.Map(location=[center_lat, center_lng], zoom_start=12, tiles="CartoDB dark_matter")

    for point in map_points.to_dict("records"):
        popup_html = (
            f"<strong>#{point['rank']} {point['name']}</strong><br>"
            f"Score: {point['score']}<br>"
            f"Rating: {point['rating']} ({point['reviews']} reviews)<br>"
            f"Distance: {point['distance']}<br>"
            f"{point['address']}"
        )
        folium.CircleMarker(
            location=[point["lat"], point["lng"]],
            popup=popup_html,
            tooltip=f"#{point['rank']} {point['name']}",
            radius=7,
            color="#56B4FF",
            weight=2,
            fill=True,
            fill_color="#56B4FF",
            fill_opacity=0.7,
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
        --shell-bg: #06080d;
        --shell-bg-alt: #0b1119;
        --surface-bg: #0f1722;
        --surface-border: rgba(110, 149, 204, 0.22);
        --surface-border-strong: rgba(78, 171, 255, 0.4);
        --accent: #2f9bff;
        --accent-strong: #56b4ff;
        --text: #f3f6fb;
        --text-muted: #aeb9c8;
        --danger: #ff6f7d;
        --shadow: 0 24px 60px rgba(0, 0, 0, 0.45);
        --glow: 0 0 0 1px rgba(86, 180, 255, 0.16), 0 0 28px rgba(47, 155, 255, 0.18);
    }

    .stApp {
        background:
            radial-gradient(circle at top left, rgba(47, 155, 255, 0.16), transparent 28%),
            radial-gradient(circle at top right, rgba(73, 129, 221, 0.14), transparent 24%),
            linear-gradient(180deg, var(--shell-bg-alt) 0%, var(--shell-bg) 100%);
        color: var(--text);
    }

    .stApp,
    .stApp p,
    .stApp label,
    .stApp input,
    .stApp textarea,
    .stApp button,
    .stApp h1,
    .stApp h2,
    .stApp h3 {
        font-family: "Inter", "Segoe UI", sans-serif;
    }

    .material-symbols-rounded,
    .material-symbols-sharp,
    .material-symbols-outlined {
        font-family: "Material Symbols Rounded", "Material Symbols Sharp", "Material Symbols Outlined" !important;
        font-weight: normal;
        font-style: normal;
    }

    .block-container {
        max-width: 1180px;
        padding-top: 2rem;
        padding-bottom: 6rem;
    }

    .title-shell {
        display: flex;
        align-items: center;
        gap: 0.9rem;
        margin-bottom: 0.35rem;
    }

    .flag-icon {
        width: 28px;
        height: 20px;
        border-radius: 999px;
        background: linear-gradient(180deg, #f0c419 0 33.33%, #217346 33.33% 66.66%, #c93131 66.66% 100%);
        box-shadow: 0 0 0 1px rgba(255, 255, 255, 0.14), 0 0 18px rgba(255, 255, 255, 0.08);
        flex-shrink: 0;
    }

    .title-copy h1 {
        margin: 0;
        color: var(--text);
        font-size: clamp(2.1rem, 4vw, 3.2rem);
        line-height: 1.05;
        letter-spacing: -0.03em;
        font-weight: 700;
    }

    .title-copy p {
        margin: 0.45rem 0 0;
        color: var(--text-muted);
        font-size: 1rem;
        line-height: 1.55;
        max-width: 760px;
    }

    .phase-shell {
        position: relative;
        overflow: hidden;
        background: linear-gradient(180deg, rgba(20, 33, 52, 0.96) 0%, rgba(10, 18, 29, 0.98) 100%);
        border: 1px solid var(--surface-border);
        border-radius: 22px;
        padding: 1.4rem 1.5rem;
        margin: 1.25rem 0 1.5rem;
        box-shadow:
            inset 0 1px 0 rgba(255, 255, 255, 0.04),
            inset 0 -12px 24px rgba(0, 0, 0, 0.28),
            0 18px 32px rgba(0, 0, 0, 0.34),
            0 0 36px rgba(47, 155, 255, 0.12);
    }

    .phase-shell h2 {
        position: relative;
        margin: 0 0 0.45rem;
        color: var(--text);
        font-size: 1.25rem;
        font-weight: 650;
        letter-spacing: -0.02em;
    }

    .phase-shell p {
        position: relative;
        color: var(--text-muted);
        margin-bottom: 0;
        line-height: 1.6;
    }

    .phase-shell::before {
        content: "";
        position: absolute;
        inset: 0;
        border-radius: inherit;
        padding: 1px;
        background: linear-gradient(135deg, rgba(86, 180, 255, 0.42), transparent 32%, transparent 68%, rgba(86, 180, 255, 0.18));
        -webkit-mask:
            linear-gradient(#fff 0 0) content-box,
            linear-gradient(#fff 0 0);
        -webkit-mask-composite: xor;
        mask-composite: exclude;
        pointer-events: none;
    }

    h1, h2, h3 {
        color: var(--text);
    }

    [data-testid="stMetric"] {
        background: linear-gradient(180deg, rgba(15, 23, 34, 0.98) 0%, rgba(9, 15, 24, 0.98) 100%);
        border: 1px solid var(--surface-border);
        border-radius: 18px;
        padding: 0.9rem 1rem;
        box-shadow: var(--shadow);
    }

    [data-testid="stMetricLabel"],
    [data-testid="stMetricValue"],
    [data-testid="stMetricDelta"] {
        color: var(--text);
    }

    [data-testid="stTextInputRootElement"] input {
        background: rgba(11, 17, 25, 0.92) !important;
        color: var(--text) !important;
        border: 1px solid var(--surface-border-strong) !important;
        border-radius: 16px !important;
        box-shadow: var(--glow);
    }

    [data-testid="stTextInputRootElement"] input::placeholder {
        color: #7f8ca0 !important;
    }

    [data-testid="stTextInputRootElement"] input:focus {
        border-color: var(--accent-strong) !important;
        box-shadow: 0 0 0 1px rgba(86, 180, 255, 0.38), 0 0 28px rgba(47, 155, 255, 0.22) !important;
    }

    [data-testid="stSlider"] label,
    [data-testid="stTextInput"] label {
        color: var(--text);
        font-weight: 600;
    }

    [data-baseweb="slider"] [role="slider"] {
        background: radial-gradient(circle at 30% 30%, #ffffff, #89cbff 44%, #2f9bff 72%) !important;
        border: 2px solid rgba(255, 255, 255, 0.82) !important;
        box-shadow: 0 0 0 6px rgba(47, 155, 255, 0.18), 0 0 24px rgba(47, 155, 255, 0.42) !important;
    }

    [data-baseweb="slider"] > div > div > div {
        background: linear-gradient(90deg, rgba(47, 155, 255, 0.28), rgba(86, 180, 255, 0.92)) !important;
    }

    .stButton > button {
        background: linear-gradient(135deg, #10365e 0%, #2f9bff 100%);
        color: #f8fbff;
        border: 1px solid rgba(125, 201, 255, 0.4);
        border-radius: 16px;
        min-height: 3rem;
        font-weight: 650;
        letter-spacing: 0.01em;
        box-shadow: 0 10px 28px rgba(47, 155, 255, 0.24), inset 0 1px 0 rgba(255, 255, 255, 0.16);
    }

    .stButton > button:hover {
        border-color: rgba(173, 224, 255, 0.7);
        box-shadow: 0 14px 32px rgba(47, 155, 255, 0.32), 0 0 24px rgba(47, 155, 255, 0.18);
        transform: translateY(-1px);
    }

    .stButton > button:disabled {
        background: linear-gradient(180deg, rgba(35, 50, 69, 0.9), rgba(22, 31, 43, 0.92));
        color: #8490a3;
        border-color: rgba(85, 101, 126, 0.35);
        box-shadow: none;
    }

    [data-testid="stDataFrame"],
    [data-testid="stExpander"],
    [data-testid="stAlertContainer"] {
        background: linear-gradient(180deg, rgba(12, 19, 29, 0.92) 0%, rgba(9, 15, 24, 0.98) 100%);
        border: 1px solid var(--surface-border);
        border-radius: 18px;
        box-shadow: var(--shadow);
    }

    [data-testid="stDataFrame"] * {
        color: var(--text) !important;
    }

    [data-testid="stMarkdownContainer"] code {
        background: rgba(47, 155, 255, 0.14);
        color: #cfe9ff;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

st.markdown(
    f"""
    <div class="title-shell">
        <span class="flag-icon" aria-hidden="true"></span>
        <div class="title-copy">
            <h1>{PAGE_TITLE}</h1>
            <p>{PAGE_CAPTION}</p>
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)

if not api_key:
    st.error(
        "Missing Google Places API key. Configure `GOOGLE_PLACES_API_KEY` in Streamlit secrets or a local `.env` file."
    )
    st.info(
        "For Streamlit Cloud, add the key in app secrets. For local development, set it in `.env` before launching the app."
    )
    st.stop()

st.markdown(
    """
    <div class="phase-shell">
        <h2>Find the strongest places fast</h2>
        <p>Search by city, keyword, and radius to see a Bayesian-ranked table and map without manual Google Maps triage.</p>
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
        "Keyword",
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

        with st.expander("🔎 Debug envelopes"):
            st.caption("Phase 2 retrieval")
            st.json(serialize_retrieval_result(retrieval_result))
            st.caption("Phase 3 ranking")
            st.json(serialize_ranking_result(ranking_result))
