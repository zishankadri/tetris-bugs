from block import Block
from constants import MAX_BLOCK_LENGTH
from game import game_manager
from js import HTMLInputElement, KeyboardEvent, document


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
        game_manager.current_block.lock(game_manager.grid)
        game_manager.current_block = None
        moved = True
    if moved:
        game_manager.render()


def handle_input(evt: KeyboardEvent, input_box: HTMLInputElement) -> None:
    """Spawn a new block when Enter is pressed."""
    # Only allow new block if none is falling
    if game_manager.current_block and game_manager.current_block.falling:
        return

    if evt.key == "Enter":
        text = input_box.value.strip()
        if 1 <= len(text) <= MAX_BLOCK_LENGTH:
            new_block = Block(text, game_manager.cols, game_manager.rows)
            game_manager.current_block = new_block
            input_box.value = ""
            input_box.blur()
            game_manager.render()
