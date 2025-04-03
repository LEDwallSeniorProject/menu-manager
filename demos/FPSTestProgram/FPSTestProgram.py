from matrix_library import LEDWall, Canvas, Controller, shapes
import time


class FPSTestProgram(LEDWall.LEDProgram):
    def __init__(self, canvas, controller):
        self.polygons = [
            shapes.Polygon(shapes.get_polygon_vertices(3, 20, (32, 32)), (255, 0, 0)),
            shapes.Polygon(shapes.get_polygon_vertices(4, 20, (96, 32)), (0, 255, 0)),
            shapes.Polygon(shapes.get_polygon_vertices(5, 20, (64, 64)), (0, 0, 255)),
            shapes.Polygon(shapes.get_polygon_vertices(6, 20, (32, 96)), (255, 255, 0)),
            shapes.Polygon(shapes.get_polygon_vertices(7, 20, (96, 96)), (0, 255, 255)),
        ]

        super().__init__(canvas, controller)

    def __loop__(self):
        self.preLoop()
        last_time = time.time()
        frame_time = 1 / 60
        frames = 0

        while self.running:
            current_time = time.time()
            elapsed_time = current_time - last_time

            while elapsed_time < frame_time:
                current_time = time.time()
                elapsed_time = current_time - last_time
                time.sleep(.001)

            self.__draw__(frames, last_time)
            frames += 1
            last_time = current_time

        self.postLoop()
        self.__unbind_controls__()

    def __draw__(self, frames, last_time):
      
        self.canvas.clear()

        for polygon in self.polygons:
            polygon.rotate(1, polygon.center)

            self.canvas.add(polygon)

        frame_time = time.time()-last_time
        avg_fps = 1/frame_time

        fps_phrase = shapes.Phrase(f"FPS: {avg_fps:.1f}", [0,0])
        self.canvas.add(fps_phrase)

        self.canvas.draw()

    def __bind_controls__(self):
        self.controller.add_function("SELECT", self.quit)

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
