import os

import streamlit as st
from dotenv import load_dotenv


load_dotenv()

PAGE_TITLE = "Lithuania Places Ranker"
PAGE_CAPTION = "Find and rank the best places in Lithuania with Google Places data."
CITY_HELP = "Lithuanian and English city names are both acceptable."
CATEGORY_PLACEHOLDER = "Kebabai, Museums, Cafes"
SEARCH_CTA_LABEL = "Search places"


def get_google_places_api_key() -> str:
    if "GOOGLE_PLACES_API_KEY" in st.secrets:
        return st.secrets["GOOGLE_PLACES_API_KEY"]
    return os.getenv("GOOGLE_PLACES_API_KEY", "")


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

city = st.text_input("City", help=CITY_HELP)
category = st.text_input("Category", placeholder=CATEGORY_PLACEHOLDER)
radius_km = st.slider("Radius (km)", min_value=1, max_value=50, value=10)
st.button(SEARCH_CTA_LABEL, use_container_width=True)
