from __future__ import annotations

import copy

from shared.game import BaseGameManager

Grid = list[list[str | None]]


class GameManager(BaseGameManager):
    """Game logic manager."""

    def __init__(self, *args: int, **kwargs: int) -> None:
        super().__init__(*args, **kwargs)
        self.undo_stack: list[Grid] = []
        self.redo_stack: list[Grid] = []

    def lock_current_block(self) -> None:
        """Lock current block into grid and add last state to undo history."""
        self.undo_stack.append(copy.deepcopy(self.grid))

        super().lock_current_block()

    def undo(self) -> None:
        """Undo block placement in the grid."""
        if not self.undo_stack:
            return
        self.redo_stack.append(copy.deepcopy(self.grid))
        self.grid = self.undo_stack.pop()
        self.ui_manager.render()

    def redo(self) -> None:
        """Redo block placement in the grid."""
        if not self.redo_stack:
            return
        self.undo_stack.append(copy.deepcopy(self.grid))
        self.grid = self.redo_stack.pop()
        self.ui_manager.render()


game_manager = GameManager(40, 20)
