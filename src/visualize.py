"""
Visualize the Estonian forest and population probability scale.

Produces a horizontal log-scale chart saved to output/probability_scale.png.
"""

import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import sys
import os

sys.path.insert(0, os.path.dirname(__file__))

from compute_probs import (
    compute_probabilities,
    parse_forest_stock,
    parse_damaged_forest,
    parse_births,
    parse_deaths,
)
from fetch_data import fetch_forest_stock, fetch_damaged_forest, fetch_births, fetch_deaths

OUTPUT_PATH = "output/probability_scale.png"


def plot_probability_scale(probs: list[dict]) -> None:
    """
    Draw a horizontal log-scale probability chart and save to OUTPUT_PATH.
    Events are sorted by probability descending.
    """
    probs_sorted = sorted(probs, key=lambda p: p["probability"], reverse=True)

    labels = [p["event"] for p in probs_sorted]
    values = [p["probability"] for p in probs_sorted]

    fig, ax = plt.subplots(figsize=(13, 6))

    green_shades = [
        "#1b4332", "#2d6a4f", "#40916c",
        "#52b788", "#74c69d", "#95d5b2", "#b7e4c7"
    ]

    y_positions = list(range(len(labels)))
    bars = ax.barh(y_positions, values, color=green_shades[:len(labels)], height=0.6)

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

    ax.set_xlabel("Tõenäosus (logaritmiline skaala)", fontsize=12)
    ax.set_title("Eesti tõenäosusskaala", fontsize=15, fontweight="bold", pad=15)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.grid(axis="x", linestyle="--", alpha=0.4)

    plt.tight_layout()
    plt.savefig(OUTPUT_PATH, dpi=150, bbox_inches="tight")
    print(f"Graafik salvestatud: {OUTPUT_PATH}")


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
    plot_probability_scale(probs)