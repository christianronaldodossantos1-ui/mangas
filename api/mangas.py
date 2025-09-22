# api/mangas.py
import json
import os
from datetime import datetime, timedelta
from bs4 import BeautifulSoup
import requests

CACHE_FILE = "/tmp/cache.json"
CACHE_DURATION = timedelta(minutes=30)  # Atualiza cache a cada 30 minutos

def handler(request, response):
    # Checa cache
    if os.path.exists(CACHE_FILE):
        with open(CACHE_FILE, "r") as f:
            cache = json.load(f)
        last_update = datetime.fromisoformat(cache["time"])
        if datetime.now() - last_update < CACHE_DURATION:
            return response.json(cache["data"])

    # Faz scraping
    try:
        BASE_URL = "https://animefire.plus/animes/kemonozume-todos-os-episodios"  # Substitua pelo site alvo
        r = requests.get(BASE_URL, timeout=5)
        r.raise_for_status()
        soup = BeautifulSoup(r.text, "html.parser")
        mangas = [item.text.strip() for item in soup.select(".manga-title")]  # Ajuste conforme site

        data = {"mangas": mangas}

        # Salva cache
        with open(CACHE_FILE, "w") as f:
            json.dump({"time": datetime.now().isoformat(), "data": data}, f)

        return response.json(data)

    except requests.exceptions.RequestException as e:
        return response.status(500).json({"error": f"Request failed: {str(e)}"})
    except Exception as e:
        return response.status(500).json({"error": str(e)})