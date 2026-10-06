"""Pull ERCOT hourly demand (D) and day-ahead forecast (DF) from the EIA API into bronze."""
import os
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path

import pandas as pd
import requests
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.environ["EIA_API_KEY"]
URL = "https://api.eia.gov/v2/electricity/rto/region-data/data/"
PAGE_SIZE = 5000  # the API's hard cap per request
BRONZE = Path("data/bronze")


def fetch(start: str, end: str) -> pd.DataFrame:
    rows, offset = [], 0
    while True:
        params = {
            "api_key": API_KEY,
            "frequency": "hourly",
            "data[]": "value",
            "facets[respondent][]": "ERCO",
            "facets[type][]": ["D", "DF"],
            "start": start,
            "end": end,
            "sort[0][column]": "period",
            "sort[0][direction]": "asc",
            "offset": offset,
            "length": PAGE_SIZE,
        }
        resp = requests.get(URL, params=params, timeout=60)
        if resp.status_code != 200:
            # Don't print resp.url: it contains the API key.
            raise RuntimeError(f"EIA API returned HTTP {resp.status_code}")
        body = resp.json()["response"]
        batch = body["data"]
        rows.extend(batch)
        total = int(body["total"])
        print(f"fetched {len(rows)} of {total} rows")
        offset += PAGE_SIZE
        if not batch or offset >= total:
            break
    df = pd.DataFrame(rows)
    df["ingested_at"] = datetime.now(timezone.utc).isoformat()
    return df


def main(days: int) -> None:
    end = datetime.now(timezone.utc)
    start = end - timedelta(days=days)
    df = fetch(start.strftime("%Y-%m-%dT%H"), end.strftime("%Y-%m-%dT%H"))
    BRONZE.mkdir(parents=True, exist_ok=True)
    # One file per date range: rerunning the same range overwrites it instead of duplicating.
    out = BRONZE / f"eia_ercot_{start:%Y%m%d}_{end:%Y%m%d}.parquet"
    df.to_parquet(out, index=False)
    print(f"wrote {len(df)} rows to {out}")


if __name__ == "__main__":
    main(int(sys.argv[1]) if len(sys.argv) > 1 else 7)
