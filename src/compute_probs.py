"""
Compute probabilities for the Estonian forest and population probability scale.

Data sources: Statistics Estonia (stat.ee)
  - KK51.PX:  forest area by tree species, National Forest Inventory, 1999-2024
  - KK513.PX: destroyed forest stands by cause, 1991-2024
  - RV104.PX: births by multiplicity (single, twins, triplets), 1922-2024
  - RV40.PX:  deaths by month, 1927-2024

All probabilities are derived programmatically from the fetched data.
"""

import pandas as pd
from fetch_data import fetch_forest_stock, fetch_damaged_forest, fetch_births, fetch_deaths

ESTONIA_TOTAL_AREA_KHA = 4522.0  # Estonia total land area in thousand hectares
ESTONIA_POPULATION = 1_374_687   # Estonia population, 2024 census


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


def parse_births(raw: dict) -> pd.DataFrame:
    """
    Parse the raw RV104.PX response into a DataFrame.
    Rows = years, columns = indicator codes (1=kokku, 3=kaksikud).
    """
    records = []
    for entry in raw["data"]:
        year, indicator = entry["key"]
        raw_value = entry["values"][0]
        value = 0.0 if raw_value == ".." else float(raw_value)
        records.append({"indicator": int(indicator), "year": int(year), "count": value})

    df = pd.DataFrame(records)
    return df.pivot(index="year", columns="indicator", values="count")


def parse_deaths(raw: dict) -> pd.DataFrame:
    """
    Parse the raw RV40.PX response into a DataFrame.
    Rows = years, column = annual death count.
    """
    records = []
    for entry in raw["data"]:
        year, _month = entry["key"]
        value = float(entry["values"][0])
        records.append({"year": int(year), "deaths": value})

    return pd.DataFrame(records).set_index("year")


def compute_probabilities(
    stock_df: pd.DataFrame,
    damaged_df: pd.DataFrame,
    births_df: pd.DataFrame,
    deaths_df: pd.DataFrame,
) -> list[dict]:
    """
    Compute a list of events with their probabilities.

    Uses 2024 data where available. Fire damage uses a 10-year average
    (2015-2024) to smooth out year-to-year variation.

    Returns a list of dicts with keys: event, probability, source.
    """
    latest_stock = stock_df.loc[2024]
    total_forest_kha = latest_stock[1]
    conifer_kha = latest_stock[3] + latest_stock[4]
    birch_kha = latest_stock[5]
    aspen_kha = latest_stock[6]

    fire_avg_ha = damaged_df.loc[2015:2024, 7].mean()
    total_forest_ha = total_forest_kha * 1000
    fire_prob = fire_avg_ha / total_forest_ha

    total_births_2024 = births_df.loc[2024, 1]
    twin_births_2024 = births_df.loc[2024, 3]
    twin_prob = (twin_births_2024 * 2) / total_births_2024

    deaths_2024 = deaths_df.loc[2024, "deaths"]
    death_prob = deaths_2024 / ESTONIA_POPULATION

    return [
        {
            "event": "Juhuslik Eesti hektar on metsamaa",
            "probability": round(total_forest_kha / ESTONIA_TOTAL_AREA_KHA, 4),
            "source": "Statistikaamet KK51.PX, 2024"
        },
        {
            "event": "Juhuslik metsahektar on männik või kuusik",
            "probability": round(conifer_kha / total_forest_kha, 4),
            "source": "Statistikaamet KK51.PX, 2024"
        },
        {
            "event": "Juhuslik metsahektar on kaasik",
            "probability": round(birch_kha / total_forest_kha, 4),
            "source": "Statistikaamet KK51.PX, 2024"
        },
        {
            "event": "Juhuslik eestlane suri sel aastal",
            "probability": round(death_prob, 4),
            "source": "Statistikaamet RV40.PX, 2024"
        },
        {
            "event": "Juhuslik metsahektar on haavikut",
            "probability": round(aspen_kha / total_forest_kha, 4),
            "source": "Statistikaamet KK51.PX, 2024"
        },
        {
            "event": "Juhuslik sünd on kaksikud",
            "probability": round(twin_prob, 4),
            "source": "Statistikaamet RV104.PX, 2024"
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
    births_raw = fetch_births()
    deaths_raw = fetch_deaths()

    stock_df = parse_forest_stock(stock_raw)
    damaged_df = parse_damaged_forest(damaged_raw)
    births_df = parse_births(births_raw)
    deaths_df = parse_deaths(deaths_raw)

    probs = compute_probabilities(stock_df, damaged_df, births_df, deaths_df)

    for p in probs:
        print(f"{p['probability']:.6f}  {p['event']}")