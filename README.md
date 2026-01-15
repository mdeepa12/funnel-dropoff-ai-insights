# 🧭 Funnel Drop-Off Analysis with AI-Assisted Insights (2024)

**SQL • Python • Streamlit**

Live Dashboard: https://streamapp-2024-dashboard.streamlit.app/ 
Repository: https://github.com/mdeepa12/funnel-dropoff-ai-insights

---

## Business Problem

Product teams observed that a large portion of users failed to complete purchases, but lacked visibility into **where users dropped off in the funnel and why**.

The objective of this analysis was to:
- Identify high-friction funnel stages
- Quantify conversion and drop-off rates
- Understand differences by device and region
- Provide actionable, data-driven recommendations to improve conversion

---

## Dataset Overview

This project uses a large-scale **synthetic event dataset** designed to mimic real-world product usage while avoiding sensitive data.

- Users: 100,000+
- Events: Millions of event-level records
- Funnel Steps: Visit → Product View → Add to Cart → Purchase
- Dimensions: user_id, event_time, device, region

---

## Metrics Defined

The following core product metrics were defined:

- Step Conversion Rate  
  Percentage of users moving from one funnel step to the next

- Step Drop-Off Rate  
  Percentage of users exiting the funnel at each stage

- Overall Funnel Conversion  
  Percentage of users completing the full funnel

Metrics were calculated using **SQL aggregations** and validated in Python.

---

## Key Findings

- The largest drop-off occurred between **Product View → Add to Cart**, indicating UX or pricing friction
- Mobile users showed consistently higher mid-funnel drop-off than desktop users
- Certain regions underperformed specifically at the checkout stage

These findings suggest issues primarily in the **mid- and late-funnel experience**, not acquisition.

---

## Dashboard

An interactive Streamlit dashboard was built to:
- Visualize funnel conversion and drop-off rates
- Segment performance by device and region
- Enable self-serve analysis for stakeholders

The dashboard reduces reliance on ad-hoc analysis and supports faster decision-making.

---

## AI-Assisted Insights

AI-assisted analysis was used to:
- Summarize funnel performance across segments
- Highlight meaningful conversion differences
- Generate structured recommendations based on observed patterns

AI serves as a **decision-support layer**, not a replacement for analysis.

---

## Recommendations

1. Optimize Product View → Add to Cart UX, especially for mobile users  
2. Improve mobile performance and call-to-action visibility  
3. Investigate checkout issues in underperforming regions  
4. Validate improvements through controlled A/B testing  

---

## Architecture

Raw Event Data (CSV)  
→ SQL Funnel Aggregations  
→ Python Analysis & Validation  
→ Streamlit Dashboard  
→ AI-Assisted Insights

---

## Tech Stack

- SQL: Funnel and conversion analysis  
- Python: Pandas, NumPy  
- Visualization: Streamlit  
- Version Control: Git, GitHub  

---

## Future Enhancements

<<<<<<< HEAD
- Statistical significance testing between segments  
- Time-based funnel trend analysis  
- Deeper experimentation framework integration 

## Code
- SQL (main funnel metrics): `sql/02_funnel_metrics.sql`
- Python (data + exports): `data/generate_events.py` and `notebooks/funnel_analysis.ipynb`
- Dashboard: `app.py`

>>>>>>> 2f658da (Add documented SQL for funnel metrics and quality checks)
