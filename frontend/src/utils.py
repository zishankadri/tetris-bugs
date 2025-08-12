from __future__ import annotations

from datetime import UTC, datetime
from typing import TYPE_CHECKING

from js import URL, Blob, document

if TYPE_CHECKING:
    from game_manager import GameManager


def create_visual_grid(game_manager: GameManager) -> None:
    """Create visual grid."""
    game_div = document.getElementById("game")
    fragment = document.createDocumentFragment()
    for _y in range(game_manager.rows):
        row = []
        for _x in range(game_manager.cols):
            cell = document.createElement("div")
            cell.classList.add("cell")
            fragment.appendChild(cell)
            row.append(cell)
        game_manager.cells.append(row)
    game_div.appendChild(fragment)


def save_grid_code_to_file(game_manager: GameManager) -> None:
    """Open a save dialog to save the current grid code as a file."""
    saved_code = game_manager.format_grid_as_text()

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
