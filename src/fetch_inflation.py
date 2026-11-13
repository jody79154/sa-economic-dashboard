"""Fetch South African annual CPI inflation without altering unemployment data."""
import json
import math
from datetime import datetime, timezone
from pathlib import Path

import pandas as pd
import requests

ROOT = Path(__file__).resolve().parents[1]
COUNTRY = "ZAF"
INDICATOR = "FP.CPI.TOTL.ZG"
URL = f"https://api.worldbank.org/v2/country/{COUNTRY}/indicator/{INDICATOR}"


def main():
    retrieved = datetime.now(timezone.utc)
    raw_dir = ROOT / "data" / "raw" / "inflation" / retrieved.strftime("%Y%m%dT%H%M%S%fZ")
    raw_dir.mkdir(parents=True, exist_ok=False)
    rows = []
    page = 1
    while True:
        response = requests.get(
            URL, params={"format": "json", "per_page": 100, "page": page},
            timeout=(10, 60),
        )
        response.raise_for_status()
        payload = response.json()
        snapshot = {
            "request_url": response.url,
            "retrieved_at_utc": retrieved.isoformat(),
            "response": payload,
        }
        (raw_dir / f"page-{page}.json").write_text(
            json.dumps(snapshot, indent=2), encoding="utf-8"
        )
        if not isinstance(payload, list) or len(payload) != 2:
            raise ValueError("Unexpected API response; inspect the raw snapshot.")
        meta, observations = payload
        if not isinstance(observations, list) or not observations:
            raise ValueError("API returned no observations.")
        for item in observations:
            if item["countryiso3code"] != COUNTRY or item["indicator"]["id"] != INDICATOR:
                raise ValueError("Unexpected country or indicator.")
            value = item["value"]
            if value is not None and (
                isinstance(value, bool)
                or not isinstance(value, (int, float))
                or not math.isfinite(value)
            ):
                raise ValueError("Non-numeric or non-finite inflation value.")
            rows.append({
                "country_code": COUNTRY,
                "indicator_code": INDICATOR,
                "indicator_name": item["indicator"]["value"],
                "year": int(item["date"]),
                "inflation_pct": value,
                "retrieved_at_utc": retrieved.isoformat(),
            })
        if page >= int(meta["pages"]):
            break
        page += 1
    frame = pd.DataFrame(rows).sort_values("year")
    if frame.duplicated(["country_code", "indicator_code", "year"]).any():
        raise ValueError("Duplicate observations; export cancelled.")
    frame["inflation_pct"] = pd.to_numeric(frame["inflation_pct"], errors="raise")
    valid = frame.dropna(subset=["inflation_pct"])
    if valid.empty:
        raise ValueError("No available inflation values; export cancelled.")
    # Inflation is an annual rate of change: negative values and >100% can be valid.
    output = ROOT / "data" / "processed" / "za_inflation.csv"
    output.parent.mkdir(parents=True, exist_ok=True)
    temporary = output.with_suffix(".csv.tmp")
    frame.to_csv(temporary, index=False)
    temporary.replace(output)
    print(f"Rows: {len(frame)} | Missing values: {int(frame.inflation_pct.isna().sum())}")
    print(f"Returned years: {int(frame.year.min())}–{int(frame.year.max())}")
    print(f"Available years: {int(valid.year.min())}–{int(valid.year.max())}")
    print("Latest available annual CPI inflation observations (%):")
    print(valid[["year", "inflation_pct"]].tail().to_string(index=False))
    print(f"CSV: {output}")
    print(f"Raw snapshots: {raw_dir}")


if __name__ == "__main__":
    main()
