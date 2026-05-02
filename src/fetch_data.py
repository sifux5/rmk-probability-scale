"""
Fetch forest inventory data from Statistics Estonia (stat.ee) API.

The API follows the PX-Web standard. We query:
  - KK51.PX:  forest stock estimates from the National Forest Inventory (SMI), 1999-2024
  - KK513.PX: destroyed forest stands by cause and county, 1991-2024
"""

import json
import requests

BASE_URL = "https://andmed.stat.ee/api/v1/et/stat"
STOCK_TABLE_PATH = "keskkond/loodusvarad-ja-nende-kasutamine/metsavaru/KK51.PX"
DAMAGED_TABLE_PATH = "keskkond/loodusvarad-ja-nende-kasutamine/metsavaru/KK513.PX"


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
        "response": {
            "format": "json"
        }
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
        "response": {
            "format": "json"
        }
    }

    response = requests.post(url, json=query)
    response.raise_for_status()
    return response.json()


if __name__ == "__main__":
    data = fetch_damaged_forest()
    print(json.dumps(data, indent=2, ensure_ascii=False))