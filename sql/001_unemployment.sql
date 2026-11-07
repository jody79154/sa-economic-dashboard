-- Run from the repository root using psql -f.
\set ON_ERROR_STOP on
BEGIN;

CREATE TABLE IF NOT EXISTS public.unemployment_observations (
    country_code text NOT NULL CHECK (length(country_code) = 3),
    indicator_code text NOT NULL,
    indicator_name text NOT NULL,
    year integer NOT NULL CHECK (year BETWEEN 1 AND 9999),
    unemployment_pct numeric CHECK (unemployment_pct BETWEEN 0 AND 100),
    retrieved_at_utc timestamptz NOT NULL,
    PRIMARY KEY (country_code, indicator_code, year)
);

CREATE TEMP TABLE unemployment_import
    (LIKE public.unemployment_observations INCLUDING ALL)
    ON COMMIT DROP;

-- Client-side copy: reads the CSV as the current Linux user.
-- Blank percentages become SQL NULL, not zero.
\copy unemployment_import (country_code, indicator_code, indicator_name, year, unemployment_pct, retrieved_at_utc) FROM 'data/processed/za_unemployment.csv' WITH (FORMAT csv, HEADER true)

INSERT INTO public.unemployment_observations AS existing
SELECT * FROM unemployment_import
ON CONFLICT (country_code, indicator_code, year)
DO UPDATE SET
    indicator_name = EXCLUDED.indicator_name,
    unemployment_pct = EXCLUDED.unemployment_pct,
    retrieved_at_utc = EXCLUDED.retrieved_at_utc
WHERE EXCLUDED.retrieved_at_utc >= existing.retrieved_at_utc;

COMMIT;

SELECT COUNT(*) AS total_rows,
       COUNT(unemployment_pct) AS available_values,
       COUNT(*) - COUNT(unemployment_pct) AS missing_values,
       MIN(year) AS first_year,
       MAX(year) AS last_year
FROM public.unemployment_observations
WHERE country_code = 'ZAF' AND indicator_code = 'SL.UEM.TOTL.ZS';
