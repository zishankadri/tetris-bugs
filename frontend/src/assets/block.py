from random import randint

from constants import MAX_BLOCK_LENGTH


class Block:
    """Represents a horizontal text block moving on a grid."""

    def __init__(self, text: str, grid_cols: int, grid_rows: int) -> None:
        self.text = text[: min(MAX_BLOCK_LENGTH, grid_cols)]
        self.cols = grid_cols
        self.rows = grid_rows
        # Spawns blocks randomly along the x-axis.
        self.x = randint(0, self.cols - len(self.text))  # noqa: S311
        self.y = 0
        self.falling = True

    def can_move(self, dx: int, dy: int, grid: list[list[str | None]]) -> bool:
        """Check if move is valid."""
        new_x = self.x + dx
        new_y = self.y + dy
        for i in range(len(self.text)):
            tx, ty = new_x + i, new_y
            if tx < 0 or tx >= self.cols or ty >= self.rows:
                return False
            if ty >= 0 and grid[ty][tx] is not None:
                return False
        return True

    def move(self, dx: int, dy: int, grid: list[list[str | None]]) -> bool:
        """Try moving the block, return True if moved."""
        if self.can_move(dx, dy, grid):
            # Update position if move is valid
            self.x += dx
            self.y += dy
            return True
        return False

    def lock(self, grid: list[list[str | None]]) -> None:
        """Place the block into the grid and stop it from falling."""
        for i, ch in enumerate(self.text):
            tx = self.x + i
            ty = self.y
            if 0 <= tx < self.cols and 0 <= ty < self.rows:
                grid[ty][tx] = ch
        self.falling = False
