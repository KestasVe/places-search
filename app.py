import os

import streamlit as st
from dotenv import load_dotenv


load_dotenv()


def get_google_places_api_key() -> str:
    if "GOOGLE_PLACES_API_KEY" in st.secrets:
        return st.secrets["GOOGLE_PLACES_API_KEY"]
    return os.getenv("GOOGLE_PLACES_API_KEY", "")


st.set_page_config(page_title="Lithuania Places Ranker", layout="wide")

api_key = get_google_places_api_key()

st.title("Lithuania Places Ranker")
st.caption("Find and rank the best places in Lithuania with Google Places data.")

if not api_key:
    st.warning(
        "Set `GOOGLE_PLACES_API_KEY` in Streamlit secrets or environment variables "
        "before implementing live searches."
    )

st.subheader("Planned v1 Search Flow")
st.write(
    "Search by city, category, and radius, then rank places using a Bayesian weighted score."
)

city = st.selectbox("City", ["Vilnius", "Kaunas", "Klaipeda", "Siauliai", "Panevezys"])
category = st.text_input("Category", placeholder="Kebabai")
radius_km = st.slider("Radius (km)", min_value=1, max_value=50, value=10)

st.dataframe(
    [
        {"rank": 1, "name": "Example Place", "rating": 4.8, "reviews": 500, "score": 4.76},
        {"rank": 2, "name": "Another Place", "rating": 4.7, "reviews": 420, "score": 4.66},
    ],
    use_container_width=True,
)

st.map(
    [
        {"lat": 54.6872, "lon": 25.2797},
        {"lat": 54.6896, "lon": 25.2685},
    ]
)

st.info(
    f"Placeholder UI only. Current inputs: city={city}, category={category or 'n/a'}, "
    f"radius={radius_km}km."
)
