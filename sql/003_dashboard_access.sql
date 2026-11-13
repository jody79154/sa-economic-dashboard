\set ON_ERROR_STOP on
-- Execute as database owner analytics_user, after creating dashboard_reader.
BEGIN;
GRANT CONNECT ON DATABASE sa_economics TO dashboard_reader;
GRANT USAGE ON SCHEMA public TO dashboard_reader;
GRANT SELECT ON public.unemployment_observations TO dashboard_reader;
COMMIT;
