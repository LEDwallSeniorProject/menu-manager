import os
import random
import time

from matrix_library import LEDWall, Canvas, Controller, shapes

IMAGE_DIRECTORY = "/home/led/pictures"
DISPLAY_DURATION = 10


class RandomImage(LEDWall.LEDProgram):
    def __init__(self, canvas, controller):
        self.image = None
        self.image_path = None
        self.display_started = None
        super().__init__(canvas, controller, trackFPS=False, fps=15)

    def preLoop(self):
        self.display_started = time.time()
        self.image_path = self._choose_image()

        if self.image_path:
            self.image = shapes.Image(width=128, height=128, position=[0, 0])
            try:
                self.image.loadfile(self.image_path)
            except Exception as exc:
                print(f"Failed to load image {self.image_path}: {exc}")
                self.image = None
        else:
            self.image = None

    def __draw__(self):
        if self.image is not None:
            self.canvas.add(self.image)
        else:
            fallback = shapes.Phrase("NO IMAGE", (64, 64), (255, 0, 0))
            fallback.translate(0 - fallback.get_width() / 2, -4)
            self.canvas.add(fallback)

        if (time.time() - self.display_started) >= DISPLAY_DURATION:
            self.quit()

    def __bind_controls__(self):
        self.controller.add_function("SELECT", self.quit)

    def postLoop(self):
        self.canvas.clear()
        self.canvas.draw()
        time.sleep(0.5)

    def _choose_image(self):
        if not os.path.isdir(IMAGE_DIRECTORY):
            print(f"Image directory not found: {IMAGE_DIRECTORY}")
            return None

        candidates = []
        for name in os.listdir(IMAGE_DIRECTORY):
            lower = name.lower()
            if lower.endswith(".jpg") or lower.endswith(".jpeg"):
                path = os.path.join(IMAGE_DIRECTORY, name)
                if os.path.isfile(path):
                    candidates.append(path)

        if not candidates:
            print(f"No JPEG images found in {IMAGE_DIRECTORY}")
            return None

        return random.choice(candidates)


if __name__ == "__main__":
    RandomImage(Canvas(), Controller())
