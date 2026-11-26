"""Download the Chrome dino game sources and assets from Chromium, pinned to one commit.

The files land in chromium/ with their Chromium paths, so build.py can bundle the
real game (no redrawn sprites, no re-recorded sounds).

    python fetch_chromium.py            # pinned COMMIT
    python fetch_chromium.py main       # a newer Chromium, then rebuild and check
"""
import base64
import json
import sys
import urllib.request
from pathlib import Path

COMMIT = "3f3f2f0c42781730fde4aba9071862b79ce15fe2"  # chromium/src main, 2026-10-30
BASE = "https://chromium.googlesource.com/chromium/src/+/{rev}/{path}?format={fmt}"
NETERROR = "components/neterror/resources"
INTERSTITIAL = "components/security_interstitials/core/common/resources"

FILES = [
    "LICENSE",
    f"{NETERROR}/constants.ts",
    f"{NETERROR}/neterror.css",
    f"{INTERSTITIAL}/interstitial_core.css",
    f"{INTERSTITIAL}/interstitial_common.css",
] + [
    f"{NETERROR}/sounds/{s}.mp3" for s in ("button-press", "hit", "score-reached")
] + [
    f"{NETERROR}/images/default_{p}_percent/offline/{p}-{n}.png"
    for p in (100, 200) for n in ("offline-sprite", "error-offline")
]

OUT = Path(__file__).resolve().parent / "chromium"


def get(rev, path, fmt):
    with urllib.request.urlopen(BASE.format(rev=rev, path=path, fmt=fmt), timeout=60) as r:
        return r.read()


def main():
    rev = sys.argv[1] if len(sys.argv) > 1 else COMMIT
    listing = json.loads(get(rev, f"{NETERROR}/dino_game/", "JSON")[4:])  # drop the )]}' guard
    game = [f"{NETERROR}/dino_game/{e['name']}" for e in listing["entries"] if e["name"].endswith(".ts")]
    for path in FILES + game:
        data = base64.b64decode(get(rev, path, "TEXT"))
        dest = OUT / path
        dest.parent.mkdir(parents=True, exist_ok=True)
        dest.write_bytes(data)
        print(f"{len(data):>8}  {path}")
    (OUT / "REVISION").write_text(rev + "\n")


if __name__ == "__main__":
    main()
