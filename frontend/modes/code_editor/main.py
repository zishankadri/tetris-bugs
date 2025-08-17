from typing import Tuple  # noqa: UP035

from controls import Controller
from execute_code import run_python_code
from js import document, setInterval, window
from modal import continue_modal

# pyright: reportMissingImports=false
from pyodide.ffi import create_proxy
from shared.game import BaseGameManager
from ui_manager import UIManager

game_manager = BaseGameManager(40, 20)


def main() -> None:
    """Initialize the game."""
    ui_manager = UIManager(game_manager)
    game_manager.ui_manager = ui_manager  # Inject ui_manager instance (dependency injection)
    controller = Controller(game_manager, ui_manager)  # Inject game_manager and ui_manager instance

    ui_manager.create_visual_grid()  # Create display grid

    # Bind events
    input_box = document.getElementById("text-input")
    input_proxy = create_proxy(lambda evt: controller.handle_input(evt, input_box))
    input_box.addEventListener("keydown", input_proxy)

    # Bind save button
    run_btn = document.getElementById("runCodeButton")
    run_proxy = create_proxy(lambda *_: run_python_code(game_manager))
    run_btn.addEventListener("click", run_proxy)

    # Bind save button
    save_btn = document.getElementById("save-btn")
    save_btn2 = document.getElementById("save-btn2")
    save_proxy = create_proxy(lambda *_: ui_manager.save_grid_code_to_file())
    save_btn.addEventListener("click", save_proxy)
    save_btn2.addEventListener("click", save_proxy)

    # Bind new-file button
    new_file = document.getElementById("new-file")
    new_file_proxy = create_proxy(lambda *_: ui_manager.clear_grid())
    new_file.addEventListener("click", new_file_proxy)

    # Bind continue modal button
    continue_btn = document.getElementById("continue-btn")
    if continue_btn:

        def on_continue(*_args: Tuple) -> None:  # noqa: UP006
            continue_modal("modal-bg")  # hide modal

    continue_proxy = create_proxy(on_continue)
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

    return ui_manager


main()
