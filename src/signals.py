"""
Signal engineering for visa ops daily snapshots.

Reads:  data/processed/visaops_daily.csv
Writes: data/processed/visaops_signals.csv
"""

from __future__ import annotations

import pandas as pd


def add_signals(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()

    # Parse and sort
    df["date"] = pd.to_datetime(df["date"])
    df = df.sort_values(["center", "date"])

    g = df.groupby("center", group_keys=False)

    # -------------------------------------------------
    # Base operational signals
    # -------------------------------------------------

    # Utilization proxy (system load)
    df["utilization"] = (df["processed_apps"] / df["capacity_apps"]).clip(0, 1.5)

    # Queue velocity (backlog change)
    df["queue_delta"] = g["queue_size"].diff().fillna(0.0)

    # -------------------------------------------------
    # Rolling weak signals
    # -------------------------------------------------

    for w in (7, 14):
        df[f"tat_mean_{w}d"] = (
            g["avg_tat_days"]
            .rolling(w, min_periods=3)
            .mean()
            .reset_index(level=0, drop=True)
        )

        df[f"tat_std_{w}d"] = (
            g["avg_tat_days"]
            .rolling(w, min_periods=3)
            .std()
            .reset_index(level=0, drop=True)
        )

        df[f"queue_mean_{w}d"] = (
            g["queue_size"]
            .rolling(w, min_periods=3)
            .mean()
            .reset_index(level=0, drop=True)
        )

        df[f"queue_vel_mean_{w}d"] = (
            g["queue_delta"]
            .rolling(w, min_periods=3)
            .mean()
            .reset_index(level=0, drop=True)
        )

        df[f"util_mean_{w}d"] = (
            g["utilization"]
            .rolling(w, min_periods=3)
            .mean()
            .reset_index(level=0, drop=True)
        )

    # Fill early rolling-window NaNs
    df = df.bfill().ffill()

    # -------------------------------------------------
    # Composite Stress Index
    # -------------------------------------------------

    # Normalize components within each center (z-score)
    for col in ["utilization", "queue_vel_mean_7d", "tat_std_7d"]:
        mean = g[col].transform("mean")
        std = g[col].transform("std").replace(0, 1.0)
        df[f"{col}_z"] = (df[col] - mean) / std

    # Interpretable weighted stress index
    df["stress_index"] = (
        0.5 * df["utilization_z"]
        + 0.3 * df["queue_vel_mean_7d_z"]
        + 0.2 * df["tat_std_7d_z"]
    )

    # -------------------------------------------------
    # Simple Regime Labels
    # -------------------------------------------------

    def label_regime(x: float) -> str:
        if x < -0.5:
            return "stable"
        elif x < 0.75:
            return "elevated"
        else:
            return "stressed"

    df["regime"] = df["stress_index"].apply(label_regime)

    return df


def main() -> None:
    inp = "data/processed/visaops_daily.csv"
    outp = "data/processed/visaops_signals.csv"

    df = pd.read_csv(inp)
    feats = add_signals(df)
    feats.to_csv(outp, index=False)

    print(f"Saved {len(feats)} rows -> {outp}")
    print(
        feats[
            [
                "date",
                "center",
                "avg_tat_days",
                "queue_size",
                "utilization",
                "stress_index",
                "regime",
            ]
        ]
        .head(10)
        .to_string(index=False)
    )


if __name__ == "__main__":
    main()
