from matrix_library import LEDWall, Canvas, Controller, Circle
import time


class Particle(Circle):
    def __init__(self, radius, center, color, velocity_x, velocity_y):
        super().__init__(radius, center, color)
        self.velocity_x = velocity_x
        self.velocity_y = velocity_y

    def distance_to(self, other: "Particle") -> float:
        dx = self.center[0] - other.center[0]
        dy = self.center[1] - other.center[1]
        return (dx ** 2 + dy ** 2) ** 0.5

    def hits(self, other: "Particle"):
        if self == other:
            return False
        return self.radius + other.radius >= self.distance_to(other)

    def bounce(self, other: "Particle"):
        if not self.hits(other):
            return

        m1 = self.radius**2
        m2 = other.radius**2
        m1_m2 = m1 + m2

        dx = self.center[0] - other.center[0]
        dy = self.center[1] - other.center[1]
        dist_sq = dx**2 + dy**2
        dvx = self.velocity_x - other.velocity_x
        dvy = self.velocity_y - other.velocity_y

        dot_product_2 = 2 * (dx * dvx + dy * dvy) / dist_sq
        dv1_scale = m2 / m1_m2 * dot_product_2
        dv2_scale = m1 / m1_m2 * dot_product_2

        self.velocity_x -= dv1_scale * dx
        self.velocity_y -= dv1_scale * dy
        other.velocity_x += dv2_scale * dx
        other.velocity_y += dv2_scale * dy

        dist = self.distance_to(other)
        dist_x_norm = dx / dist
        dist_y_norm = dy / dist
        intrusion_dist = (self.radius + other.radius - dist) / 2 + 1e-6

        self.translate(intrusion_dist * dist_x_norm, intrusion_dist * dist_y_norm)
        other.translate(-intrusion_dist * dist_x_norm, -intrusion_dist * dist_y_norm)


class ParticleBounce(LEDWall.LEDProgram):
    def __init__(self, canvas, controller):
        self.particles = []
        self.counter = 0
        self.max_frames = 200
        super().__init__(canvas, controller)

    def preLoop(self):
        # Başlangıç parçacıklarını oluştur
        self.particles.append(Particle(8, (32, 96), (0, 255, 0), 3, 2))
        self.particles.append(Particle(10, (96, 96), (0, 0, 255), -3, 2))
        self.particles.append(Particle(12, (64, 96), (255, 0, 0), 2, -3))
        self.particles.append(Particle(6, (64, 75), (255, 255, 0), -2, -3))

    def __draw__(self):
        if self.counter >= self.max_frames:
            self.stop()
            return

        self.canvas.clear()

        # Parçacıkları güncelle
        for particle in self.particles:
            # Kenara çarpma kontrolü
            if particle.center[1] + particle.radius >= 128 or particle.center[1] - particle.radius <= 0:
                particle.velocity_y *= -1
            if particle.center[0] + particle.radius >= 128 or particle.center[0] - particle.radius <= 0:
                particle.velocity_x *= -1
            particle.translate(particle.velocity_x, particle.velocity_y)

        # Çarpışma kontrolü
        for i in range(len(self.particles)):
            for j in range(i):
                self.particles[i].bounce(self.particles[j])

        # Çizim
        for particle in self.particles:
            self.canvas.add(particle)

        self.counter += 1

    def __bind_controls__(self):
        self.controller.add_function("START", self.stop)

    def postLoop(self):
        self.canvas.clear()
        self.canvas.draw()
        time.sleep(0.5)


# Programı başlat
if __name__ == "__main__":
    ParticleBounce(Canvas(), Controller())
