from datetime import datetime
import time
from matrix_library import LEDWall, Canvas, Controller, Line, CircleOutline


class ClockProgram(LEDWall.LEDProgram):
    def __init__(self, canvas, controller):
        self.timer = 0
        self.max_time = 10  # saniye

        # saat dairesi
        self.circle = CircleOutline(64, (64, 64), (255, 255, 255))

        # saat üzerindeki 12 işaret
        self.markers = []
        for i in range(12):
            marker = Line((64, 16), (64, 8), (255, 255, 255))
            marker.rotate(i * 30, (64, 64))
            self.markers.append(marker)

        super().__init__(canvas, controller)

    def __draw__(self):
        if self.timer >= self.max_time:
            self.stop()
            return

        now = datetime.now()
        hour = now.hour % 12
        minute = now.minute
        second = now.second
        millisecond = now.microsecond / 1000

        hour_angle = hour * 30 + (minute / 60) * 30
        minute_angle = minute * 6 + (second / 60) * 6
        second_angle = second * 6 + (millisecond / 1000) * 6

        # Akrep, yelkovan, saniye çizgileri
        hour_hand = Line((64, 64), (64, 24), (255, 0, 0))
        hour_hand.rotate(hour_angle, (64, 64))

        minute_hand = Line((64, 64), (64, 20), (0, 255, 0))
        minute_hand.rotate(minute_angle, (64, 64))

        second_hand = Line((64, 64), (64, 16), (0, 0, 255))
        second_hand.rotate(second_angle, (64, 64))

        # Ekranı temizle ve yeniden çiz
        self.canvas.clear()
        self.canvas.add(self.circle)
        for marker in self.markers:
            self.canvas.add(marker)
        self.canvas.add(hour_hand)
        self.canvas.add(minute_hand)
        self.canvas.add(second_hand)
        self.canvas.draw()

        self.timer += 1
        time.sleep(1)  # saniyede bir güncellenen saat

    def __bind_controls__(self):
        self.controller.add_function("START", self.stop)

    def postLoop(self):
        self.canvas.clear()
        self.canvas.draw()
        time.sleep(0.5)


# Programı çalıştır
if __name__ == "__main__":
    ClockProgram(Canvas(), Controller())
