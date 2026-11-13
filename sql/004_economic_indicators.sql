-- Execute from the repository root as analytics_user in sa_economics.
\set ON_ERROR_STOP on
\pset pager off
BEGIN;

CREATE TABLE IF NOT EXISTS public.economic_observations (
    country_code text NOT NULL CHECK (length(country_code) = 3),
    indicator_code text NOT NULL,
    indicator_name text NOT NULL,
    year integer NOT NULL CHECK (year BETWEEN 1 AND 9999),
    value numeric,
    unit text NOT NULL,
    retrieved_at_utc timestamptz NOT NULL,
    PRIMARY KEY (country_code, indicator_code, year),
    CHECK (value IS NULL OR value::text NOT IN ('NaN', 'Infinity', '-Infinity')),
    CHECK (indicator_code <> 'SL.UEM.TOTL.ZS' OR value BETWEEN 0 AND 100)
);

-- Preserve the legacy table: the deployed dashboard still reads it.
INSERT INTO public.economic_observations AS existing
    (country_code, indicator_code, indicator_name, year, value, unit, retrieved_at_utc)
SELECT country_code, indicator_code, indicator_name, year, unemployment_pct,
       '% of total labor force', retrieved_at_utc
FROM public.unemployment_observations
WHERE indicator_code = 'SL.UEM.TOTL.ZS'
ON CONFLICT (country_code, indicator_code, year)
DO UPDATE SET indicator_name = EXCLUDED.indicator_name,
              value = EXCLUDED.value, unit = EXCLUDED.unit,
              retrieved_at_utc = EXCLUDED.retrieved_at_utc
WHERE EXCLUDED.retrieved_at_utc >= existing.retrieved_at_utc;

CREATE TEMP TABLE inflation_import (
    country_code text NOT NULL CHECK (country_code = 'ZAF'),
    indicator_code text NOT NULL CHECK (indicator_code = 'FP.CPI.TOTL.ZG'),
    indicator_name text NOT NULL,
    year integer NOT NULL CHECK (year BETWEEN 1 AND 9999),
    inflation_pct numeric,
    retrieved_at_utc timestamptz NOT NULL,
    PRIMARY KEY (country_code, indicator_code, year),
    CHECK (inflation_pct IS NULL OR inflation_pct::text NOT IN ('NaN', 'Infinity', '-Infinity'))
) ON COMMIT DROP;

\copy inflation_import (country_code, indicator_code, indicator_name, year, inflation_pct, retrieved_at_utc) FROM 'data/processed/za_inflation.csv' WITH (FORMAT csv, HEADER true)

INSERT INTO public.economic_observations AS existing
    (country_code, indicator_code, indicator_name, year, value, unit, retrieved_at_utc)
SELECT country_code, indicator_code, indicator_name, year, inflation_pct,
       'annual % change in consumer prices', retrieved_at_utc
FROM inflation_import
ON CONFLICT (country_code, indicator_code, year)
DO UPDATE SET indicator_name = EXCLUDED.indicator_name,
              value = EXCLUDED.value, unit = EXCLUDED.unit,
              retrieved_at_utc = EXCLUDED.retrieved_at_utc
WHERE EXCLUDED.retrieved_at_utc >= existing.retrieved_at_utc;

GRANT SELECT ON public.economic_observations TO dashboard_reader;
COMMIT;

SELECT indicator_code, unit, COUNT(*) AS total_rows,
       COUNT(value) AS available_values,
       COUNT(*) - COUNT(value) AS missing_values,
       MIN(year) AS first_year, MAX(year) AS last_year
FROM public.economic_observations
WHERE country_code = 'ZAF'
GROUP BY indicator_code, unit
ORDER BY indicator_code;
