# SQL: Funnel Metrics

This folder contains the SQL used to compute funnel conversion and drop-off metrics.

## What this SQL does
- Filters event data to funnel steps (visit → product_view → add_to_cart → purchase)
- Deduplicates events by taking the first occurrence per user per step
- Enforces step order (a user counts for step N only if they completed step N-1 earlier)
- Produces step-level counts, conversion rate, and drop-off rate

## Files
- `02_funnel_metrics.sql` — Main query to compute funnel metrics (overall + by device/region)
- `03_quality_checks.sql` — Optional data quality checks (nulls, duplicates, unexpected steps)

## Output tables / exports
The query is designed to produce a dataset shaped like:

device | region | step | step_order | users | step_conversion_rate | step_dropoff_rate

This output is exported to CSV and used by the Streamlit dashboard.
