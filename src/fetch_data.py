"""
Fetch forest inventory data from Statistics Estonia (stat.ee) API.

The API follows the PX-Web standard. We query table KK51.PX which contains
forest stock estimates from the National Forest Inventory (SMI), 1999-2024.
"""

import json
import requests
import pandas as pd

BASE_URL = "https://andmed.stat.ee/api/v1/et/stat"
TABLE_PATH = "keskkond/loodusvarad-ja-nende-kasutamine/metsavaru/KK51.PX"


def fetch_forest_stock() -> dict:
    """
    Fetch forest area by tree species from the Statistics Estonia API.
    Returns the raw API response as a dict.
    """
    url = f"{BASE_URL}/{TABLE_PATH}"

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


if __name__ == "__main__":
    data = fetch_forest_stock()
    print(json.dumps(data, indent=2, ensure_ascii=False))