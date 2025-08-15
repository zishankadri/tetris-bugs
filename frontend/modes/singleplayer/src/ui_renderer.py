from __future__ import annotations

from datetime import UTC, datetime
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from game import GameManager
from js import URL, Blob, console, document


class GridRenderer:
    """Handles rendering and UI interactions for the game."""

    def __init__(self, game: GameManager) -> None:
        self.game = game
        self.cells: list[list] = []
        self._last_rendered_grid: list[list[str | None]] = [[None for _ in range(game.cols)] for _ in range(game.rows)]

    def create_visual_grid(self) -> None:
        """Create the visual grid in DOM."""
        game_div = document.getElementById("game")
        fragment = document.createDocumentFragment()

        for _y in range(self.game.rows):
            row = []
            for _x in range(self.game.cols):
                cell = document.createElement("div")
                cell.classList.add("cell")
                fragment.appendChild(cell)
                row.append(cell)
            self.cells.append(row)

        game_div.appendChild(fragment)

    def render(self) -> None:
        """Update only cells that have changed to match the current game state."""
        combined_grid = [row.copy() for row in self.game.grid]

        if self.game.current_block and self.game.current_block.falling:
            for i, ch in enumerate(self.game.current_block.text):
                tx = self.game.current_block.x + i
                ty = self.game.current_block.y
                if 0 <= tx < self.game.cols and 0 <= ty < self.game.rows:
                    combined_grid[ty][tx] = ch

        for y in range(self.game.rows):
            for x in range(self.game.cols):
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

    def save_grid_code_to_file(self) -> None:
        """Prompt user to download current grid code."""
        saved_code = self.game.format_grid_as_text()
        blob = Blob.new([saved_code], {"type": "text/x-python"})
        url = URL.createObjectURL(blob)

        download_link = document.createElement("a")
        download_link.href = url
        timestamp = datetime.now(UTC).strftime("%Y-%m-%d_%H-%M-%S")
        download_link.download = f"tetris_code_{timestamp}.py"
        download_link.style.display = "none"

        document.body.appendChild(download_link)
        download_link.click()
        document.body.removeChild(download_link)
        URL.revokeObjectURL(url)

    def clear_row(self, row_index: int) -> None:
        """Clear all cells in a specific row of the game grid.

        This will set all elements in the row to None in the game's internal
        grid representation and update the visual representation on the DOM.

        Args:
            row_index (int): The index of the row to clear (0-based).

        """
        # Clear the internal grid data
        self.game.clear_row(row_index)

        console.log("row_index")
        console.log(row_index)
        # Clear the visual cells
        for x in range(self.game.cols):
            cell = self.cells[row_index][x]
            console.log(cell.textContent)

            cell.className = "cell"
            cell.style.background = ""
            cell.style.color = ""
            cell.textContent = ""

        # Update last rendered grid to reflect cleared state
        self._last_rendered_grid[row_index] = [None for _ in range(self.game.cols)]
        self.render()
