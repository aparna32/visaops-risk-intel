from __future__ import annotations
import pandas as pd
import numpy as np

"""
Synthetic data generator for visa operations (daily snapshots).

Creates a small, non-sensitive dataset for development/testing:
date, center, demand_apps, capacity_apps, processed_apps, queue_size, avg_tat_days
"""




def generate_daily_ops(
    start_date: str = "2024-01-01",
    days: int = 30,
    centers: tuple[str, ...] = ("Delhi", "Mumbai", "Bengaluru"),
    seed: int = 42,
) -> pd.DataFrame:
    rng = np.random.default_rng(seed)
    dates = pd.date_range(start_date, periods=days, freq="D")

    rows = []
    for center in centers:
        queue = 0.0
        base_demand = float(rng.integers(200, 320))
        base_capacity = float(rng.integers(220, 340))

        for d in dates:
            demand = max(50.0, base_demand + rng.normal(0, 25))
            capacity = max(50.0, base_capacity + rng.normal(0, 20))

            processed = min(demand + queue, capacity)
            queue = max(0.0, queue + demand - processed)

            # simple TAT relationship: grows with queue
            avg_tat = max(1.0, 3.0 + 0.015 * queue + rng.normal(0, 0.3))

            rows.append(
                {
                    "date": d.date().isoformat(),
                    "center": center,
                    "demand_apps": round(demand, 2),
                    "capacity_apps": round(capacity, 2),
                    "processed_apps": round(processed, 2),
                    "queue_size": round(queue, 2),
                    "avg_tat_days": round(avg_tat, 2),
                }
            )

    return pd.DataFrame(rows).sort_values(["center", "date"]).reset_index(drop=True)


def main() -> None:
    df = generate_daily_ops()
    out_path = "data/processed/visaops_daily.csv"
    df.to_csv(out_path, index=False)
    print(f"Saved {len(df)} rows -> {out_path}")
    print(df.head(5).to_string(index=False))


if __name__ == "__main__":
    main()