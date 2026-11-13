\set ON_ERROR_STOP on
\pset pager off
-- All queries use the South African modeled ILO unemployment series.

\echo '1. Latest five available years'
SELECT year, unemployment_pct
FROM public.unemployment_observations
WHERE country_code = 'ZAF' AND indicator_code = 'SL.UEM.TOTL.ZS'
  AND unemployment_pct IS NOT NULL
ORDER BY year DESC
LIMIT 5;

\echo '2. Five highest observed annual rates'
SELECT year, unemployment_pct
FROM public.unemployment_observations
WHERE country_code = 'ZAF' AND indicator_code = 'SL.UEM.TOTL.ZS'
  AND unemployment_pct IS NOT NULL
ORDER BY unemployment_pct DESC, year
LIMIT 5;

\echo '3. Average annual rate by decade (available years only)'
SELECT (year / 10) * 10 AS decade,
       COUNT(*) AS available_years,
       ROUND(AVG(unemployment_pct), 3) AS mean_annual_rate_pct
FROM public.unemployment_observations
WHERE country_code = 'ZAF' AND indicator_code = 'SL.UEM.TOTL.ZS'
  AND unemployment_pct IS NOT NULL
GROUP BY (year / 10) * 10
ORDER BY decade;
-- An unweighted mean of annual rates, not a pooled labor-force unemployment rate.
-- The 1990s and 2020s have incomplete decade coverage.

\echo '4. Recent year-over-year changes in percentage points'
SELECT current.year, current.unemployment_pct,
       current.unemployment_pct - previous.unemployment_pct AS change_percentage_points
FROM public.unemployment_observations AS current
LEFT JOIN public.unemployment_observations AS previous
  ON previous.country_code = current.country_code
 AND previous.indicator_code = current.indicator_code
 AND previous.year = current.year - 1
WHERE current.country_code = 'ZAF'
  AND current.indicator_code = 'SL.UEM.TOTL.ZS'
  AND current.unemployment_pct IS NOT NULL
ORDER BY current.year DESC
LIMIT 5;
-- Explicit year matching avoids treating multi-year gaps as annual changes.

\echo '5. Missing-data coverage'
SELECT MIN(year) AS first_returned_year,
       MAX(year) AS last_returned_year,
       MIN(year) FILTER (WHERE unemployment_pct IS NOT NULL) AS first_available_year,
       MAX(year) FILTER (WHERE unemployment_pct IS NOT NULL) AS last_available_year,
       COUNT(*) AS total_rows,
       COUNT(unemployment_pct) AS available_values,
       COUNT(*) FILTER (WHERE unemployment_pct IS NULL) AS missing_values
FROM public.unemployment_observations
WHERE country_code = 'ZAF' AND indicator_code = 'SL.UEM.TOTL.ZS';
