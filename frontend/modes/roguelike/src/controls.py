from __future__ import annotations

from engine.controls import BaseController
from js import KeyboardEvent, document


class Controller(BaseController):
    """Handles user input and mediates interactions between the game state and the UI.

    Attributes:
        game_manager (GameManager): The game state manager instance.
        ui_manager (UIManager): The ui_manager responsible for updating the visual grid.

    """

    def handle_key(self, evt: KeyboardEvent) -> None:
        """Handle arrow keys and spacebar."""
        active = document.activeElement
        if active and active.id == "text-input":
            return

        if not self.game_manager.current_block:
            return

        moved = False
        if evt.key == "ArrowLeft":
            moved = self.game_manager.current_block.move(-1, 0, self.game_manager.grid)
        elif evt.key == "ArrowRight":
            moved = self.game_manager.current_block.move(1, 0, self.game_manager.grid)
        elif evt.key == "ArrowDown":
            moved = self.game_manager.current_block.move(0, 1, self.game_manager.grid)

        if moved:
            self.ui_manager.render()
