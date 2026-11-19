# Object positions

Run from the project root to detect objects in the sample image:

```bash
python3 positions/get_positions.py
```

Example output (first three of 61 positions):

```json
[
  {"x": 234, "y": 253},
  {"x": 176, "y": 253},
  {"x": 234, "y": 229}
]
```

To analyze another image:

```bash
python3 positions/get_positions.py /path/to/image.tif --fiji /home/mutterer/apps/Fiji
```

The script calls the ImageJ macro directly with Fiji's `-batch` option and reads the JSON positions from stdout, without temporary files. Coordinates are zero-based image pixels from the top-left corner, not microscope stage positions. No detections returns `[]`.
