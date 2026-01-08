import pandas as pd
import streamlit as st
import plotly.express as px

st.set_page_config(page_title="Funnel Drop-Off Dashboard (2024)", layout="wide")

st.title("🧭 Funnel Drop-Off Dashboard (2024)")
st.caption("Funnel analysis using synthetic 2024 event data. Explore drop-offs by device and region.")

# Load exported metrics
by_seg_path = "data/funnel_metrics_by_device_region.csv"
overall_path = "data/funnel_metrics_overall.csv"

by_seg = pd.read_csv(by_seg_path)
overall = pd.read_csv(overall_path)

# Sidebar filters
st.sidebar.header("Filters")
device = st.sidebar.selectbox("Device", ["all"] + sorted(by_seg["device"].unique().tolist()))
region = st.sidebar.selectbox("Region", ["all"] + sorted(by_seg["region"].unique().tolist()))

if device != "all":
    by_seg = by_seg[by_seg["device"] == device]
if region != "all":
    by_seg = by_seg[by_seg["region"] == region]

# Overall funnel
st.subheader("Overall Funnel")
col1, col2 = st.columns([1, 2])

with col1:
    st.dataframe(overall[["step_order","step","users","step_conversion_pct","step_dropoff_pct"]], use_container_width=True)

with col2:
    fig = px.bar(overall.sort_values("step_order"), x="step", y="users", title="Users by Funnel Step (Overall)")
    st.plotly_chart(fig, use_container_width=True)

# Segment funnel
st.subheader("Funnel by Segment (Device / Region)")
st.write(f"Showing: **device={device}**, **region={region}**")

col3, col4 = st.columns([1, 2])

with col3:
    st.dataframe(by_seg[["device","region","step_order","step","users","step_conversion_pct","step_dropoff_pct"]]
                 .sort_values(["device","region","step_order"]), use_container_width=True)

with col4:
    # Drop-off chart (step > 1)
    tmp = by_seg[by_seg["step_order"] > 1].copy()
    if len(tmp) == 0:
        st.info("No segment rows found for selected filters.")
    else:
        fig2 = px.line(tmp.sort_values("step_order"), x="step", y="step_dropoff_pct",
                       color="region" if device != "all" and region == "all" else None,
                       markers=True,
                       title="Step Drop-off % (Selected Segment)")
        st.plotly_chart(fig2, use_container_width=True)

st.markdown("---")
st.caption("Built with SQL + Python + Streamlit. AI-assisted insights included in /ai.")

