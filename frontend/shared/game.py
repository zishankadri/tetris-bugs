from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from shared.ui_manager import BaseUIManager

from shared.objects.block import Block
from shared.patterns import SingletonMeta


class BaseGameManager(metaclass=SingletonMeta):
    """Game logic manager."""

    def __init__(self, cols: int, rows: int) -> None:
        self.cols, self.rows = cols, rows
        self.grid: list[list[str | None]] = [[None for _ in range(self.cols)] for _ in range(self.rows)]
        self.current_block: Block | None = None
        self.ui_manager: BaseUIManager = None

    def tick(self) -> None:
        """Advance game state by one step."""
        if not self.current_block or not self.current_block.falling:
            return

        if not self.current_block.move(0, 1, self.grid):
            self.lock_current_block()

    def spawn_block(self, text: str) -> None:
        """Create and spawn a new block."""
        new_block = Block(text, self.cols, self.rows)
        self.current_block = new_block

        self.ui_manager.render()

    def lock_current_block(self) -> None:
        """Lock current block into grid."""
        self.current_block.lock(self.grid)
        self.ui_manager.lock_visual_cells()

        self.current_block = None

    def format_grid_as_text(self) -> str:
        """Return grid contents as plain text."""
        lines = [
            "".join(cell if cell else " " for cell in row)
            for row in self.grid
            if any(cell is not None for cell in row)
        ]
        return "\n".join(lines) if lines else ""

    def format_grid_line_as_text(self, i: int) -> str:
        """Return the i-th line of the grid as text."""
        row = self.grid[i]
        return "".join(cell if cell else " " for cell in row).rstrip()

    def clear_grid(self) -> None:
        """Clear the grid by resetting all cells to None.

        Note:
            This only updates the game state; visual updates are be handled
            separately by the ui_manager.

        """
        self.current_block = None
        self.grid = [[None for _ in range(self.cols)] for _ in range(self.rows)]

    def clear_row(self, row_index: int) -> None:
        """Clear all cells in the specified row in the internal grid.

        Note:
            This only updates the game state; visual updates are be handled
            separately by the ui_manager.

        """
        self.grid[row_index] = [None for _ in range(self.cols)]
