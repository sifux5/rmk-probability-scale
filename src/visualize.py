"""
Visualize the Estonian probability scale.

Produces a horizontal log-scale chart saved to output/probability_scale.png.
Forest events are shown in green, population events in blue.
"""

import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import matplotlib.patches as mpatches
import sys
import os

sys.path.insert(0, os.path.dirname(__file__))

from compute_probs import (
    compute_probabilities,
    parse_forest_stock,
    parse_damaged_forest,
    parse_births,
    parse_deaths,
    parse_divorces,
    parse_marriages,
)
from fetch_data import (
    fetch_forest_stock,
    fetch_damaged_forest,
    fetch_births,
    fetch_deaths,
    fetch_divorces,
    fetch_marriages,
    save_raw,
)

OUTPUT_PATH = "output/probability_scale.png"

FOREST_COLOR = "#2d6a4f"
POPULATION_COLOR = "#1d3557"


def plot_probability_scale(probs: list[dict]) -> None:
    """
    Draw a horizontal log-scale probability chart and save to OUTPUT_PATH.
    Events are sorted by probability descending.
    Forest and population events are colored differently.
    """
    probs_sorted = sorted(probs, key=lambda p: p["probability"], reverse=True)

    labels = [p["event"] for p in probs_sorted]
    values = [p["probability"] for p in probs_sorted]
    colors = [
        FOREST_COLOR if p["category"] == "forest" else POPULATION_COLOR
        for p in probs_sorted
    ]

    fig, ax = plt.subplots(figsize=(14, 7))

    y_positions = list(range(len(labels)))
    bars = ax.barh(y_positions, values, color=colors, height=0.6)

    ax.set_xscale("log")
    ax.set_xlim(0.00005, 2.0)
    ax.xaxis.set_major_formatter(ticker.FuncFormatter(
        lambda x, _: f"{x:.0%}" if x >= 0.01 else f"{x:.5f}"
    ))

    ax.set_yticks(y_positions)
    ax.set_yticklabels(labels, fontsize=11)
    ax.invert_yaxis()

    for bar, val in zip(bars, values):
        ax.text(
            val * 1.4, bar.get_y() + bar.get_height() / 2,
            f"{val:.4f}" if val >= 0.001 else f"{val:.6f}",
            va="center", ha="left", fontsize=10, color="#1b4332"
        )

    forest_patch = mpatches.Patch(color=FOREST_COLOR, label="Forest")
    population_patch = mpatches.Patch(color=POPULATION_COLOR, label="Population")
    ax.legend(handles=[forest_patch, population_patch], fontsize=11, loc="lower right")

    ax.set_xlabel("Probability (log scale)", fontsize=12)
    ax.set_title("Estonian Probability Scale", fontsize=15, fontweight="bold", pad=15)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.grid(axis="x", linestyle="--", alpha=0.4)

    plt.tight_layout()
    plt.savefig(OUTPUT_PATH, dpi=150, bbox_inches="tight")
    print(f"Chart saved to: {OUTPUT_PATH}")


if __name__ == "__main__":
    stock_raw = fetch_forest_stock()
    save_raw("forest_stock", stock_raw)

    damaged_raw = fetch_damaged_forest()
    save_raw("damaged_forest", damaged_raw)

    births_raw = fetch_births()
    save_raw("births", births_raw)

    deaths_raw = fetch_deaths()
    save_raw("deaths", deaths_raw)

    divorces_raw = fetch_divorces()
    save_raw("divorces", divorces_raw)

    marriages_raw = fetch_marriages()
    save_raw("marriages", marriages_raw)

    stock_df = parse_forest_stock(stock_raw)
    damaged_df = parse_damaged_forest(damaged_raw)
    births_df = parse_births(births_raw)
    deaths_df = parse_deaths(deaths_raw)
    divorces_df = parse_divorces(divorces_raw)
    marriages_df = parse_marriages(marriages_raw)

    probs = compute_probabilities(
        stock_df, damaged_df, births_df, deaths_df, divorces_df, marriages_df
    )
    plot_probability_scale(probs)