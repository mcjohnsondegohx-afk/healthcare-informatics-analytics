-- Synthetic Hospital Appointment Access Analytics
-- SQLite-compatible SQL; all data is simulated, not real patient information.
-- No-show rate = No Show / (No Show + Completed). No cancellations are included.

-- 1. Overall performance
SELECT COUNT(*) AS total_appointments,
       SUM(CASE WHEN status = 'No Show' THEN 1 ELSE 0 END) AS no_shows,
       ROUND(100.0 * SUM(CASE WHEN status = 'No Show' THEN 1 ELSE 0 END) / COUNT(*), 1) AS no_show_rate_pct,
       ROUND(AVG(CASE WHEN status = 'Completed' THEN checkin_wait_minutes END), 1) AS avg_checkin_wait_minutes
FROM appointments;

-- 2. Compare facilities
SELECT facility, COUNT(*) AS appointments,
       ROUND(100.0 * SUM(CASE WHEN status = 'No Show' THEN 1 ELSE 0 END) / COUNT(*), 1) AS no_show_rate_pct,
       ROUND(AVG(CASE WHEN status = 'Completed' THEN checkin_wait_minutes END), 1) AS avg_checkin_wait_minutes
FROM appointments GROUP BY facility ORDER BY no_show_rate_pct DESC;

-- 3. Compare specialties
SELECT specialty, COUNT(*) AS appointments,
       ROUND(100.0 * SUM(CASE WHEN status = 'No Show' THEN 1 ELSE 0 END) / COUNT(*), 1) AS no_show_rate_pct
FROM appointments GROUP BY specialty ORDER BY no_show_rate_pct DESC;

-- 4. Appointment lead-time and missed visits
SELECT CASE WHEN days_to_appointment <= 7 THEN '0 to 7 days'
            WHEN days_to_appointment <= 14 THEN '8 to 14 days'
            WHEN days_to_appointment <= 30 THEN '15 to 30 days'
            ELSE '31+ days' END AS lead_time_band,
       COUNT(*) AS appointments,
       ROUND(100.0 * SUM(CASE WHEN status = 'No Show' THEN 1 ELSE 0 END) / COUNT(*), 1) AS no_show_rate_pct
FROM appointments
GROUP BY lead_time_band
ORDER BY MIN(days_to_appointment);
