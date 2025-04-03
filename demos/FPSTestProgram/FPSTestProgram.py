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
        expected_frame_time = 1 / 60
        frames = 0
        fps_timer = 0  # Track time elapsed for FPS averaging
        fps_count = 0  # Track number of frames in the interval
        avg_fps = 0    # Store averaged FPS

        while self.running:
            current_time = time.time()
            frame_time = current_time - last_time
            elapsed_time = frame_time
            last_time = current_time

            # Accumulate FPS stats
            fps_timer += frame_time
            fps_count += 1

            # Update FPS every second
            if fps_timer >= 1:
                avg_fps = fps_count / fps_timer  # Average FPS over the past second
                fps_timer = 0
                fps_count = 0

            while elapsed_time < expected_frame_time:
                current_time = time.time()
                elapsed_time = current_time - last_time
                time.sleep(.001)

            self.__draw__(avg_fps)
            frames += 1

        self.postLoop()
        self.__unbind_controls__()

    def __draw__(self, avg_fps):
      
        self.canvas.clear()

        for polygon in self.polygons:
            polygon.rotate(1, polygon.center)

            self.canvas.add(polygon)

        fps_phrase = shapes.Phrase(f"FPS: {avg_fps:.1f}", [0,0])
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
