from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from shared.game import GameManager
    from shared.ui_manager import UIManager

from js import KeyboardEvent, document


class BaseController:
    """Handles user input and mediates interactions between the game state and the UI.

    Attributes:
        game_manager (GameManager): The game state manager instance.
        ui_manager (UIManager): The ui_manager responsible for updating the visual grid.

    """

    def __init__(self, game_manager: GameManager, ui_manager: UIManager) -> None:
        self.game_manager = game_manager
        self.ui_manager = ui_manager

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
        elif evt.key == " ":
            evt.preventDefault()
            self.game_manager.lock_current_block()
            moved = True

        if moved:
            self.ui_manager.render()
