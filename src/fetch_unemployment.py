"""Fetch annual South African unemployment data; preserve missing observations."""
import json
from datetime import datetime, timezone
from pathlib import Path

import pandas as pd
import requests

ROOT = Path(__file__).resolve().parents[1]
COUNTRY = "ZAF"
INDICATOR = "SL.UEM.TOTL.ZS"
URL = f"https://api.worldbank.org/v2/country/{COUNTRY}/indicator/{INDICATOR}"


def main():
    retrieved = datetime.now(timezone.utc)
    raw_dir = ROOT / "data" / "raw" / retrieved.strftime("%Y%m%dT%H%M%S%fZ")
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
            raise ValueError("Unexpected API response; inspect saved raw snapshot.")
        meta, observations = payload
        if not isinstance(observations, list) or not observations:
            raise ValueError("API returned no observations.")
        for item in observations:
            if item["countryiso3code"] != COUNTRY or item["indicator"]["id"] != INDICATOR:
                raise ValueError("Unexpected country or indicator.")
            rows.append({
                "country_code": COUNTRY,
                "indicator_code": INDICATOR,
                "indicator_name": item["indicator"]["value"],
                "year": item["date"],
                "unemployment_pct": item["value"],
                "retrieved_at_utc": retrieved.isoformat(),
            })
        if page >= int(meta["pages"]):
            break
        page += 1

    frame = pd.DataFrame(rows)
    frame["year"] = pd.to_numeric(frame["year"], errors="raise").astype(int)
    frame["unemployment_pct"] = pd.to_numeric(frame["unemployment_pct"], errors="raise")
    if frame.duplicated(["country_code", "indicator_code", "year"]).any():
        raise ValueError("Duplicate observations found; export cancelled.")
    values = frame["unemployment_pct"].dropna()
    if values.empty or not values.between(0, 100).all():
        raise ValueError("Missing all values or unemployment outside 0–100 percent.")
    frame = frame.sort_values("year")
    output = ROOT / "data" / "processed" / "za_unemployment.csv"
    output.parent.mkdir(parents=True, exist_ok=True)
    frame.to_csv(output, index=False)
    print(f"Rows: {len(frame)} | Missing values: {frame['unemployment_pct'].isna().sum()}")
    print("Latest available observations (modeled ILO estimates):")
    print(frame.dropna(subset=["unemployment_pct"])[["year", "unemployment_pct"]].tail().to_string(index=False))
    print(f"CSV: {output}")
    print(f"Raw snapshots: {raw_dir}")


if __name__ == "__main__":
    main()
