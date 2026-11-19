// The image path is passed directly as the -batch macro argument.
open(getArgument());
run("Find Maxima...", "prominence=100 light output=[Point Selection]");
count = 0;
if (selectionType() == 10) {
    getSelectionCoordinates(xs, ys);
    count = xs.length;
}
print("OBJECT_COUNT=" + count);
close();
return "" + count;
