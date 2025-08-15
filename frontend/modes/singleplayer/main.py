from block_generator import block_generator
from controls import Controller
from game import game_manager
from js import document, setInterval, window
from modal import continue_modal
from pyodide.ffi import create_proxy
from ui_renderer import GridRenderer


def main() -> None:
    """Initialize the game."""
    renderer = GridRenderer(game_manager)
    game_manager.renderer = renderer  # Inject renderer instance (dependency injection)
    controller = Controller(game_manager, renderer)  # Inject game_manager and renderer instance
    game_manager.block_gen = block_generator(renderer)

    renderer.create_visual_grid()  # Create display grid

    # Bind continue modal button and start timer
    continue_btn = document.getElementById("continue-btn")

    continue_proxy = create_proxy(lambda _evt: continue_modal("modal-bg", renderer))
    continue_btn.addEventListener("click", continue_proxy)

    # Bind keyboard event inside the game manager
    handle_key_proxy = create_proxy(lambda evt: controller.handle_key(evt))
    window.addEventListener("keydown", handle_key_proxy)

    tick_proxy = create_proxy(lambda *_: (game_manager.tick(), renderer.render()))
    setInterval(tick_proxy, 500)

    renderer.render()

    # Hide loading screen once game is ready
    loading_screen = document.getElementById("loading-screen")
    if loading_screen:
        loading_screen.classList.add("hidden")


main()
