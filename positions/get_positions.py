#!/usr/bin/env python3
"""Run the ImageJ positions macro and return its JSON positions list to Python."""

import argparse
import json
from pathlib import Path
import subprocess

HERE = Path(__file__).resolve().parent


def get_positions(image_path=HERE.parent / "blobs.tif", fiji_path="/home/mutterer/apps/Fiji"):
    """Return a list of {x, y} pixel coordinates, with no temporary files."""
    image_path = Path(image_path).resolve(strict=True)
    launcher = Path(fiji_path).resolve() / "fiji"
    if not launcher.is_file():
        raise FileNotFoundError(f"Fiji launcher not found: {launcher}")
    process = subprocess.run(
        [str(launcher), "--headless", "--allow-multiple", "-batch",
         str(HERE / "positions.ijm"), str(image_path)],
        capture_output=True, text=True, timeout=120,
    )
    if process.returncode == 0:
        for line in reversed(process.stdout.splitlines()):
            if line.startswith("POSITIONS="):
                return json.loads(line.removeprefix("POSITIONS="))
    raise RuntimeError(
        f"Fiji did not return positions (exit {process.returncode}).\n"
        f"{process.stdout}\n{process.stderr}"
    )


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("image", nargs="?", type=Path, default=HERE.parent / "blobs.tif")
    parser.add_argument("--fiji", type=Path, default=Path("/home/mutterer/apps/Fiji"))
    args = parser.parse_args()
    print(json.dumps(get_positions(args.image, args.fiji), indent=2))
