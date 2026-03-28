# Lithuania Places Ranker

Streamlit app for searching, ranking, and mapping places using the Google Places API.

## Run locally

1. Install dependencies:
   `C:\Users\user\AppData\Local\Programs\Python\Python311\python.exe -m pip install -r requirements.txt`
2. Set `GOOGLE_PLACES_API_KEY` in [.env](C:/Users/user/Desktop/files/projects/it_projects/gsd_codex_test/.env) using the placeholder format already in the repo.
3. Start Streamlit:
   `C:\Users\user\AppData\Local\Programs\Python\Python311\Scripts\streamlit.exe run app.py`

## Deploy on Streamlit Cloud

1. Deploy [app.py](C:/Users/user/Desktop/files/projects/it_projects/gsd_codex_test/app.py) as the app entrypoint.
2. Add `GOOGLE_PLACES_API_KEY` to app secrets using [.streamlit/secrets.toml.example](C:/Users/user/Desktop/files/projects/it_projects/gsd_codex_test/.streamlit/secrets.toml.example) as the template.
3. Keep `.env` local only; it is already ignored by [.gitignore](C:/Users/user/Desktop/files/projects/it_projects/gsd_codex_test/.gitignore).

## Notes

- The app stops at startup if no API key is configured.
- Repeated identical searches are cached within the session.
- Bayesian ranking constants currently stay in code in [ranking.py](C:/Users/user/Desktop/files/projects/it_projects/gsd_codex_test/ranking.py).
