from game import game_manager
from js import KeyboardEvent, document


def handle_key(evt: KeyboardEvent) -> None:
    """Handle arrow keys and spacebar."""
    # Ignore input if typing in text box
    active = document.activeElement
    if active and active.id == "text-input":
        return

    if not game_manager.current_block:
        return

    moved = False
    if evt.key == "ArrowLeft":
        moved = game_manager.current_block.move(-1, 0, game_manager.grid)
    elif evt.key == "ArrowRight":
        moved = game_manager.current_block.move(1, 0, game_manager.grid)
    elif evt.key == "ArrowDown":
        moved = game_manager.current_block.move(0, 1, game_manager.grid)
    elif evt.key == " ":
        evt.preventDefault()
        game_manager.lock_current_block()
        moved = True
    if moved:
        game_manager.render()
