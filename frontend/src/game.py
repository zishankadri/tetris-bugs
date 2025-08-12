from datetime import UTC, datetime
from typing import TYPE_CHECKING

from js import URL, Blob, document
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

    def save_grid_code(self) -> None:
        """Save the current grid code and display it."""
        saved_code = self.format_grid_as_text()
        current_time = datetime.now(UTC).strftime("%H:%M:%S")
        text_output = document.querySelector("#text-output")
        if text_output:
            if saved_code == "":
                text_output.innerText = saved_code
            else:
                text_output.innerText = f"Saved at {current_time}:\n\n{saved_code}"

    def save_grid_code_to_file(self) -> None:
        """Open a save dialog to save the current grid code as a file."""
        saved_code = self.format_grid_as_text()
        blob = Blob.new([saved_code], {"type": "text/plain"})
        url = URL.createObjectURL(blob)
        a = document.createElement("a")
        a.href = url
        a.download = f"tetris_code_{datetime.now(UTC).strftime('%Y%m%d_%H%M%S')}.py"
        a.style.display = "none"
        document.body.appendChild(a)
        a.click()
        document.body.removeChild(a)
        URL.revokeObjectURL(url)

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
        lines = []
        for row in self.grid:
            line = "".join(cell if cell is not None else " " for cell in row)
            # Only add non-empty lines
            if line.strip():
                lines.append(line)
        return "\n".join(lines) if lines else ""
