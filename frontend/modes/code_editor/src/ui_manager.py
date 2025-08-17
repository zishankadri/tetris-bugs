from __future__ import annotations

from js import document
from shared.ui_manager import BaseUIManager


class UIManager(BaseUIManager):
    """Handles rendering and UI interactions for the game."""

    def lock_visual_cells(self, *args, **kwargs) -> None:  # noqa: ANN002, ANN003
        """Lock the cells occupied by the current block visually."""
        super().lock_visual_cells(*args, **kwargs)

        # Focus the input field
        input_box = document.getElementById("text-input")
        input_box.focus()
