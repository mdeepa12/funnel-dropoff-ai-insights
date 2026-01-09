import os
import pandas as pd
import streamlit as st

st.set_page_config(page_title="Funnel Drop-Off Dashboard (2024)", layout="wide")

# ---------- Load data ----------
BY_SEG_PATH = "data/funnel_metrics_by_device_region.csv"
OVERALL_PATH = "data/funnel_metrics_overall.csv"

def load_csv(path: str) -> pd.DataFrame:
    if not os.path.exists(path):
        st.error(f"Missing required file: {path}")
        st.stop()
    return pd.read_csv(path)

by_seg = load_csv(BY_SEG_PATH)
overall = load_csv(OVERALL_PATH)

# ---------- Helpers ----------
STEP_LABELS = {
    "visit": "Visit",
    "signup": "Signup",
    "product_view": "Product View",
    "add_to_cart": "Add to Cart",
    "purchase": "Purchase"
}

def prettify_steps(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df["step_label"] = df["step"].map(STEP_LABELS).fillna(df["step"])
    return df

overall = prettify_steps(overall)
by_seg = prettify_steps(by_seg)

def funnel_kpis(overall_df: pd.DataFrame):
    ordered = overall_df.sort_values("step_order")
    visit_users = int(ordered.loc[ordered["step"] == "visit", "users"].iloc[0])
    purchase_users = int(ordered.loc[ordered["step"] == "purchase", "users"].iloc[0])
    overall_conv = (purchase_users / visit_users) * 100 if visit_users else 0

    # biggest drop-off step (exclude first step where dropoff is NaN)
    drop_df = ordered[ordered["step_order"] > 1].copy()
    drop_df["step_dropoff_pct"] = pd.to_numeric(drop_df["step_dropoff_pct"], errors="coerce")
    worst = drop_df.sort_values("step_dropoff_pct", ascending=False).head(1)
    worst_step = worst["step_label"].iloc[0] if len(worst) else "N/A"
    worst_drop = float(worst["step_dropoff_pct"].iloc[0]) if len(worst) else 0.0

    return visit_users, purchase_users, overall_conv, worst_step, worst_drop

# ---------- Header ----------
st.markdown("## 🧭 Funnel Drop-Off Dashboard (2024)")
st.caption("End-to-end funnel analysis using SQL + Python. Explore drop-offs by device and region.")

visit_users, purchase_users, overall_conv, worst_step, worst_drop = funnel_kpis(overall)

k1, k2, k3, k4 = st.columns(4)
k1.metric("Visits", f"{visit_users:,}")
k2.metric("Purchases", f"{purchase_users:,}")
k3.metric("Overall Conversion", f"{overall_conv:.2f}%")
k4.metric("Largest Drop-Off Step", worst_step, f"{worst_drop:.2f}%")

st.markdown("---")

# ---------- Sidebar filters ----------
st.sidebar.header("Filters")
device_choice = st.sidebar.selectbox("Device", ["All"] + sorted(by_seg["device"].unique().tolist()))
region_choice = st.sidebar.selectbox("Region", ["All"] + sorted(by_seg["region"].unique().tolist()))

seg = by_seg.copy()
if device_choice != "All":
    seg = seg[seg["device"] == device_choice]
if region_choice != "All":
    seg = seg[seg["region"] == region_choice]

# ---------- Tabs ----------
tab1, tab2, tab3 = st.tabs(["📌 Funnel Overview", "📉 Drop-Off Insights", "🧩 Segment Table"])

with tab1:
    left, right = st.columns([1.2, 1])

    with left:
        st.subheader("Overall Funnel (Users per Step)")
        chart_df = overall.sort_values("step_order")[["step_label", "users"]].set_index("step_label")
        st.bar_chart(chart_df)

    with right:
        st.subheader("Overall Metrics Table")
        show = overall.sort_values("step_order")[["step_order","step_label","users","step_conversion_pct","step_dropoff_pct"]].copy()
        show.columns = ["Step #", "Step", "Users", "Step Conversion %", "Step Drop-Off %"]
        st.dataframe(show, use_container_width=True, hide_index=True)

with tab2:
    st.subheader("Drop-Off by Step (Selected Segment)")
    st.caption(f"Current filter: device = **{device_choice}**, region = **{region_choice}**")

    seg_drop = seg[seg["step_order"] > 1].sort_values("step_order").copy()
    if seg_drop.empty:
        st.info("No rows found for the selected segment.")
    else:
        # show drop-off chart
        drop_chart = seg_drop[["step_label","step_dropoff_pct"]].set_index("step_label")
        st.line_chart(drop_chart)

        # highlight worst segment step
        seg_drop["step_dropoff_pct"] = pd.to_numeric(seg_drop["step_dropoff_pct"], errors="coerce")
        worst_seg = seg_drop.sort_values("step_dropoff_pct", ascending=False).head(1)
        ws = worst_seg["step_label"].iloc[0]
        wd = float(worst_seg["step_dropoff_pct"].iloc[0])
        st.success(f"Biggest drop-off in this segment is **{ws}** at **{wd:.2f}%**.")

with tab3:
    st.subheader("Funnel by Device/Region (Detail Table)")
    out = seg.sort_values(["device","region","step_order"])[
        ["device","region","step_order","step_label","users","step_conversion_pct","step_dropoff_pct"]
    ].copy()
    out.columns = ["Device","Region","Step #","Step","Users","Step Conversion %","Step Drop-Off %"]
    st.dataframe(out, use_container_width=True, hide_index=True)

st.markdown("---")
st.caption("Built with SQL + Python + Streamlit. AI-assisted recommendations available in the repo under `/ai`.")
