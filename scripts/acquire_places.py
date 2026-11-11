from pathlib import Path
import requests
import hashlib
import json
from datetime import datetime, timezone

# Code that finds the folder relative to this script
ROOT = Path(__file__).resolve().parents[1]
RAW_FILE = ROOT / "data" / "raw" / "places_county_2025.csv"
RECEIPT  = ROOT / "data" / "raw" / "places_manifest.json"
URL = "https://data.cdc.gov/api/views/i46a-9kgh/rows.csv?accessType=DOWNLOAD"


# First run: download, checksum, write the receipt
if not RAW_FILE.exists():
    response = requests.get(URL)
    RAW_FILE.parent.mkdir(parents=True, exist_ok=True)
    RAW_FILE.write_bytes(response.content)

    fingerprint = hashlib.sha256(RAW_FILE.read_bytes()).hexdigest()

    receipt = {
        "source_url": URL,
        "dataset_id": "i46a-9kgh",
        "release": "PLACES 2025 release",
        "downloaded_utc": datetime.now(timezone.utc).isoformat(),
        "sha256": fingerprint,
    }
    RECEIPT.write_text(json.dumps(receipt, indent=2))
    print("Downloaded and wrote receipt.")

# Later runs: compute checksum to ensure it matches
else:
    fingerprint = hashlib.sha256(RAW_FILE.read_bytes()).hexdigest()

    saved = json.loads(RECEIPT.read_text())
    if fingerprint != saved["sha256"]:
        raise SystemExit(
            f"Checksum mismatch: expected {saved['sha256']}, got {fingerprint}"
        )
    print("Checksum OK.")