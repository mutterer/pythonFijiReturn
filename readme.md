# Return an ImageJ object count to Python

Smart microscopy workflows are usually controlled from Python, where image analysis results can guide acquisition decisions. It can be handy to perform the analysis with an existing ImageJ macro, reusing a familiar workflow without rewriting it in Python. This example shows how to call such a macro from Python and bring its result back into the microscopy workflow.

created during the first french RTMFM-GDR Imabio smart microscopy Hackthon, Aussois, 16-20 November 2026.

Python runs the analysis macro directly through Fiji's `-batch` option and reads the printed count from standard output. No temporary files, wrapper macros, sockets, or additional Python packages are needed.

## Usage

Requirements: Python 3 and Fiji, installed by default at `/home/mutterer/apps/Fiji`.

```bash
python3 count_objects.py
python3 count_objects.py /path/to/image.tif --fiji /path/to/Fiji
```

The included sample `blobs.tif` produces:

```text
Object count: 61
```

Use the returned integer in Python:

```python
from count_objects import count_objects

count = count_objects("blobs.tif")
```

## Files

- `count_objects.py`: invokes Fiji and parses the count from stdout.
- `Macro.ijm`: opens the image, counts detected maxima, prints the count, and closes the image.
- `blobs.tif`: sample image.
- [`positions/`](positions/readme.md): an additional script and macro that return the detected x/y coordinates as a JSON positions list.

## How Fiji is called

Python calls `subprocess.run()` with an argument list equivalent to:

```bash
/home/mutterer/apps/Fiji/fiji --headless --allow-multiple -batch /absolute/path/to/Macro.ijm /absolute/path/to/blobs.tif
```

`-batch` runs the analysis macro directly. The final argument is the image path, which the macro reads with `getArgument()`. Paths are passed as separate arguments without using a shell.

`--headless` runs without a graphical interface. `--allow-multiple` starts an independent Fiji instance, ensuring Python can capture its stdout even when another Fiji instance is open. This implementation does not execute the analysis inside an existing Fiji instance: command forwarding to that instance would not connect its stdout to Python's subprocess pipe.

Python waits for Fiji to finish, captures stdout and stderr, and enforces a 120-second timeout. The default image and macro paths are resolved relative to the Python script.

## How the result returns

The macro opens the image and runs:

```java
run("Find Maxima...", "prominence=100 light output=[Point Selection]");
```

The `light` option selects a light background for detecting dark objects. The macro counts the coordinates of the resulting point selection, or uses zero if no point selection exists. It prints a labeled line:

```text
OBJECT_COUNT=61
```

Python searches the captured stdout for `OBJECT_COUNT=`, converts the value with `int()`, and returns it from `count_objects()`. The prefix distinguishes the result from Fiji startup and diagnostic messages.

The macro also ends with `return "" + count;`, allowing other ImageJ macros or Java callers to receive its return value. The command-line Python integration uses the printed line, since a macro return value is not automatically exposed as the subprocess result.

## Interpretation and errors

The count is the number of detected maxima, rather than segmented connected components. Adjust `prominence=100` in `Macro.ijm` for other images as needed.

Missing image or launcher paths raise `FileNotFoundError`. A failed Fiji process or missing count line raises `RuntimeError` with captured output. Exceeding the timeout raises `subprocess.TimeoutExpired`; an invalid count raises `ValueError`.
