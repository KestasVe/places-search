import os

import streamlit as st
from dotenv import load_dotenv

from query import build_search_query, can_submit_search, normalize_text_input, validate_search_inputs
from retrieval import retrieve_places, serialize_retrieval_result


load_dotenv()

PAGE_TITLE = "Lithuania Places Ranker"
PAGE_CAPTION = "Find and rank the best places in Lithuania with Google Places data."
CITY_HELP = "Lithuanian and English city names are both acceptable."
CATEGORY_PLACEHOLDER = "Kebabai, Museums, Cafes"
SEARCH_CTA_LABEL = "Search places"
QUERY_STATE_KEY = "search_query"
RETRIEVAL_STATE_KEY = "retrieval_result"
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
        "Set `GOOGLE_PLACES_API_KEY` in Streamlit secrets or environment variables "
        "before implementing live searches."
    )

st.markdown(
    """
    <div class="phase-shell">
        <h2>Ready to search Lithuania</h2>
        <p>Enter a city, category, and radius to prepare a ranked search query. Results appear in later phases.</p>
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
        st.session_state[RETRIEVAL_STATE_KEY] = retrieve_places(search_query, api_key=api_key)

if QUERY_STATE_KEY in st.session_state:
    search_query = st.session_state[QUERY_STATE_KEY]
    st.success("Search query captured and sent through the Phase 2 retrieval pipeline.")
    st.json(
        {
            "city_raw": search_query.city_raw,
            "city_normalized": search_query.city_normalized,
            "category_raw": search_query.category_raw,
            "category_normalized": search_query.category_normalized,
            "radius_km": search_query.radius_km,
            "radius_m": search_query.radius_m,
        }
    )

if RETRIEVAL_STATE_KEY in st.session_state:
    retrieval_result = st.session_state[RETRIEVAL_STATE_KEY]
    if retrieval_result.error:
        st.error(retrieval_result.error.message)

    st.subheader("Phase 2 Retrieval Envelope")
    st.json(serialize_retrieval_result(retrieval_result))
