// Receive the image path directly from Fiji's -batch argument.
open(getArgument());
run("Find Maxima...", "prominence=100 light output=[Point Selection]");
positions = "[";
if (selectionType() == 10) {
    getSelectionCoordinates(xs, ys);
    for (i = 0; i < xs.length; i++) {
        if (i > 0) positions += ",";
        positions += "{\"x\":" + d2s(xs[i], 0) + ",\"y\":" + d2s(ys[i], 0) + "}";
    }
}
positions += "]";
print("POSITIONS=" + positions);
close();
return positions;
