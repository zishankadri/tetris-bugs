from __future__ import annotations

from typing import TYPE_CHECKING

from constants import MAX_BLOCK_LENGTH

if TYPE_CHECKING:
    from game import GameManager
    from ui_manager import UIManager

from js import HTMLInputElement, KeyboardEvent, document


class Controller:
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
        # Ignore input if typing in text box
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

    # Mode-specific
    # TODO: Everything above will be abstracted in the next refactor
    def handle_input(self, evt: KeyboardEvent, input_box: HTMLInputElement) -> None:
        """Spawn a new block when Enter is pressed."""
        # Only allow new block if none is falling
        if self.game_manager.current_block and self.game_manager.current_block.falling:
            return
        try:
            if evt.key == "Enter":
                text = input_box.value.strip()
                if 1 <= len(text) <= MAX_BLOCK_LENGTH:
                    self.game_manager.spawn_block(text)
                    input_box.value = ""
                    input_box.blur()
                    self.ui_manager.render()
        except AttributeError:
            pass
