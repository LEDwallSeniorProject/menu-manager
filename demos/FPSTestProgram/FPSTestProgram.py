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

        super().__init__(canvas, controller, trackFPS=True, fps=60)

    def __draw__(self):   
        for polygon in self.polygons:
            polygon.rotate(1, polygon.center)

            self.canvas.add(polygon)


    def __bind_controls__(self):
        self.controller.add_function("SELECT", self.quit)

    def postLoop(self):
        self.canvas.clear()
        self.canvas.draw()
        time.sleep(0.5)

if __name__ == "__main__":
    FPSTestProgram(Canvas(), Controller())
