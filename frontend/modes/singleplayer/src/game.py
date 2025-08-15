from block import Block
from js import HTMLElement  # PyScript exposes js.HTMLElement
from patterns import SingletonMeta


class GameManager(metaclass=SingletonMeta):  # noqa: D101
    def __init__(self) -> None:
        # Grid size
        self.cols, self.rows = 40, 20
        self.grid = [[None for _ in range(self.cols)] for _ in range(self.rows)]
        self.current_block: Block | None = None
        self.cells = []

        # Keep track of last rendered state to minimize DOM updates
        self._last_rendered_grid = [[None for _ in range(self.cols)] for _ in range(self.rows)]

    def render(self) -> None:
        """Render grid and current block efficiently by updating only changed cells."""
        # Copy current grid state including current_block overlay
        combined_grid = [row.copy() for row in self.grid]

        if self.current_block and self.current_block.falling:
            for i, ch in enumerate(self.current_block.text):
                tx = self.current_block.x + i
                ty = self.current_block.y
                if 0 <= tx < self.cols and 0 <= ty < self.rows:
                    combined_grid[ty][tx] = ch

        # Update only changed cells
        for y in range(self.rows):
            for x in range(self.cols):
                cell = self.cells[y][x]
                current_char = combined_grid[y][x]
                last_char = self._last_rendered_grid[y][x]

                if current_char != last_char:
                    if current_char is None:
                        cell.className = "cell"
                        cell.style.background = ""
                        cell.style.color = ""
                        cell.textContent = ""
                    else:
                        cell.className = "block"
                        cell.textContent = current_char

                self._last_rendered_grid[y][x] = current_char

    def tick(self) -> None:
        """Advance game state by one step."""
        if not self.current_block or not self.current_block.falling:
            return

        # Try to move block down
        if not self.current_block.move(0, 1, self.grid):
            # If can't move down, lock block and clear current_block
            self.current_block.lock(self.grid)
            self.lock_visual_cells()
            self.current_block = None
        self.render()

    def format_grid_as_text(self) -> str:
        """Format the grid as a text representation."""
        lines = []
        for row in self.grid:
            line = "".join(cell if cell is not None else " " for cell in row)
            # Only add non-empty lines
            if line.strip():
                lines.append(line)
        return "\n".join(lines) if lines else ""

    def spawn_block(self, text: str) -> None:
        """Spawn a block in the frontend."""
        new_block = Block(text, game_manager.cols, game_manager.rows)
        game_manager.current_block = new_block
        game_manager.render()

    def get_block_cells(self) -> list[HTMLElement]:
        """Return DOM elements corresponding to the current block."""
        if not self.current_block:
            return []
        return [self.cells[y][x] for x, y in self.current_block.get_cells_coords()]

    def lock_visual_cells(self) -> None:
        """Lock the cells occupied by the current block visually and focus the input."""
        cords = self.current_block.get_cells_coords()
        for cord in cords:
            cell = self.cells[cord[1]][cord[0]]
            cell.className = "locked-cell"


game_manager = GameManager()
