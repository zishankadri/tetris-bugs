from controls import handle_key
from game import game_manager
from js import document, setInterval, window
from modal import close_modal

# pyright: reportMissingImports=false
from pyodide.ffi import create_proxy
from ui_helpers import create_visual_grid


def main() -> None:
    """Initialize the game."""
    create_visual_grid()  # Create display grid

    # Bind continue modal button and start timer
    continue_btn = document.getElementById("continue-btn")

    continue_proxy = create_proxy(lambda _evt: close_modal("modal-bg"))
    continue_btn.addEventListener("click", continue_proxy)

    # Bind keyboard event inside the game manager
    handle_key_proxy = create_proxy(lambda evt: handle_key(evt))
    window.addEventListener("keydown", handle_key_proxy)

    tick_proxy = create_proxy(lambda *_: game_manager.tick())
    setInterval(tick_proxy, 500)

    game_manager.spawn_next_block()

    game_manager.render()

    # Hide loading screen once game is ready
    loading_screen = document.getElementById("loading-screen")
    if loading_screen:
        loading_screen.classList.add("hidden")


main()
