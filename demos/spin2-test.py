import sys
import matrix_library as matrix
import time

controller = matrix.Controller()
canvas = matrix.Canvas()

exited = False
thickness = 2
triangle = matrix.PolygonOutline(
    matrix.get_polygon_vertices(3, 20, (32, 32)), (255, 0, 0), thickness
)
square = matrix.PolygonOutline(
    matrix.get_polygon_vertices(4, 20, (96, 32)), (0, 255, 0), thickness
)
pentagon = matrix.PolygonOutline(
    matrix.get_polygon_vertices(5, 20, (64, 64)), (0, 0, 255), thickness
)
hexagon = matrix.PolygonOutline(
    matrix.get_polygon_vertices(6, 20, (32, 96)), (255, 255, 0), thickness
)
heptagon = matrix.PolygonOutline(
    matrix.get_polygon_vertices(7, 20, (96, 96)), (0, 255, 255), thickness
)

polygons = [triangle, square, pentagon, hexagon, heptagon]

def exit_prog():
    global canvas, exited
    print("quit")
    canvas.clear()
    canvas.draw()
    time.sleep(0.15)
    exited = True

controller.add_function("START", exit_prog)

counter = 0
while counter <= 20:

    # check if exited
    if exited: sys.exit(0)

    canvas.clear()
    for polygon in polygons:
        polygon.rotate(1, (polygon.center[0], polygon.center[1]))
        canvas.add(polygon)
    canvas.draw()
    time.sleep(0.25)
    counter += 1
