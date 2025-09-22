# api/mangas.py
from bs4 import BeautifulSoup
import requests

def handler(request, response):
    BASE_URL = "https://mangadex.org"  # Substitua pelo site alvo
    try:
        r = requests.get(BASE_URL, timeout=5)  # timeout evita crash
        r.raise_for_status()
        soup = BeautifulSoup(r.text, "html.parser")

        mangas = []
        for item in soup.select(".manga-title"):
            mangas.append(item.text.strip())

        if not mangas:
            mangas = ["Nenhum mangá encontrado, verifique o seletor CSS."]

        return response.json({"mangas": mangas})

    except requests.exceptions.Timeout:
        return response.status(504).json({"error": "O site demorou para responder (timeout)."})
    except requests.exceptions.RequestException as e:
        return response.status(500).json({"error": f"Erro na requisição: {str(e)}"})
    except Exception as e:
        return response.status(500).json({"error": f"Erro interno: {str(e)}"})