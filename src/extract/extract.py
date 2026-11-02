
import requests
import json
import time
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor

# Project paths
PROJECT_ROOT = Path(__file__).resolve().parents[2]
RAW_PATH = PROJECT_ROOT / "data" / "raw"
RAW_PATH.mkdir(parents=True, exist_ok=True)

BASE_URL = "https://pokeapi.co/api/v2"


def fetch_data(resource, pokemon_id):
    url = f"{BASE_URL}/{resource}/{pokemon_id}/"

    for attempt in range(3):
        try:
            response = requests.get(url, timeout=20)
            response.raise_for_status()
            return response.json()
        except requests.RequestException:
            if attempt == 2:
                raise
            time.sleep(2 * (attempt + 1))


def extract(resource):
    with ThreadPoolExecutor(max_workers=4) as pool:
        return list(
            pool.map(
                lambda i: fetch_data(resource, i),
                range(1, 494)
            )
        )


# Extract Gen 1 and Gen 2
pokemon = (extract("pokemon")) # battle performance
species = (extract("pokemon-species")) # identity and classification


# Save raw JSON
for filename, data in [
    ("pokemon.json", pokemon),
    ("species.json", species)
]:
    with open(RAW_PATH / filename, "w") as f:
        json.dump(data, f, indent=2)

print(f"Pokemon extracted: {len(pokemon)}")
print(f"Species extracted: {len(species)}")
print(f"Saved to: {RAW_PATH}")

