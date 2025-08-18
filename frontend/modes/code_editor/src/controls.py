from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from js import HTMLInputElement, KeyboardEvent

from shared.constants import MAX_BLOCK_LENGTH
from shared.controls import BaseController


class Controller(BaseController):
    """Handles user input and mediates interactions between the game state and the UI.

    Attributes:
        game_manager (GameManager): The game state manager instance.
        ui_manager (UIManager): The ui_manager responsible for updating the visual grid.

    """

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
