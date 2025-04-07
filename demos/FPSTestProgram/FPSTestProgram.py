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
        last = time.time()
        max_fps = 60
        max_frame_time = 1 / max_fps
        expected_frame_time = max_frame_time
        start = last
        fps_count = 0
        fps_time = 0
        avg_fps = 0

        while self.running:
            start_time = time.time()
            
            self.__draw__(avg_fps)
            
            elapsed = time.time() - start_time
            sleep_time = expected_frame_time - elapsed

            if sleep_time > 0:
                time.sleep(sleep_time)
            
            now = time.time()
            dif = now - last
            last = now

            fps_time += dif
            fps_count += 1

            if fps_time >= 1:
                avg_fps = fps_count
                fps_count = 0
                fps_time = 0

                if avg_fps > max_fps:
                    expected_frame_time += max_frame_time * 0.05
                elif (max_fps - avg_fps) > 3:
                    expected_frame_time -= max_frame_time * 0.01
                
        self.postLoop()
        self.__unbind_controls__()

    def __draw__(self, avg_fps):
      
        self.canvas.clear()

        for polygon in self.polygons:
            polygon.rotate(1, polygon.center)

            self.canvas.add(polygon)

        fps_phrase = shapes.Phrase(f"FPS: {avg_fps:.0f}", [0,0])
        self.canvas.add(fps_phrase)

        self.canvas.draw()

    def __bind_controls__(self):
        self.controller.add_function("SELECT", self.quit)

    def postLoop(self):
        self.canvas.clear()
        self.canvas.draw()
        time.sleep(0.5)

if __name__ == "__main__":
    FPSTestProgram(Canvas(), Controller())
