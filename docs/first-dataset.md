# First dataset

Run from the repository root with the virtual environment active:

```bash
python src/fetch_unemployment.py
```

Requires outbound HTTPS access to api.worldbank.org. Saves timestamped raw response pages and a cleaned CSV in ignored data folders. The CSV is overwritten on each successful run; raw snapshots are retained. Errors stop the export; an older CSV may remain after a failed run, so inspect the terminal result and retrieval timestamp.

Checks: HTTP success, response structure, expected country/indicator, numeric years/values, duplicate keys, at least one available value, and percentage range. Missing observations remain blank, never zero-filled.

Inspect the printed counts and latest available years. This is the modeled ILO estimate, not a national estimate. Missing years and historical revisions must be discussed in analysis.

Validation so far: Python syntax compilation passed. Live API retrieval and server execution have not yet been verified. Record actual counts and lessons in the learning log after the first successful run. No fabricated observations are included.
