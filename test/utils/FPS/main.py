import sys
import matrix_library as matrix
import time

controller = matrix.Controller()
canvas = matrix.Canvas()

exited = False
thickness = 2
triangle = matrix.Polygon(matrix.get_polygon_vertices(3, 20, (32, 32)), (255, 0, 0))
square = matrix.Polygon(matrix.get_polygon_vertices(4, 20, (96, 32)), (0, 255, 0))
pentagon = matrix.Polygon(matrix.get_polygon_vertices(5, 20, (64, 64)), (0, 0, 255))
hexagon = matrix.Polygon(matrix.get_polygon_vertices(6, 20, (32, 96)), (255, 255, 0))
heptagon = matrix.Polygon(matrix.get_polygon_vertices(7, 20, (96, 96)), (0, 255, 255))

fps_text = matrix.Phrase("FPS: ...", [0, 0])

polygons = [triangle, square, pentagon, hexagon, heptagon]

clear_times = []
rotate_times = []
add_times = []
add_all_times = []
draw_times = []
frame_times = []

frame = 0

def exit_prog():
    global canvas, exited
    print("quit")
    canvas.clear()
    canvas.draw()
    time.sleep(0.15)
    exited = True

controller.add_function("START", exit_prog)

while True:
    if exited: sys.exit(0)
    # if frame % 100 == 0 and frame != 0:
    #     print(f"Frame {frame}")
    #     print(f"Clear: {sum(clear_times) / len(clear_times)}")
    #     print(f"Rotate: {sum(rotate_times) / len(rotate_times)}")
    #     print(f"Add: {sum(add_times) / len(add_times)}")
    #     print(f"Add All: {sum(add_all_times) / len(add_all_times)}")
    #     print(f"Draw: {sum(draw_times) / len(draw_times)}")
    #     print(f"Frame: {sum(frame_times) / len(frame_times)}")
    #     print(f"Avg FPS: {1 / (sum(frame_times) / len(frame_times))}")

    frame_start = time.perf_counter()
    canvas.clear()
    clear_end = time.perf_counter()
    clear_times.append(clear_end - frame_start)

    add_all_start = time.perf_counter()
    for polygon in polygons:
        rotate_start = time.perf_counter()
        polygon.rotate(1, (polygon.center[0], polygon.center[1]))

        rotate_times.append(time.perf_counter() - rotate_start)

        add_start = time.perf_counter()
        canvas.add(polygon)
        add_times.append(time.perf_counter() - add_start)
    if frame != 0:
        fps_text.set_text(f"FPS: {1 / (sum(frame_times) / len(frame_times)):.2f}")
    canvas.add(fps_text)

    add_all_times.append(time.perf_counter() - add_all_start)

    draw_start = time.perf_counter()
    canvas.draw()
    draw_times.append(time.perf_counter() - draw_start)

    # Total time for the frame
    frame_end = time.perf_counter()
    frame_times.append(frame_end - frame_start)

    frame += 1
