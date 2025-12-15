import pygame
from core.entity import Entity
from core.physics import PhysicsBody
from settings import PLAYER_W, PLAYER_H, PLAYER_SPEED, PLAYER_JUMP


JUMP_BUFFER_TIME = 0.12
COYOTE_TIME = 0.12


class Player(Entity, PhysicsBody):
    def __init__(self, x, y, input_handler, color, name="P"):
        Entity.__init__(self, x, y, PLAYER_W, PLAYER_H)
        PhysicsBody.__init__(self)

        self.input = input_handler
        self.color = color
        self.name = name
        self.jump_buffer = 0.0
        self.coyote_timer = 0.0


    def wants_merge(self):
        return self.input.merge_pressed()

    def update(self, dt, solids, other_players):
        self.apply_gravity()

        # Horizontal movement (independent of jumping)
        self.vel.x = self.input.axis() * PLAYER_SPEED

        # Jump buffering
        if self.input.jump_pressed():
            self.jump_buffer = JUMP_BUFFER_TIME
        else:
            self.jump_buffer = max(0.0, self.jump_buffer - dt)

        # Coyote time
        if self.on_ground:
            self.coyote_timer = COYOTE_TIME
        else:
            self.coyote_timer = max(0.0, self.coyote_timer - dt)

        # Jump execution
        if self.jump_buffer > 0 and self.coyote_timer > 0:
            self.vel.y = PLAYER_JUMP
            self.jump_buffer = 0
            self.coyote_timer = 0

        self.move_and_collide(self.rect, solids, dt)
        self._collide_players(other_players)


    def _collide_players(self, others):
        # Simple resolution: separate on overlap by the shallowest axis.
        for o in others:
            if o is self:
                continue
            if not self.rect.colliderect(o.rect):
                continue

            dx_left = abs(self.rect.right - o.rect.left)
            dx_right = abs(o.rect.right - self.rect.left)
            dy_top = abs(self.rect.bottom - o.rect.top)
            dy_bottom = abs(o.rect.bottom - self.rect.top)

            min_sep = min(dx_left, dx_right, dy_top, dy_bottom)

            if min_sep == dy_top:
                # standing on them
                self.rect.bottom = o.rect.top
                self.vel.y = 0
                self.on_ground = True
            elif min_sep == dy_bottom:
                self.rect.top = o.rect.bottom
                self.vel.y = 0
            elif min_sep == dx_left:
                self.rect.right = o.rect.left
                self.vel.x = 0
            else:
                self.rect.left = o.rect.right
                self.vel.x = 0

    def draw(self, surface, camera_offset=(0, 0)):
        r = self.rect.move(-camera_offset[0], -camera_offset[1])
        pygame.draw.rect(surface, self.color, r, border_radius=6)
        pygame.draw.rect(surface, (10, 10, 10), r, 2, border_radius=6)
