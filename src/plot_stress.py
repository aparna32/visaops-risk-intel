import os
import argparse
import pandas as pd
import matplotlib

"""
Simple visualization of operational stress over time for one center.

Saves the plot to a PNG file instead of displaying it (headless environment).
"""

matplotlib.use("Agg")  # headless backend
import matplotlib.pyplot as plt
import matplotlib.dates as mdates


def plot_center(df: pd.DataFrame, center: str, out_path: str) -> None:
    if "date" not in df.columns or "center" not in df.columns or "stress_index" not in df.columns:
        raise ValueError("Input CSV must contain 'date', 'center', and 'stress_index' columns.")

    df["date"] = pd.to_datetime(df["date"], errors="coerce")
    d = df[df["center"] == center].dropna(subset=["date"]).sort_values("date")
    if d.empty:
        available = ", ".join(sorted(df["center"].unique()))
        raise ValueError(f"No data for center '{center}'. Available centers: {available}")

    os.makedirs(os.path.dirname(out_path) or ".", exist_ok=True)

    plt.style.use("seaborn-v0_8")
    fig, ax = plt.subplots(figsize=(10, 4.5))
    ax.plot(d["date"], d["stress_index"], marker="o", linestyle="-", linewidth=1)
    ax.axhline(0, linestyle="--", color="gray", linewidth=0.8)
    ax.set_title(f"Operational Stress Index — {center}")
    ax.set_xlabel("Date")
    ax.set_ylabel("Stress Index")

    locator = mdates.AutoDateLocator()
    formatter = mdates.ConciseDateFormatter(locator)
    ax.xaxis.set_major_locator(locator)
    ax.xaxis.set_major_formatter(formatter)
    plt.setp(ax.get_xticklabels(), rotation=30, ha="right")

    fig.tight_layout()
    fig.savefig(out_path, dpi=150, bbox_inches="tight")
    plt.close(fig)


def main():
    parser = argparse.ArgumentParser(description="Plot stress index for a center.")
    parser.add_argument("--center", default="Delhi", help="Center name to plot")
    parser.add_argument("--input", default="data/processed/visaops_signals.csv", help="Input CSV path")
    parser.add_argument("--output", default="data/processed/stress_plot_delhi.png", help="Output PNG path")
    args = parser.parse_args()

    try:
        df = pd.read_csv(args.input)
    except FileNotFoundError:
        raise SystemExit(f"Input file not found: {args.input}")

    try:
        plot_center(df, args.center, args.output)
    except ValueError as e:
        raise SystemExit(str(e))

    print(f"Saved plot -> {args.output}")


if __name__ == "__main__":
    main()