"""Download the author's public archive; preserve it unchanged and log provenance."""
from pathlib import Path
from datetime import datetime, timezone
import hashlib
import json
import urllib.request
import zipfile

ROOT = Path(__file__).resolve().parents[2]
URL = "https://davidcard.berkeley.edu/data_sets/njmin.zip"


def main():
    raw = ROOT / "data" / "raw"
    raw.mkdir(parents=True, exist_ok=True)
    with urllib.request.urlopen(URL, timeout=60) as response:
        payload = response.read()
    archive = raw / "njmin.zip"
    archive.write_bytes(payload)
    destination = (raw / "author").resolve()
    with zipfile.ZipFile(archive) as z:
        for member in z.infolist():
            target = (destination / member.filename).resolve()
            if not target.is_relative_to(destination):
                raise ValueError("Unsafe archive path")
        z.extractall(destination)
    metadata = {
        "source_url": URL,
        "source_page": "https://davidcard.berkeley.edu/data_sets.html",
        "downloaded_at_utc": datetime.now(timezone.utc).isoformat(),
        "sha256": hashlib.sha256(payload).hexdigest(),
        "bytes": len(payload),
        "note": "Author-hosted public archive, not the course-provided CSV."
    }
    (ROOT / "docs" / "data_provenance.json").write_text(
        json.dumps(metadata, indent=2), encoding="utf-8"
    )
    print("Downloaded author archive and recorded provenance.")


if __name__ == "__main__":
    main()
