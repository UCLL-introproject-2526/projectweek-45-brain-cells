import pygame

class PlayerInput:
    def __init__(self, left, right, jump, merge):
        self.left = left
        self.right = right
        self.jump = jump
        self.merge = merge

        self._jump_prev = False
        self._merge_prev = False

    def reset(self):
        self._jump_prev = False
        self._merge_prev = False

    def axis(self):
        keys = pygame.key.get_pressed()
        return int(keys[self.right]) - int(keys[self.left])

    def jump_pressed(self):
        keys = pygame.key.get_pressed()
        pressed = keys[self.jump] and not self._jump_prev
        self._jump_prev = keys[self.jump]
        return pressed

    def merge_pressed(self):
        keys = pygame.key.get_pressed()
        pressed = keys[self.merge] and not self._merge_prev
        self._merge_prev = keys[self.merge]
        return pressed
