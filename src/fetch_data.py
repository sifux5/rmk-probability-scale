"""
Fetch forest and population data from Statistics Estonia (stat.ee) API.

The API follows the PX-Web standard. We query:
  - KK51.PX:  forest area by tree species, National Forest Inventory, 1999-2024
  - KK513.PX: destroyed forest stands by cause, 1991-2024
  - RV104.PX: births by multiplicity (single, twins, etc.), 1922-2024
  - RV40.PX:  deaths by month, 1927-2024
  - RV291.PX: divorces by marriage duration, 1949-2024
  - RV02.PX:  marriages by month and county, 2006-2024
"""

import json
import requests

BASE_URL = "https://andmed.stat.ee/api/v1/et/stat"

STOCK_TABLE_PATH = "keskkond/loodusvarad-ja-nende-kasutamine/metsavaru/KK51.PX"
DAMAGED_TABLE_PATH = "keskkond/loodusvarad-ja-nende-kasutamine/metsavaru/KK513.PX"
BIRTHS_TABLE_PATH = "rahvastik/rahvastikusundmused/sunnid/RV104.PX"
DEATHS_TABLE_PATH = "rahvastik/rahvastikusundmused/surmad/RV40.PX"
DIVORCES_TABLE_PATH = "rahvastik/rahvastikusundmused/abielulahutused/RV291.PX"
MARRIAGES_TABLE_PATH = "rahvastik/rahvastikusundmused/abielud/RV02.PX"


def fetch_forest_stock() -> dict:
    """
    Fetch forest area by tree species from the Statistics Estonia API.
    Returns the raw API response as a dict.
    """
    url = f"{BASE_URL}/{STOCK_TABLE_PATH}"

    query = {
        "query": [
            {
                "code": "Näitaja",
                "selection": {
                    "filter": "item",
                    "values": ["1", "2", "3", "4", "5", "6", "7", "8", "9"]
                }
            },
            {
                "code": "Aasta",
                "selection": {
                    "filter": "all",
                    "values": ["*"]
                }
            }
        ],
        "response": {"format": "json"}
    }

    response = requests.post(url, json=query)
    response.raise_for_status()
    return response.json()


def fetch_damaged_forest() -> dict:
    """
    Fetch data on destroyed forest stands by cause from Statistics Estonia.
    Table KK513.PX: destroyed forest stands by county, 1991-2024.
    Cause codes: 1=Kokku, 7=Tulekahjud
    """
    url = f"{BASE_URL}/{DAMAGED_TABLE_PATH}"

    query = {
        "query": [
            {
                "code": "Maakond",
                "selection": {
                    "filter": "item",
                    "values": ["00"]
                }
            },
            {
                "code": "Hukkumise põhjus",
                "selection": {
                    "filter": "item",
                    "values": ["1", "7"]
                }
            },
            {
                "code": "Aasta",
                "selection": {
                    "filter": "all",
                    "values": ["*"]
                }
            }
        ],
        "response": {"format": "json"}
    }

    response = requests.post(url, json=query)
    response.raise_for_status()
    return response.json()


def fetch_births() -> dict:
    """
    Fetch birth counts by multiplicity (single, twins, triplets).
    Table RV104.PX: number of deliveries and multiple births, 1922-2024.
    Indicator codes: 1=Kokku, 3=kaksikud
    """
    url = f"{BASE_URL}/{BIRTHS_TABLE_PATH}"

    query = {
        "query": [
            {
                "code": "Näitaja",
                "selection": {
                    "filter": "item",
                    "values": ["1", "3"]
                }
            },
            {
                "code": "Aasta",
                "selection": {
                    "filter": "all",
                    "values": ["*"]
                }
            }
        ],
        "response": {"format": "json"}
    }

    response = requests.post(url, json=query)
    response.raise_for_status()
    return response.json()


def fetch_deaths() -> dict:
    """
    Fetch annual death counts from Statistics Estonia.
    Table RV40.PX: deaths by month, 1927-2024.
    Surmakuu=1 means yearly total (Kuud kokku).
    """
    url = f"{BASE_URL}/{DEATHS_TABLE_PATH}"

    query = {
        "query": [
            {
                "code": "Surmakuu",
                "selection": {
                    "filter": "item",
                    "values": ["1"]
                }
            },
            {
                "code": "Aasta",
                "selection": {
                    "filter": "all",
                    "values": ["*"]
                }
            }
        ],
        "response": {"format": "json"}
    }

    response = requests.post(url, json=query)
    response.raise_for_status()
    return response.json()


def fetch_divorces() -> dict:
    """
    Fetch annual divorce counts from Statistics Estonia.
    Table RV291.PX: divorces by marriage duration, 1949-2024.
    Abielu kestus=1 means yearly total (Kokku).
    """
    url = f"{BASE_URL}/{DIVORCES_TABLE_PATH}"

    query = {
        "query": [
            {
                "code": "Abielu kestus",
                "selection": {
                    "filter": "item",
                    "values": ["1"]
                }
            },
            {
                "code": "Aasta",
                "selection": {
                    "filter": "all",
                    "values": ["*"]
                }
            }
        ],
        "response": {"format": "json"}
    }

    response = requests.post(url, json=query)
    response.raise_for_status()
    return response.json()


def fetch_marriages() -> dict:
    """
    Fetch annual marriage counts from Statistics Estonia.
    Table RV02.PX: marriages by month and county, 2006-2024.
    Maakond=00 means all of Estonia, Registreerimiskuu=1 means yearly total.
    """
    url = f"{BASE_URL}/{MARRIAGES_TABLE_PATH}"

    query = {
        "query": [
            {
                "code": "Maakond",
                "selection": {
                    "filter": "item",
                    "values": ["00"]
                }
            },
            {
                "code": "Registreerimiskuu",
                "selection": {
                    "filter": "item",
                    "values": ["1"]
                }
            },
            {
                "code": "Aasta",
                "selection": {
                    "filter": "all",
                    "values": ["*"]
                }
            }
        ],
        "response": {"format": "json"}
    }

    response = requests.post(url, json=query)
    response.raise_for_status()
    return response.json()


if __name__ == "__main__":
    print("--- Divorces ---")
    print(json.dumps(fetch_divorces(), indent=2, ensure_ascii=False)[:500])
    print("--- Marriages ---")
    print(json.dumps(fetch_marriages(), indent=2, ensure_ascii=False)[:500])