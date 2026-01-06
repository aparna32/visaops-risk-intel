import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
from datetime import datetime
from pathlib import Path

st.set_page_config(page_title="VisaOps Risk Console", layout="wide")

st.title("VisaOps Risk Console")
st.caption("Operational stress monitoring + regime labeling + early-warning episodes (synthetic demo data).")


# ---------- Load data ----------
@st.cache_data
def load_signals():
    df = pd.read_csv("data/processed/visaops_signals.csv")
    df["date"] = pd.to_datetime(df["date"])
    return df


@st.cache_data
def load_episodes():
    try:
        ep = pd.read_csv("data/processed/early_warning_episodes.csv")
        ep["stress_start"] = pd.to_datetime(ep["stress_start"])
        ep["warning_start"] = pd.to_datetime(ep["warning_start"])
        return ep
    except FileNotFoundError:
        return None


df = load_signals()
episodes = load_episodes()
centers = sorted(df["center"].unique().tolist())

# ---------- Sidebar ----------
st.sidebar.header("Controls")
center = st.sidebar.selectbox("Center", centers, index=0)

d = df[df["center"] == center].sort_values("date").copy()

# Current status = last row
latest = d.iloc[-1]
regime = str(latest["regime"])
stress = float(latest["stress_index"])
tat = float(latest["avg_tat_days"])
queue = float(latest["queue_size"])
util = float(latest["utilization"])

# ---------- KPIs ----------
k1, k2, k3, k4, k5 = st.columns(5)
k1.metric("Current Regime", regime)
k2.metric("Stress Index", f"{stress:.2f}")
k3.metric("Avg TAT (days)", f"{tat:.2f}")
k4.metric("Queue Size", f"{queue:.0f}")
k5.metric("Utilization", f"{util:.2f}")

st.divider()

# ---------- Helper: latest per center ----------
latest_by_center = (
    df.sort_values("date")
      .groupby("center", as_index=False)
      .tail(1)
      .sort_values("stress_index", ascending=False)
      .reset_index(drop=True)
)

# ---------- Helper: episode summary ----------
def episode_summary(ep: pd.DataFrame) -> pd.DataFrame:
    if ep is None or ep.empty:
        return pd.DataFrame(columns=["center", "episodes", "early_warnings", "detection_rate", "avg_lead_time_days"])

    rows = []
    for c, g in ep.groupby("center"):
        total = len(g)
        detected = g["lead_time_days"].notna().sum()
        rate = detected / total if total else 0.0
        avg_lead = g["lead_time_days"].mean()
        rows.append(
            {
                "center": c,
                "episodes": total,
                "early_warnings": int(detected),
                "detection_rate": round(rate, 2),
                "avg_lead_time_days": round(avg_lead, 2) if detected > 0 else None,
            }
        )
    return pd.DataFrame(rows).sort_values("center").reset_index(drop=True)


ep_summary = episode_summary(episodes)

# ---------- Report builders ----------
def build_status_report_csv() -> str:
    rep = latest_by_center[["center", "regime", "stress_index", "avg_tat_days", "queue_size", "utilization"]].copy()
    rep["generated_at_utc"] = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")
    return rep.to_csv(index=False)


def build_memo_markdown(selected_center: str) -> str:
    dsel = df[df["center"] == selected_center].sort_values("date")
    last = dsel.iloc[-1]

    ep_c = None
    if episodes is not None:
        ep_c = episodes[episodes["center"] == selected_center].sort_values("stress_start")

    lines = []
    lines.append(f"# VisaOps Risk Memo — {selected_center}")
    lines.append("")
    lines.append(f"Generated (UTC): **{datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')}**")
    lines.append("")
    lines.append("## Current Status")
    lines.append(f"- Regime: **{last['regime']}**")
    lines.append(f"- Stress Index: **{float(last['stress_index']):.2f}**")
    lines.append(f"- Avg TAT (days): **{float(last['avg_tat_days']):.2f}**")
    lines.append(f"- Queue Size: **{float(last['queue_size']):.0f}**")
    lines.append(f"- Utilization: **{float(last['utilization']):.2f}**")
    lines.append("")
    lines.append("## Top Risk Centers (latest day)")
    lines.append("")
    top5 = latest_by_center.head(5)[["center", "regime", "stress_index", "avg_tat_days", "queue_size", "utilization"]]
    lines.append(top5.to_markdown(index=False))
    lines.append("")

    lines.append("## Early Warning Performance")
    if episodes is None or episodes.empty:
        lines.append("_No early-warning episodes file found. Run `python src/early_warning.py`._")
    else:
        lines.append("### Summary by Center")
        lines.append(ep_summary.to_markdown(index=False))
        lines.append("")
        lines.append("### Episodes for Selected Center")
        if ep_c is None or ep_c.empty:
            lines.append("_No stressed episodes detected for this center._")
        else:
            show_cols = ["stress_start", "warning_start", "lead_time_days"]
            lines.append(ep_c[show_cols].to_markdown(index=False))

    lines.append("")
    lines.append("## Notes")
    lines.append("- This demo uses synthetic, non-sensitive operational data.")
    lines.append("- Stress Index is a weighted combination of utilization, backlog velocity, and TAT volatility (center-normalized).")
    lines.append("- Regimes are rule-based thresholds on Stress Index (stable/elevated/stressed).")
    return "\n".join(lines)


def get_latest_pdf():
    reports_dir = Path("reports")
    if not reports_dir.exists():
        return None
    pdfs = sorted(
        reports_dir.glob("visaops_report_*.pdf"),
        key=lambda p: p.stat().st_mtime,
        reverse=True,
    )
    return pdfs[0] if pdfs else None


# ---------- Tabs ----------
tab1, tab2, tab3, tab4 = st.tabs(["Monitor", "Early Warning", "Data", "Export"])

with tab1:
    st.subheader("Top Risk Centers (latest day)")
    st.dataframe(
        latest_by_center[["center", "regime", "stress_index", "avg_tat_days", "queue_size", "utilization"]],
        use_container_width=True,
    )

    st.subheader(f"Stress + Regime Timeline — {center}")

    fig, ax = plt.subplots()
    ax.plot(d["date"], d["stress_index"], label="Stress Index")
    ax.axhline(0, linestyle="--", linewidth=1)

    regime_colors = {"stable": "#d4f4dd", "elevated": "#fff3cd", "stressed": "#f8d7da"}
    ymin = float(d["stress_index"].min())
    ymax = float(d["stress_index"].max())

    for reg, col in regime_colors.items():
        mask = (d["regime"] == reg).to_numpy()
        ax.fill_between(d["date"], ymin, ymax, where=mask, color=col, alpha=0.35, label=reg)

    ax.set_title(f"Operational Stress & Regimes – {center}")
    ax.set_xlabel("Date")
    ax.set_ylabel("Stress Index")
    ax.tick_params(axis="x", rotation=30)
    ax.legend(loc="upper left")
    fig.tight_layout()
    st.pyplot(fig, clear_figure=True)

    st.write("Regime counts (this center):")
    st.dataframe(
        d["regime"].value_counts().rename_axis("regime").reset_index(name="days"),
        use_container_width=True,
    )

with tab2:
    st.subheader("Early Warning Episodes")

    if episodes is None:
        st.warning("No early warning episodes file found yet. Run: python src/early_warning.py")
    else:
        ep_c = episodes[episodes["center"] == center].sort_values("stress_start").copy()
        st.write("Episodes for selected center:")
        st.dataframe(ep_c, use_container_width=True)

        total = len(ep_c)
        detected = ep_c["lead_time_days"].notna().sum() if total > 0 else 0
        rate = (detected / total) if total > 0 else 0.0
        avg_lead = ep_c["lead_time_days"].mean()

        c1, c2, c3 = st.columns(3)
        c1.metric("Episodes", f"{total}")
        c2.metric("Detection Rate", f"{rate:.2f}")
        c3.metric("Avg Lead Time (days)", f"{avg_lead:.2f}" if pd.notna(avg_lead) else "—")

        st.subheader("Summary by center")
        st.dataframe(ep_summary, use_container_width=True)

with tab3:
    st.subheader("Signals (latest rows)")
    st.dataframe(d.tail(30), use_container_width=True)

    st.subheader("Columns")
    st.write(list(d.columns))

with tab4:
    st.subheader("Export Reports")

    st.write("### Download latest status snapshot (CSV)")
    st.download_button(
        label="Download status_report.csv",
        data=build_status_report_csv().encode("utf-8"),
        file_name="status_report.csv",
        mime="text/csv",
    )

    st.write("### Download memo (Markdown)")
    memo_md = build_memo_markdown(center)
    st.download_button(
        label=f"Download memo_{center}.md",
        data=memo_md.encode("utf-8"),
        file_name=f"memo_{center}.md",
        mime="text/markdown",
    )

    st.write("### Download latest PDF report")
    latest_pdf = get_latest_pdf()
    if latest_pdf is None:
        st.warning("No PDF report found. Generate one by running: python src/report_generator.py")
    else:
        with open(latest_pdf, "rb") as f:
            st.download_button(
                label=f"Download {latest_pdf.name}",
                data=f.read(),
                file_name=latest_pdf.name,
                mime="application/pdf",
            )

    st.info("Tip: Put exported memos and generated reports in the `reports/` folder for clean versioning.")
