"""
Compute probabilities for the Estonian forest probability scale.

Data source: Statistics Estonia (stat.ee)
  - KK51.PX:  forest area by tree species, National Forest Inventory, 1999-2024
  - KK513.PX: destroyed forest stands by cause, 1991-2024

All probabilities are derived programmatically from the fetched data.
"""

import pandas as pd
from fetch_data import fetch_forest_stock, fetch_damaged_forest

ESTONIA_TOTAL_AREA_KHA = 4522.0  # Estonia total land area in thousand hectares


def parse_forest_stock(raw: dict) -> pd.DataFrame:
    """
    Parse the raw KK51.PX response into a DataFrame.
    Rows = years, columns = indicator codes (1-9).
    """
    records = []
    for entry in raw["data"]:
        indicator, year = entry["key"]
        value = float(entry["values"][0])
        records.append({"indicator": int(indicator), "year": int(year), "area_kha": value})

    df = pd.DataFrame(records)
    return df.pivot(index="year", columns="indicator", values="area_kha")


def parse_damaged_forest(raw: dict) -> pd.DataFrame:
    """
    Parse the raw KK513.PX response into a DataFrame.
    Rows = years, columns = cause codes (1=kokku, 7=tulekahjud).
    Missing values ('..') are treated as 0.
    """
    records = []
    for entry in raw["data"]:
        _county, year, cause = entry["key"]
        raw_value = entry["values"][0]
        value = 0.0 if raw_value == ".." else float(raw_value)
        records.append({"cause": int(cause), "year": int(year), "area_ha": value})

    df = pd.DataFrame(records)
    return df.pivot(index="year", columns="cause", values="area_ha")


def compute_probabilities(stock_df: pd.DataFrame, damaged_df: pd.DataFrame) -> list[dict]:
    """
    Compute a list of events with their probabilities.
    Uses 2024 data for forest stock, and a 10-year average (2015-2024) for fire damage.
    Returns a list of dicts with keys: event, probability, source.
    """
    latest = stock_df.loc[2024]

    total_forest_kha = latest[1]         # kogu metsamaa
    conifer_kha = latest[3] + latest[4]  # männik + kuusik
    birch_kha = latest[5]                # kaasik
    aspen_kha = latest[6]                # haab

    # Average annual fire damage over last 10 years (in ha)
    fire_avg_ha = damaged_df.loc[2015:2024, 7].mean()
    total_forest_ha = total_forest_kha * 1000
    fire_prob = fire_avg_ha / total_forest_ha

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
        {
            "event": "Juhuslik metsahektar hukkub tulekahjus sel aastal",
            "probability": round(fire_prob, 6),
            "source": "Statistikaamet KK513.PX, keskmine 2015-2024"
        },
    ]


if __name__ == "__main__":
    stock_raw = fetch_forest_stock()
    damaged_raw = fetch_damaged_forest()

    stock_df = parse_forest_stock(stock_raw)
    damaged_df = parse_damaged_forest(damaged_raw)

    probs = compute_probabilities(stock_df, damaged_df)

    for p in probs:
        print(f"{p['probability']:.6f}  {p['event']}")