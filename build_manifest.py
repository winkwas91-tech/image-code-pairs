#!/usr/bin/env python3
"""Pair reference images with scripts and write a CSV manifest."""

from __future__ import annotations

import argparse
import csv
import sys
from pathlib import Path

IMAGE_EXT = {".png", ".jpg", ".jpeg", ".webp"}
SCRIPT_EXT = {".py"}


def collect(folder: Path) -> dict[str, dict[str, Path]]:
    found: dict[str, dict[str, Path]] = {}
    for path in sorted(folder.iterdir()):
        if not path.is_file():
            continue
        suffix = path.suffix.lower()
        if suffix in IMAGE_EXT:
            found.setdefault(path.stem, {})["image"] = path
        elif suffix in SCRIPT_EXT:
            found.setdefault(path.stem, {})["script"] = path
    return found


def rows_from(folder: Path) -> list[dict[str, str]]:
    rows = []
    for stem, files in collect(folder).items():
        image = files.get("image")
        script = files.get("script")
        status = "complete" if image and script else "incomplete"
        rows.append(
            {
                "id": stem,
                "image": image.as_posix() if image else "",
                "script": script.as_posix() if script else "",
                "status": status,
            }
        )
    return rows


def write_csv(rows: list[dict[str, str]], out: Path) -> None:
    out.parent.mkdir(parents=True, exist_ok=True)
    with out.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=["id", "image", "script", "status"])
        writer.writeheader()
        writer.writerows(rows)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Build image-code pair manifest")
    parser.add_argument("folder", type=Path, help="folder with images and scripts")
    parser.add_argument("--out", type=Path, default=Path("manifest.csv"))
    args = parser.parse_args(argv)

    if not args.folder.is_dir():
        print(f"error: folder not found: {args.folder}", file=sys.stderr)
        return 1

    rows = rows_from(args.folder)
    write_csv(rows, args.out)
    complete = sum(1 for row in rows if row["status"] == "complete")
    print(f"wrote {args.out} ({complete}/{len(rows)} complete pairs)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
