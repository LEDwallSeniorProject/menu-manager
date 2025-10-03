import os
import random
import time

from matrix_library import LEDWall, Canvas, Controller, shapes

IMAGE_DIRECTORY = "/home/led/pictures"
DISPLAY_DURATION = 10
STATUS_COLOR = (255, 255, 0)
ERROR_COLOR = (255, 0, 0)
LOG_PATH = "/tmp/random_image.log"

class RandomImage(LEDWall.LEDProgram):
    def __init__(self, canvas, controller):
        self.image = None
        self.image_path = None
        self.display_started = None
        self.status_text = ""
        super().__init__(canvas, controller, trackFPS=False, fps=15)

    def preLoop(self):
        self.image_path = self._choose_image()

        if self.image_path:
            self.image = shapes.Image(width=128, height=128, position=[0, 0])
            try:
                self.image.loadfile(self.image_path)
                filename = os.path.basename(self.image_path)
                self.status_text = f"Showing {filename}"
                self._log(f"Loaded image: {self.image_path}")
            except Exception as exc:
                self._log(f"Failed to load image {self.image_path}: {exc}")
                self.status_text = "Load failed"
                self.image = None
        else:
            self.image = None
            self.status_text = "No images found"

        self.display_started = time.time()

    def __draw__(self):
        if self.image is not None:
            self.canvas.add(self.image)
            self.canvas.draw()
        else:
            fallback = shapes.Phrase("NO IMAGE", (64, 60), ERROR_COLOR, size=1.5)
            fallback.translate(0 - fallback.get_width() / 2, 0)
            self.canvas.add(fallback)
            self.canvas.draw()

        if self.status_text:
            status_color = STATUS_COLOR if self.image is not None else ERROR_COLOR
            status = shapes.Phrase(self.status_text, (2, 118), status_color)
            self.canvas.add(status)
            self.canvas.draw()

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
            self._log(f"Image directory not found: {IMAGE_DIRECTORY}")
            return None

        candidates = []
        for name in os.listdir(IMAGE_DIRECTORY):
            lower = name.lower()
            if lower.endswith(".jpg") or lower.endswith(".jpeg"):
                path = os.path.join(IMAGE_DIRECTORY, name)
                if os.path.isfile(path):
                    candidates.append(path)

        if not candidates:
            self._log(f"No JPEG images found in {IMAGE_DIRECTORY}")
            return None

        return random.choice(candidates)

    def _log(self, message):
        timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
        try:
            with open(LOG_PATH, "a", encoding="utf-8") as handle:
                handle.write(f"[{timestamp}] {message}\n")
        except Exception:
            pass


if __name__ == "__main__":
    RandomImage(Canvas(), Controller())
