-- Funnel Drop-Off Analysis (PostgreSQL-friendly)
-- Assumes an events table with:
--   user_id (text/int), event_name (text), event_time (timestamp),
--   device (text), region (text)

-- ------------------------------------------------------------
-- 1) Define funnel steps and map event_name -> step_order
-- ------------------------------------------------------------
WITH funnel_steps AS (
  SELECT 1 AS step_order, 'visit'        AS step UNION ALL
  SELECT 2,              'signup'        UNION ALL
  SELECT 3,              'product_view'  UNION ALL
  SELECT 4,              'add_to_cart'   UNION ALL
  SELECT 5,              'purchase'
),

-- ------------------------------------------------------------
-- 2) Earliest time each user hit each step (per segment)
--    NOTE: This avoids double-counting repeated events.
-- ------------------------------------------------------------
user_step_times AS (
  SELECT
    e.user_id,
    COALESCE(e.device, 'unknown') AS device,
    COALESCE(e.region, 'unknown') AS region,
    fs.step_order,
    fs.step,
    MIN(e.event_time) AS first_step_time
  FROM events e
  JOIN funnel_steps fs
    ON e.event_name = fs.step
  GROUP BY 1,2,3,4,5
),

-- ------------------------------------------------------------
-- 3) Enforce funnel order:
--    A user counts at step N only if they have completed step N-1
--    earlier (or same time) within the same segment.
-- ------------------------------------------------------------
ordered_funnel AS (
  SELECT
    a.user_id, a.device, a.region,
    a.step_order, a.step, a.first_step_time,
    b.first_step_time AS prev_step_time
  FROM user_step_times a
  LEFT JOIN user_step_times b
    ON a.user_id = b.user_id
   AND a.device  = b.device
   AND a.region  = b.region
   AND a.step_order = b.step_order + 1
),

-- Step 1 always qualifies. Steps 2..5 require prev step time <= current step time
qualified_steps AS (
  SELECT *
  FROM ordered_funnel
  WHERE step_order = 1
     OR (prev_step_time IS NOT NULL AND prev_step_time <= first_step_time)
),

-- ------------------------------------------------------------
-- 4) Count distinct users at each step (overall + by segment)
-- ------------------------------------------------------------
step_counts AS (
  SELECT
    device,
    region,
    step_order,
    step,
    COUNT(DISTINCT user_id) AS users
  FROM qualified_steps
  GROUP BY 1,2,3,4
),

-- ------------------------------------------------------------
-- 5) Add previous step users to compute conversion & drop-off
-- ------------------------------------------------------------
step_with_prev AS (
  SELECT
    sc.*,
    LAG(users) OVER (PARTITION BY device, region ORDER BY step_order) AS prev_users
  FROM step_counts sc
)

SELECT
  device,
  region,
  step_order,
  step,
  users,
  prev_users,
  CASE
    WHEN prev_users IS NULL THEN NULL
    WHEN prev_users = 0 THEN NULL
    ELSE ROUND((users::numeric / prev_users::numeric) * 100, 2)
  END AS step_conversion_pct,
  CASE
    WHEN prev_users IS NULL THEN NULL
    WHEN prev_users = 0 THEN NULL
    ELSE ROUND(((prev_users - users)::numeric / prev_users::numeric) * 100, 2)
  END AS step_dropoff_pct
FROM step_with_prev
ORDER BY device, region, step_order;

