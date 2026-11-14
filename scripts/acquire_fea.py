from pathlib import Path
import requests
import hashlib
import json
import zipfile
from datetime import datetime, timezone

# Finds the folder relative to this script
ROOT = Path(__file__).resolve().parents[1]
RAW_FILE    = ROOT / "data" / "raw" / "fea_county_2025.zip"
# EXTRACT_DIR = ROOT / "data" / "raw" / "fea_county_2025"
RECEIPT     = ROOT / "data" / "raw" / "fea_manifest.json"

# USDA ERS Food Environment Atlas, current version (CSV files, zipped)
# Listed on: https://www.ers.usda.gov/data-products/food-environment-atlas/data-access-and-documentation-downloads
SOURCE_PAGE = "https://www.ers.usda.gov/data-products/food-environment-atlas/data-access-and-documentation-downloads"
DOWNLOAD_URL = "https://www.ers.usda.gov/media/5570/food-environment-atlas-csv-files.zip?v=71038"


def sha256_of(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


# First run: download, checksum, write the receipt
if not RAW_FILE.exists():
    response = requests.get(DOWNLOAD_URL, headers={"User-Agent": "IS477-course-project"}, timeout=60)
    response.raise_for_status()

    RAW_FILE.parent.mkdir(parents=True, exist_ok=True)
    RAW_FILE.write_bytes(response.content)

    fingerprint = sha256_of(RAW_FILE)

    with zipfile.ZipFile(RAW_FILE) as z:
        contents = z.namelist()

    receipt = {
        "source_page": SOURCE_PAGE,
        "source_url": DOWNLOAD_URL,
        "dataset": "USDA ERS Food Environment Atlas (CSV files)",
        "downloaded_utc": datetime.now(timezone.utc).isoformat(),
        "size_bytes": RAW_FILE.stat().st_size,
        "files_in_zip": contents,
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

# # Unzip the CSVs so the cleaning script can read them
# if not EXTRACT_DIR.exists():
#     with zipfile.ZipFile(RAW_FILE) as z:
#         z.extractall(EXTRACT_DIR)
#     print(f"Extracted to {EXTRACT_DIR.relative_to(ROOT)}")
