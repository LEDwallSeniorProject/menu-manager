from matrix_library import LEDWall, Canvas, Controller, shapes
import time


class FPSTestProgram(LEDWall.LEDProgram):
    def __init__(self, canvas, controller):
        self.frame = 0
        self.max_frames = 200

        self.clear_times = []
        self.rotate_times = []
        self.add_times = []
        self.add_all_times = []
        self.draw_times = []
        self.frame_times = []

        self.fps_text = shapes.Phrase("FPS: ...", [0, 0])

        self.polygons = [
            shapes.Polygon(shapes.get_polygon_vertices(3, 20, (32, 32)), (255, 0, 0)),
            shapes.Polygon(shapes.get_polygon_vertices(4, 20, (96, 32)), (0, 255, 0)),
            shapes.Polygon(shapes.get_polygon_vertices(5, 20, (64, 64)), (0, 0, 255)),
            shapes.Polygon(shapes.get_polygon_vertices(6, 20, (32, 96)), (255, 255, 0)),
            shapes.Polygon(shapes.get_polygon_vertices(7, 20, (96, 96)), (0, 255, 255)),
        ]

        super().__init__(canvas, controller)

    def __draw__(self):
        if self.frame >= self.max_frames:
            self.stop()
            return

        frame_start = time.perf_counter()
        self.canvas.clear()
        clear_end = time.perf_counter()
        self.clear_times.append(clear_end - frame_start)

        add_all_start = time.perf_counter()
        for polygon in self.polygons:
            rotate_start = time.perf_counter()
            polygon.rotate(1, polygon.center)
            self.rotate_times.append(time.perf_counter() - rotate_start)

            add_start = time.perf_counter()
            self.canvas.add(polygon)
            self.add_times.append(time.perf_counter() - add_start)

        if self.frame > 0:
            avg_frame_time = sum(self.frame_times) / len(self.frame_times)
            fps = 1 / avg_frame_time
            self.fps_text.set_text(f"FPS: {fps:.2f}")

        self.canvas.add(self.fps_text)
        self.add_all_times.append(time.perf_counter() - add_all_start)

        draw_start = time.perf_counter()
        self.canvas.draw()
        self.draw_times.append(time.perf_counter() - draw_start)

        self.frame_times.append(time.perf_counter() - frame_start)
        self.frame += 1

    def __bind_controls__(self):
        self.controller.add_function("START", self.stop)

    def postLoop(self):
        self.canvas.clear()
        self.canvas.draw()
        time.sleep(0.5)

        # 🟡 Performans çıktıları yorum satırına alındı (gerekirse açabilirsin)
        # if self.frame_times:
        #     avg_fps = 1 / (sum(self.frame_times) / len(self.frame_times))
        #     print(f"Avg FPS: {avg_fps:.2f}")
        #     print(f"Frame Count: {self.frame}")
        #     print(f"Clear avg: {sum(self.clear_times)/len(self.clear_times):.6f}s")
        #     print(f"Rotate avg: {sum(self.rotate_times)/len(self.rotate_times):.6f}s")
        #     print(f"Add avg: {sum(self.add_times)/len(self.add_times):.6f}s")
        #     print(f"Add All avg: {sum(self.add_all_times)/len(self.add_all_times):.6f}s")
        #     print(f"Draw avg: {sum(self.draw_times)/len(self.draw_times):.6f}s")
        #     print(f"Frame avg: {sum(self.frame_times)/len(self.frame_times):.6f}s")


if __name__ == "__main__":
    FPSTestProgram(Canvas(), Controller())
