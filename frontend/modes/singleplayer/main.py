from typing import Tuple  # noqa: UP035

from block_generator import block_generator
from controls import handle_key
from game import game_manager
from js import console, document, setInterval, window
from modal import close_modal

# pyright: reportMissingImports=false
from pyodide.ffi import create_proxy
from timer import start_timer
from ui_helpers import create_visual_grid


def main() -> None:
    """Initialize the game."""
    create_visual_grid()  # Create display grid

    # Bind continue modal button and start timer
    continue_btn = document.getElementById("continue-btn")

    def on_continue(*_args: Tuple) -> None:  # noqa: UP006
        close_modal("modal-bg")  # hide modal
        start_timer()  # start the timer

    continue_proxy = create_proxy(on_continue)
    continue_btn.addEventListener("click", continue_proxy)

    # Bind keyboard event inside the game manager
    handle_key_proxy = create_proxy(lambda evt: handle_key(evt))
    window.addEventListener("keydown", handle_key_proxy)

    demo_program = """from collections.abc import Generator
    x = 10
    y = 20
    print(x + y)"""

    tick_proxy = create_proxy(lambda *_: game_manager.tick())
    setInterval(tick_proxy, 500)

    block = block_generator(demo_program)
    console.log("next: ", block)
    game_manager.spawn_block(next(block))

    game_manager.render()

    # Hide loading screen once game is ready
    loading_screen = document.getElementById("loading-screen")
    if loading_screen:
        loading_screen.classList.add("hidden")


main()
