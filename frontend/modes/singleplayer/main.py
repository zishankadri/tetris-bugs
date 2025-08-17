from block_generator import block_generator
from game import game_manager
from js import document, setInterval, window
from modal import continue_modal
from pyodide.ffi import create_proxy
from shared.controls import BaseController
from shared.ui_manager import BaseUIManager


def main() -> None:
    """Initialize the game."""
    ui_manager = BaseUIManager(game_manager)
    game_manager.ui_manager = ui_manager
    controller = BaseController(game_manager, ui_manager)
    game_manager.block_gen = block_generator(ui_manager)

    ui_manager.create_visual_grid()

    # Bind continue modal button and start timer
    continue_btn = document.getElementById("continue-btn")
    continue_proxy = create_proxy(lambda _evt: continue_modal("modal-bg", ui_manager))
    continue_btn.addEventListener("click", continue_proxy)

    # Bind keyboard event inside the game manager
    handle_key_proxy = create_proxy(lambda evt: controller.handle_key(evt))
    window.addEventListener("keydown", handle_key_proxy)

    tick_proxy = create_proxy(lambda *_: (game_manager.tick(), ui_manager.render()))
    setInterval(tick_proxy, 500)

    ui_manager.render()

    # Hide loading screen once game is ready
    loading_screen = document.getElementById("loading-screen")
    if loading_screen:
        loading_screen.classList.add("hidden")


main()
