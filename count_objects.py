#!/usr/bin/env python3
"""Run an ImageJ analysis macro directly with -batch and read its stdout."""

import argparse
from pathlib import Path
import subprocess

HERE = Path(__file__).resolve().parent


def count_objects(image_path=HERE / "blobs.tif", fiji_path="/home/mutterer/apps/Fiji"):
    """Return the macro's printed count as an int, without temporary files."""
    image_path = Path(image_path).resolve(strict=True)
    launcher = Path(fiji_path).resolve() / "fiji"
    if not launcher.is_file():
        raise FileNotFoundError(f"Fiji launcher not found: {launcher}")
    process = subprocess.run(
        [str(launcher), "--headless", "--allow-multiple", "-batch",
         str(HERE / "Macro.ijm"), str(image_path)],
        capture_output=True, text=True, timeout=120,
    )
    if process.returncode == 0:
        for line in reversed(process.stdout.splitlines()):
            if line.startswith("OBJECT_COUNT="):
                return int(line.removeprefix("OBJECT_COUNT="))
    raise RuntimeError(
        f"Fiji did not return an object count (exit {process.returncode}).\n"
        f"{process.stdout}\n{process.stderr}"
    )


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("image", nargs="?", type=Path, default=HERE / "blobs.tif")
    parser.add_argument("--fiji", type=Path, default=Path("/home/mutterer/apps/Fiji"))
    args = parser.parse_args()
    print(f"Object count: {count_objects(args.image, args.fiji)}")
