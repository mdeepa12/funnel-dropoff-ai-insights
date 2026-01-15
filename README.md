🧭 Funnel Drop-Off Analysis with AI-Assisted Insights (2024)

SQL • Python • Streamlit

🔗 Live Dashboard: https://streamapp-2024-dashboard.streamlit.app/
🔗 Repository: https://github.com/mdeepa12/funnel-dropoff-ai-insights

📌 Business Problem

Product teams observed that a significant portion of users failed to complete purchases, but lacked clarity on where users dropped off in the funnel and why.

The goal of this analysis was to:

Identify high-friction funnel stages

Quantify conversion and drop-off rates

Understand how funnel performance varies by device and region

Provide data-driven recommendations to improve conversion

📊 Dataset Overview

This project uses a large-scale synthetic event dataset designed to reflect realistic product usage patterns.

Users: 100,000+

Events: Millions of event-level records

Event Types: Visit, Product View, Add to Cart, Purchase

Dimensions: User ID, timestamp, device type, region

Synthetic data was used to simulate real-world scale while avoiding sensitive or proprietary information.

📐 Metrics Defined

The following core product metrics were defined and calculated:

Step Conversion Rate
Percentage of users progressing from one funnel step to the next

Step Drop-Off Rate
Percentage of users who exit the funnel at each stage

Overall Funnel Conversion
Percentage of users who complete the full funnel (Visit → Purchase)

Metrics were computed using event-level SQL aggregations and validated through Python analysis.

🔍 Key Findings

The largest drop-off occurred between Product View → Add to Cart, indicating potential UX or pricing friction

Mobile users consistently showed higher mid-funnel drop-off compared to desktop users

Certain regions underperformed specifically at the checkout stage, despite similar upstream engagement

These patterns suggest that the issue is not acquisition, but mid- and late-funnel experience.

📈 Dashboard

An interactive Streamlit dashboard was built to allow stakeholders to:

Explore funnel conversion and drop-off rates by step

Segment performance by device type and region

Quickly identify the highest-impact drop-off points

The dashboard enables self-serve analysis, reducing dependency on ad-hoc analytics requests.

🤖 AI-Assisted Insights

To augment manual analysis, AI-assisted techniques were used to:

Summarize key funnel patterns across segments

Highlight statistically meaningful differences

Generate structured recommendations based on observed drop-offs

AI insights are used as a decision-support layer, not a replacement for analytical judgment.

💡 Recommendations

Based on the analysis:

Optimize Product Page → Add to Cart UX
Simplify calls-to-action and reduce friction for mobile users

Improve Mobile Performance
Prioritize mobile-specific funnel optimizations where drop-off is highest

Target Checkout Improvements by Region
Investigate payment, latency, or localization issues in underperforming regions

Validate Changes via A/B Testing
Measure impact of improvements using controlled experiments

🧱 Architecture Overview
Raw Event Data (CSV)
        ↓
SQL Funnel Aggregations
        ↓
Python Analysis & Validation
        ↓
Streamlit Dashboard
        ↓
AI-Assisted Insight Layer

🛠 Tech Stack

SQL: Funnel and conversion metrics

Python: Pandas, NumPy for analysis

Visualization: Streamlit

Version Control: Git & GitHub
