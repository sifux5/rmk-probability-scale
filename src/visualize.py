"""
Visualize the Estonian forest probability scale.

Produces a horizontal log-scale chart saved to output/probability_scale.png.
"""

import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import numpy as np
import sys
import os

sys.path.insert(0, os.path.dirname(__file__))

from compute_probs import compute_probabilities, parse_forest_stock, parse_damaged_forest
from fetch_data import fetch_forest_stock, fetch_damaged_forest

OUTPUT_PATH = "output/probability_scale.png"


def plot_probability_scale(probs: list[dict]) -> None:
    """
    Draw a horizontal log-scale probability chart and save to OUTPUT_PATH.
    """
    labels = [p["event"] for p in probs]
    values = [p["probability"] for p in probs]

    fig, ax = plt.subplots(figsize=(12, 5))

    colors = ["#2d6a4f", "#40916c", "#52b788", "#74c69d", "#b7e4c7"]

    y_positions = range(len(labels))
    bars = ax.barh(list(y_positions), values, color=colors, height=0.6)

    ax.set_xscale("log")
    ax.set_xlim(0.00001, 1.5)
    ax.xaxis.set_major_formatter(ticker.FuncFormatter(
        lambda x, _: f"{x:.0%}" if x >= 0.01 else f"{x:.4f}"
    ))

    ax.set_yticks(list(y_positions))
    ax.set_yticklabels(labels, fontsize=11)
    ax.invert_yaxis()

    for bar, val in zip(bars, values):
        ax.text(
            val * 1.3, bar.get_y() + bar.get_height() / 2,
            f"{val:.4f}",
            va="center", ha="left", fontsize=10, color="#1b4332"
        )

    ax.set_xlabel("Tõenäosus (logaritmiline skaala)", fontsize=12)
    ax.set_title("Eesti metsa tõenäosusskaala", fontsize=15, fontweight="bold", pad=15)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.grid(axis="x", linestyle="--", alpha=0.4)

    plt.tight_layout()
    plt.savefig(OUTPUT_PATH, dpi=150, bbox_inches="tight")
    print(f"Graafik salvestatud: {OUTPUT_PATH}")


if __name__ == "__main__":
    stock_raw = fetch_forest_stock()
    damaged_raw = fetch_damaged_forest()

    stock_df = parse_forest_stock(stock_raw)
    damaged_df = parse_damaged_forest(damaged_raw)

    probs = compute_probabilities(stock_df, damaged_df)
    plot_probability_scale(probs)