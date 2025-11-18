import os
import sys
import requests

DEFAULT_URL = "https://v2.jokeapi.dev/joke/Any?type=single,twopart"

def fetch_joke(url: str):
    try:
        resp = requests.get(url, timeout=10)
        resp.raise_for_status()
    except requests.RequestException as e:
        print(f"Erreur HTTP / réseau: {e}", file=sys.stderr)
        return None

    try:
        data = resp.json()
    except ValueError:
        print("Réponse non-JSON reçue.", file=sys.stderr)
        return None

    if data.get("error"):
        print("L'API a retourné une erreur:", data, file=sys.stderr)
        return None

    if data.get("type") == "single":
        return data.get("joke")
    elif data.get("type") == "twopart":
        return f"{data.get('setup')}\n{data.get('delivery')}"
    else:
        return str(data)

def main():
    url = os.getenv("JOKE_API_URL", DEFAULT_URL)
    print(f"Interrogation de l'API: {url}")
    joke = fetch_joke(url)
    if joke:
        print("\n--- Blague ---\n")
        print(joke)
        print("\n--------------\n")
    else:
        print("Impossible de récupérer une blague.", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
