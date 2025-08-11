from typing import TYPE_CHECKING

from js import document
from standard import SingletonMeta

if TYPE_CHECKING:
    from block import Block


class GameManager(metaclass=SingletonMeta):  # noqa: D101
    def __init__(self) -> None:
        # Grid size
        self.cols, self.rows = 40, 20
        self.grid = [[None for _ in range(self.cols)] for _ in range(self.rows)]
        self.current_block: Block | None = None

        # Create visual grid
        game_div = document.getElementById("game")
        self.cells = []
        fragment = document.createDocumentFragment()
        for _y in range(self.rows):
            row = []
            for _x in range(self.cols):
                cell = document.createElement("div")
                cell.classList.add("cell")
                fragment.appendChild(cell)
                row.append(cell)
            self.cells.append(row)
        game_div.appendChild(fragment)

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
                        cell.classList.remove("block", "locked")
                        cell.style.background = ""
                        cell.style.color = ""
                        cell.textContent = ""
                    else:
                        cell.classList.add("block")
                        cell.textContent = current_char
                        cell.style.background = "lime"
                        cell.style.color = "black"

                self._last_rendered_grid[y][x] = current_char

    def tick(self) -> None:
        """Advance game state by one step."""
        if not self.current_block or not self.current_block.falling:
            return

        # Try to move block down
        if not self.current_block.move(0, 1, self.grid):
            # If can't move down, lock block and clear current_block
            self.current_block.lock(self.grid)
            self.current_block = None

        self.render()

    def format_grid_as_text(self) -> str:
        """Format the grid as a text representation."""
        return "\n".join("".join(cell if cell is not None else "." for cell in row) for row in self.grid)
