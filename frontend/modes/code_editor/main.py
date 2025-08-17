from typing import Tuple  # noqa: UP035

from controls import handle_input, handle_key
from execute_code import run_python_code
from game import GameManager
from js import document, setInterval, window
from modal import continue_modal

# pyright: reportMissingImports=false
from pyodide.ffi import create_proxy
from ui_helpers import create_visual_grid, save_grid_code_to_file


def main() -> None:
    """Initialize the game."""
    game_manager = GameManager()
    create_visual_grid()  # Create display grid

    # Bind events
    input_box = document.getElementById("text-input")
    input_proxy = create_proxy(lambda evt: handle_input(evt, input_box, game_manager))
    input_box.addEventListener("keydown", input_proxy)

    # Bind save button
    run_btn = document.getElementById("runCodeButton")
    run_proxy = create_proxy(lambda *_: run_python_code())
    run_btn.addEventListener("click", run_proxy)

    # Bind save button
    save_btn = document.getElementById("save-btn")
    save_proxy = create_proxy(lambda *_: save_grid_code_to_file())
    save_btn.addEventListener("click", save_proxy)

    # Bind continue modal button
    continue_btn = document.getElementById("continue-btn")
    if continue_btn:

        def on_continue(*_args: Tuple) -> None:  # noqa: UP006
            continue_modal("modal-bg")  # hide modal

    continue_proxy = create_proxy(on_continue)
    continue_btn.addEventListener("click", continue_proxy)

    # Bind keyboard event inside the game manager
    handle_key_proxy = create_proxy(lambda evt: handle_key(evt, game_manager))
    window.addEventListener("keydown", handle_key_proxy)

    tick_proxy = create_proxy(lambda *_: game_manager.tick())
    setInterval(tick_proxy, 500)

    game_manager.render()

    # Hide loading screen once game is ready
    loading_screen = document.getElementById("loading-screen")
    if loading_screen:
        loading_screen.classList.add("hidden")


main()
