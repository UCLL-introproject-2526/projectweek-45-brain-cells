import pygame

class MergeEffect:
    def __init__(self, pos):
        self.pos = pygame.Vector2(pos)
        self.time = 0.0
        self.duration = 0.25
        self.done = False

    def update(self, dt):
        self.time += dt
        if self.time >= self.duration:
            self.done = True

    def draw(self, surface, camera_offset):
        t = self.time / self.duration
        scale = 1.0 + 0.8 * (1 - t)
        alpha = int(255 * (1 - t))

        radius = int(30 * scale)
        glow = pygame.Surface((radius*2, radius*2), pygame.SRCALPHA)
        pygame.draw.circle(glow, (200, 100, 255, alpha), (radius, radius), radius)
        surface.blit(
            glow,
            (self.pos.x - radius - camera_offset[0],
             self.pos.y - radius - camera_offset[1])
        )
