"""
Visualize operational stress with regime shading for one center.
"""

import pandas as pd
import matplotlib.pyplot as plt


def main():
    df = pd.read_csv("data/processed/visaops_signals.csv")
    df["date"] = pd.to_datetime(df["date"])

    center = "Delhi"
    d = df[df["center"] == center].sort_values("date")

    plt.figure()

    # Plot stress index
    plt.plot(d["date"], d["stress_index"], label="Stress Index")

    # Shade regimes
    for regime, color in [
        ("stable", "#d4f4dd"),
        ("elevated", "#fff3cd"),
        ("stressed", "#f8d7da"),
    ]:
        mask = d["regime"] == regime
        plt.fill_between(
            d["date"],
            d["stress_index"].min(),
            d["stress_index"].max(),
            where=mask,
            color=color,
            alpha=0.4,
            label=regime if regime not in plt.gca().get_legend_handles_labels()[1] else None,
        )

    plt.axhline(0, linestyle="--", linewidth=1)
    plt.title(f"Operational Stress & Regimes – {center}")
    plt.xlabel("Date")
    plt.ylabel("Stress Index")
    plt.xticks(rotation=30)
    plt.legend()
    plt.tight_layout()

    out_path = "data/processed/stress_regimes_delhi.png"
    plt.savefig(out_path)
    plt.close()

    print(f"Saved plot -> {out_path}")


if __name__ == "__main__":
    main()
