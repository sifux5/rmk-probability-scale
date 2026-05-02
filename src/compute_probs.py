"""
Compute probabilities for the Estonian forest probability scale.

Data source: Statistics Estonia KK51.PX (National Forest Inventory, 2024)
All probabilities are derived programmatically from the fetched data.
"""

import pandas as pd
from fetch_data import fetch_forest_stock

ESTONIA_TOTAL_AREA_KHA = 4522.0  # Estonia total land area in thousand hectares


def parse_forest_stock(raw: dict) -> pd.DataFrame:
    """
    Parse the raw API response into a DataFrame.
    Rows = years, columns = indicator codes (1-9).
    """
    records = []
    for entry in raw["data"]:
        indicator, year = entry["key"]
        value = float(entry["values"][0])
        records.append({"indicator": int(indicator), "year": int(year), "area_kha": value})

    df = pd.DataFrame(records)
    return df.pivot(index="year", columns="indicator", values="area_kha")


def compute_probabilities(df: pd.DataFrame) -> list[dict]:
    """
    Compute a list of events with their probabilities using 2024 data.
    Returns a list of dicts with keys: event, probability, source.
    """
    latest = df.loc[2024]

    total_forest_kha = latest[1]         # kogu metsamaa
    conifer_kha = latest[3] + latest[4]  # männik + kuusik
    birch_kha = latest[5]                # kaasik
    aspen_kha = latest[6]                # haab

    return [
        {
            "event": "Juhuslik Eesti hektar on metsamaa",
            "probability": round(total_forest_kha / ESTONIA_TOTAL_AREA_KHA, 3),
            "source": "Statistikaamet KK51.PX, 2024"
        },
        {
            "event": "Juhuslik metsahektar on männik või kuusik",
            "probability": round(conifer_kha / total_forest_kha, 3),
            "source": "Statistikaamet KK51.PX, 2024"
        },
        {
            "event": "Juhuslik metsahektar on kaasik",
            "probability": round(birch_kha / total_forest_kha, 3),
            "source": "Statistikaamet KK51.PX, 2024"
        },
        {
            "event": "Juhuslik metsahektar on haavikut",
            "probability": round(aspen_kha / total_forest_kha, 3),
            "source": "Statistikaamet KK51.PX, 2024"
        },
    ]


if __name__ == "__main__":
    raw = fetch_forest_stock()
    df = parse_forest_stock(raw)
    probs = compute_probabilities(df)

    for p in probs:
        print(f"{p['probability']:.3f}  {p['event']}")