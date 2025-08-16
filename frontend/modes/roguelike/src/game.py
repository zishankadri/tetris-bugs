from block import Block
from patterns import SingletonMeta


class GameManager(metaclass=SingletonMeta):
    """Game logic manager."""

    def __init__(self) -> None:
        self.cols, self.rows = 40, 20
        self.grid: list[list[str | None]] = [[None for _ in range(self.cols)] for _ in range(self.rows)]
        self.current_block: Block | None = None
        self.renderer = None

    def tick(self) -> None:
        """Advance game state by one step."""
        if not self.current_block or not self.current_block.falling:
            return

        if not self.current_block.move(0, 1, self.grid):
            self.lock_current_block()

    def lock_current_block(self) -> None:
        """Lock current block into grid."""
        self.current_block.lock(self.grid)
        self.renderer.lock_visual_cells()

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

    def clear_row(self, row_index: int) -> None:
        """Clear all cells in the specified row in the internal grid.

        Note:
            This only updates the game state; visual updates should be handled
            separately by the renderer.

        """
        self.grid[row_index] = [None for _ in range(self.cols)]

    def spawn_block(self, text: str) -> None:
        """Spawn a new block."""
        new_block = Block(text, self.cols, self.rows)
        self.current_block = new_block

        self.renderer.render()


game_manager = GameManager()
