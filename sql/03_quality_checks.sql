-- Data Quality Checks for funnel events dataset

-- 1) Check allowed event names
SELECT event_name, COUNT(*) AS cnt
FROM events
GROUP BY 1
ORDER BY cnt DESC;

-- 2) Check missing device/region
SELECT
  SUM(CASE WHEN device IS NULL THEN 1 ELSE 0 END) AS null_device,
  SUM(CASE WHEN region IS NULL THEN 1 ELSE 0 END) AS null_region
FROM events;

-- 3) Check duplicate rows (same user, event, timestamp)
SELECT user_id, event_name, event_time, COUNT(*) AS dup_cnt
FROM events
GROUP BY 1,2,3
HAVING COUNT(*) > 1
ORDER BY dup_cnt DESC
LIMIT 50;
