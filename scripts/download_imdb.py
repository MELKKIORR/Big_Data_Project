"""Download the IMDb non-commercial datasets into data/raw/.

Usage (inside the spark container):
    python scripts/download_imdb.py [--force]
"""

import argparse
from pathlib import Path

import requests

from src.common.config import RAW_DIR

BASE_URL = "https://datasets.imdbws.com"
FILES = [
    "name.basics.tsv.gz",
    "title.akas.tsv.gz",
    "title.basics.tsv.gz",
    "title.crew.tsv.gz",
    "title.episode.tsv.gz",
    "title.principals.tsv.gz",
    "title.ratings.tsv.gz",
]
CHUNK_SIZE = 1024 * 1024


def download(name: str, target_dir: Path, force: bool = False) -> None:
    """Download one file, skipping it if it is already present."""
    target = target_dir / name
    if target.exists() and not force:
        print(f"[skip] {name} already present")
        return

    url = f"{BASE_URL}/{name}"
    partial = target.with_name(target.name + ".part")
    print(f"[get]  {url}")
    with requests.get(url, stream=True, timeout=60) as response:
        response.raise_for_status()
        total = int(response.headers.get("Content-Length", 0))
        done = 0
        with open(partial, "wb") as handle:
            for chunk in response.iter_content(CHUNK_SIZE):
                handle.write(chunk)
                done += len(chunk)
                if total:
                    print(f"\r       {done / total:6.1%}", end="", flush=True)
    print()
    # Rename only at the end so an interrupted download is never mistaken
    # for a complete file.
    partial.rename(target)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--force", action="store_true", help="re-download files")
    args = parser.parse_args()

    RAW_DIR.mkdir(parents=True, exist_ok=True)
    for name in FILES:
        download(name, RAW_DIR, force=args.force)
    print(f"Done. Files are in {RAW_DIR}")


if __name__ == "__main__":
    main()
