class LevelManager:
    def __init__(self, levels):
        self.levels = levels
        self.index = 0
        self.current = self.levels[self.index]()

    def next_level(self):
        self.index += 1
        if self.index >= len(self.levels):
            self.index = 0
        self.current = self.levels[self.index]()
        return self.current
