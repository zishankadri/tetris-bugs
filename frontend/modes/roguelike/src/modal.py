from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ui_manager import UIManager

from game import game_manager
from js import document


def close_modal(id: str) -> None:
    """Close a modal dialog by its DOM element ID."""
    modal_bg = document.getElementById(id)
    if modal_bg:
        modal_bg.remove()


def continue_modal(id: str, ui_manager: UIManager) -> None:
    """Close a modal and spawn the first block."""
    close_modal(id)

    # Spawn the first block
    game_manager.spawn_next_block()
    ui_manager.render()
