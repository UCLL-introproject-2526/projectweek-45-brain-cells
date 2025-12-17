import pygame
import copy


class EditorState:
    def __init__(self, grid_w=60, grid_h=20):
        self.grid_w = grid_w
        self.grid_h = grid_h

        self.map_data = [
            [" " for _ in range(grid_w)]
            for _ in range(grid_h)
        ]

        # metadata
        self.level_name = "New Level"
        self.background_path = ""

        # tool
        self.selected_tool = 0

        # undo / redo
        self.undo_stack = []
        self.redo_stack = []

    # -------------------------
    # UNDO SYSTEM
    # -------------------------
    def snapshot(self):
        """Save current state for undo."""
        self.undo_stack.append(copy.deepcopy(self.map_data))
        self.redo_stack.clear()

    def undo(self):
        if not self.undo_stack:
            return
        self.redo_stack.append(copy.deepcopy(self.map_data))
        self.map_data = self.undo_stack.pop()

    def redo(self):
        if not self.redo_stack:
            return
        self.undo_stack.append(copy.deepcopy(self.map_data))
        self.map_data = self.redo_stack.pop()

    # -------------------------
    # GRID HELPERS
    # -------------------------
    def in_bounds(self, cx, cy):
        return 0 <= cx < self.grid_w and 0 <= cy < self.grid_h

    def set_cell(self, cx, cy, value):
        if self.in_bounds(cx, cy):
            if self.map_data[cy][cx] != value:
                self.snapshot()
                self.map_data[cy][cx] = value

    def clear_cell(self, cx, cy):
        if self.in_bounds(cx, cy) and self.map_data[cy][cx] != " ":
            self.snapshot()
            self.map_data[cy][cx] = " "
