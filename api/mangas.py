from bs4 import BeautifulSoup
import requests

def handler(request, response):
    BASE_URL = "https://mangaonline.blog"  # Substitua pelo site alvo
    try:
        r = requests.get(BASE_URL, timeout=5)
        r.raise_for_status()
        soup = BeautifulSoup(r.text, "html.parser")

        mangas = [item.text.strip() for item in soup.select(".manga-title")]  # ajuste conforme site
        return response.json({"mangas": mangas})

    except requests.exceptions.RequestException as e:
        return response.status(500).json({"error": f"Request failed: {str(e)}"})
    except Exception as e:
        return response.status(500).json({"error": str(e)})