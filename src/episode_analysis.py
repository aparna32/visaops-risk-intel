"""
Episode-level analysis to understand why early warning succeeds or fails.
"""

import pandas as pd


def analyze_episodes(
    df: pd.DataFrame,
    episodes: pd.DataFrame,
    window_days: int = 5,
) -> pd.DataFrame:
    """
    For each stressed episode, compute average signal values
    in the window immediately before stress_start.
    """
    rows = []

    for _, ep in episodes.iterrows():
        center = ep["center"]
        stress_start = ep["stress_start"]

        d = df[
            (df["center"] == center)
            & (df["date"] < stress_start)
            & (df["date"] >= stress_start - pd.Timedelta(days=window_days))
        ]

        if d.empty:
            continue

        rows.append(
            {
                "center": center,
                "stress_start": stress_start,
                "early_warning": pd.notna(ep["lead_time_days"]),
                "utilization_mean_pre": d["utilization"].mean(),
                "queue_vel_mean_pre": d["queue_vel_mean_7d"].mean(),
                "tat_std_mean_pre": d["tat_std_7d"].mean(),
            }
        )

    return pd.DataFrame(rows)


def main() -> None:
    df = pd.read_csv("data/processed/visaops_signals.csv")
    df["date"] = pd.to_datetime(df["date"])

    episodes = pd.read_csv(
        "data/processed/early_warning_episodes.csv",
        parse_dates=["stress_start", "warning_start"],
    )

    analysis = analyze_episodes(df, episodes)

    print("Episode-level signal comparison (pre-stress)")
    print(analysis.to_string(index=False))

    print("\nGrouped averages")
    print(
        analysis.groupby("early_warning")[
            ["utilization_mean_pre", "queue_vel_mean_pre", "tat_std_mean_pre"]
        ]
        .mean()
        .round(3)
        .to_string()
    )


if __name__ == "__main__":
    main()
