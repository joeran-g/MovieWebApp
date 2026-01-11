import os
import requests
from dotenv import load_dotenv

load_dotenv()

OMDB_API_KEY = os.getenv("OMDB_API_KEY")

if not OMDB_API_KEY:
    raise RuntimeError("OMDB_API_KEY is not set")


def fetch_movie_data(title):
    response = requests.get(
        "http://www.omdbapi.com/",
        params={
            "apikey": OMDB_API_KEY,
            "t": title
        }
    )

    data = response.json()

    if data.get("Response") == "False":
        return None

    return {
        "title": data.get("Title"),
        "director": data.get("Director"),
        "year": int(data.get("Year")),
        "poster_url": data.get("Poster")
    }