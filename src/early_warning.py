"""
Early-warning analysis for operational stress.

Computes lead time between early stress signals and entry into
the 'stressed' operational regime, across all centers, and prints
a per-center summary of detection performance.
"""

import pandas as pd


def compute_lead_times(
    df: pd.DataFrame,
    center: str,
    stress_threshold: float = 0.3,
    regime_label: str = "stressed",
) -> pd.DataFrame:
    """
    For each stressed episode, compute how many days earlier the stress index
    crossed a warning threshold.

    A "stressed episode" starts when regime switches into `regime_label`.
    The warning_start is detected by scanning backward from stress_start
    while stress_index >= stress_threshold remains continuously true.
    """
    d = df[df["center"] == center].sort_values("date").reset_index(drop=True)

    episodes = []
    in_episode = False

    for i in range(len(d)):
        # Detect start of stressed regime
        if d.loc[i, "regime"] == regime_label and not in_episode:
            stress_start_date = d.loc[i, "date"]

            # Scan backward for continuous warning crossing
            warn_idx = None
            for j in range(i - 1, -1, -1):
                if d.loc[j, "stress_index"] >= stress_threshold:
                    warn_idx = j
                else:
                    break

            if warn_idx is not None:
                warn_date = d.loc[warn_idx, "date"]
                lead_days = (stress_start_date - warn_date).days
            else:
                warn_date = pd.NaT
                lead_days = float("nan")

            episodes.append(
                {
                    "center": center,
                    "stress_start": stress_start_date,
                    "warning_start": warn_date,
                    "lead_time_days": lead_days,
                }
            )

            in_episode = True

        # Exit stressed regime
        if d.loc[i, "regime"] != regime_label:
            in_episode = False

    return pd.DataFrame(episodes)


def summarize_early_warning(results: pd.DataFrame) -> pd.DataFrame:
    """
    Per-center summary:
    - episodes: number of stressed episodes
    - early_warnings: episodes with a non-null lead time
    - detection_rate: early_warnings / episodes
    - avg_lead_time_days: mean lead time across detected episodes
    """
    summary = []

    for center, g in results.groupby("center"):
        total = len(g)
        detected = g["lead_time_days"].notna().sum()
        detection_rate = detected / total if total > 0 else 0.0
        avg_lead = g["lead_time_days"].mean()

        summary.append(
            {
                "center": center,
                "episodes": total,
                "early_warnings": int(detected),
                "detection_rate": round(detection_rate, 2),
                "avg_lead_time_days": round(avg_lead, 2) if detected > 0 else None,
            }
        )

    return pd.DataFrame(summary).sort_values("center").reset_index(drop=True)


def main() -> None:
    df = pd.read_csv("data/processed/visaops_signals.csv")
    df["date"] = pd.to_datetime(df["date"])

    all_centers = df["center"].unique().tolist()
    all_results = []

    for center in all_centers:
        res = compute_lead_times(
            df,
            center=center,
            stress_threshold=0.3,  # same threshold for all centers (baseline)
        )
        if not res.empty:
            all_results.append(res)

    if not all_results:
        print("No early-warning episodes detected for any center.")
        return

    final = pd.concat(all_results, ignore_index=True)
    final.to_csv("data/processed/early_warning_episodes.csv", index=False)

    print("Early-warning episodes across centers")
    print(final.to_string(index=False))

    print("\nSummary by center")
    summary = summarize_early_warning(final)
    print(summary.to_string(index=False))


if __name__ == "__main__":
    main()
