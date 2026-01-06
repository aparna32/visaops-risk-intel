# VisaOps Risk Memo — Bengaluru

Generated (UTC): **2026-01-06 07:10:36**

## Current Status
- Regime: **stable**
- Stress Index: **-0.74**
- Avg TAT (days): **2.97**
- Queue Size: **0**
- Utilization: **0.73**

## Top Risk Centers (latest day)

| center    | regime   |   stress_index |   avg_tat_days |   queue_size |   utilization |
|:----------|:---------|---------------:|---------------:|-------------:|--------------:|
| Delhi     | elevated |       0.182425 |           3.2  |            0 |      0.691802 |
| Mumbai    | stable   |      -0.532753 |           3.07 |            0 |      0.776827 |
| Bengaluru | stable   |      -0.74157  |           2.97 |            0 |      0.726951 |

## Early Warning Performance
### Summary by Center
| center    |   episodes |   early_warnings |   detection_rate |   avg_lead_time_days |
|:----------|-----------:|-----------------:|-----------------:|---------------------:|
| Bengaluru |          1 |                0 |             0    |                  nan |
| Delhi     |          1 |                1 |             1    |                    2 |
| Mumbai    |          4 |                1 |             0.25 |                    1 |

### Episodes for Selected Center
| stress_start        | warning_start   |   lead_time_days |
|:--------------------|:----------------|-----------------:|
| 2024-01-24 00:00:00 | NaT             |              nan |

## Notes
- This demo uses synthetic, non-sensitive operational data.
- Stress Index is a weighted combination of utilization, backlog velocity, and TAT volatility (center-normalized).
- Regimes are rule-based thresholds on Stress Index (stable/elevated/stressed).