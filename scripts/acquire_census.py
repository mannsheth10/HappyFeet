from pathlib import Path
import csv
import os
import requests
import hashlib
import json
from datetime import datetime, timezone
 
# Finds the folder relative to this script
ROOT = Path(__file__).resolve().parents[1]
RAW_FILE = ROOT / "data" / "raw" / "acs5_county_2024.csv"
RECEIPT  = ROOT / "data" / "raw" / "acs5_manifest.json"
 
YEAR = 2024                     
BASE_URL = f"https://api.census.gov/data/{YEAR}/acs/acs5"
VARIABLES = ["NAME", "B01003_001E", "B19013_001E", "B17001_001E", "B17001_002E"]  # name, total pop, median household income
GEOGRAPHY = "county:*"               # all counties; add "&in=state:17" 
 
#key
API_KEY = os.environ.get("CENSUS_API_KEY")
if not API_KEY:
    raise SystemExit(
        "Missing API key. Set it first, e.g.\n"
        "  macOS/Linux:  export CENSUS_API_KEY='your_key'\n"
        "  Windows PS:   $env:CENSUS_API_KEY='your_key'"
    )
 
params = {
    "get": ",".join(VARIABLES),
    "for": GEOGRAPHY,
    "key": API_KEY,
}
 
 
def sha256_of(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()
 
 
# First run: download, checksum, write the receipt
if not RAW_FILE.exists():
    response = requests.get(BASE_URL, params=params, timeout=60)
    response.raise_for_status()
 
    
    try:
        rows = response.json()
    except ValueError:
        raise SystemExit(f"Census API did not return JSON: {response.text[:300]}")
 
    RAW_FILE.parent.mkdir(parents=True, exist_ok=True)
    with RAW_FILE.open("w", newline="", encoding="utf-8") as f:
        csv.writer(f).writerows(rows)  # first row is the header
 
    fingerprint = sha256_of(RAW_FILE)
 
    receipt = {
        # Store the URL without the key
        "source_url": BASE_URL,
        "query": {"get": params["get"], "for": params["for"]},
        "dataset": f"acs/acs5 {YEAR}",
        "downloaded_utc": datetime.now(timezone.utc).isoformat(),
        "row_count": len(rows) - 1,
        "sha256": fingerprint,
    }
    RECEIPT.write_text(json.dumps(receipt, indent=2))
    print("Downloaded and wrote receipt.")
 
# checksum
else:
    fingerprint = sha256_of(RAW_FILE)
 
    saved = json.loads(RECEIPT.read_text())
    if fingerprint != saved["sha256"]:
        raise SystemExit(
            f"Checksum mismatch: expected {saved['sha256']}, got {fingerprint}"
        )
    print("Checksum OK.")