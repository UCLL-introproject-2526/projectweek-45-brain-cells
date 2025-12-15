import pygame

class PlayerInput:
    def __init__(self, left, right, jump, merge):
        self.left = left
        self.right = right
        self.jump = jump
        self.merge = merge

        self._jump_was_down = False
        self._merge_was_down = False

    def axis(self):
        keys = pygame.key.get_pressed()
        return (1 if keys[self.right] else 0) - (1 if keys[self.left] else 0)

    def jump_pressed(self):
        keys = pygame.key.get_pressed()
        down = keys[self.jump]
        pressed = down and not self._jump_was_down
        self._jump_was_down = down
        return pressed

    def merge_pressed(self):
        keys = pygame.key.get_pressed()
        down = keys[self.merge]
        pressed = down and not self._merge_was_down
        self._merge_was_down = down
        return pressed
