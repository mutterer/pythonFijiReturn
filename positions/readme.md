# Return object positions as JSON

This example uses the same Find Maxima settings as the object-count example, but returns the `xs` and `ys` coordinates as a JSON list of positions. Each entry pairs `xs[i]` with `ys[i]`:

```json
[{"x": 12, "y": 34}, {"x": 56, "y": 78}]
```

These coordinates illustrate the format. Coordinates are zero-based image pixels, measured from the top-left corner: x increases to the right and y increases downward. They are not calibrated microscope stage positions. No detections produces an empty list, `[]`.

From the project root:

```bash
python3 positions/get_positions.py
python3 positions/get_positions.py /path/to/image.tif --fiji /path/to/Fiji
```

To use the positions in Python from the project root:

```python
from positions.get_positions import get_positions

positions = get_positions("blobs.tif")
xs = [point["x"] for point in positions]
ys = [point["y"] for point in positions]
```

Python directly invokes `fiji --headless --allow-multiple -batch positions/positions.ijm <image path>`. The macro opens the image, runs Find Maxima with `prominence=100 light`, retrieves the `xs` and `ys` arrays with `getSelectionCoordinates()`, and builds the JSON list. It prints `POSITIONS=<JSON>` and also returns the JSON string to ImageJ callers.

Python captures stdout, finds the labeled line, and uses `json.loads()` to return a Python list of dictionaries. The command-line script prints that list as formatted JSON. There are no temporary files or wrapper macros. The sample image defaults to `../blobs.tif` relative to this script; all paths are resolved independently of the working directory. Requirements and timeout behavior are the same as the root example.
