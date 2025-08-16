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

    renderer.create_visual_grid()  # Create display grid

    # Bind events
    input_box = document.getElementById("text-input")
    input_proxy = create_proxy(lambda evt: controller.handle_input(evt, input_box))
    input_box.addEventListener("keydown", input_proxy)

    # Bind save button
    save_btn = document.getElementById("save-btn")
    save_proxy = create_proxy(lambda *_: renderer.save_grid_code_to_file())
    save_btn.addEventListener("click", save_proxy)

    # Bind run button
    run_btn = document.getElementById("run-btn")
    run_proxy = create_proxy(lambda *_: renderer.problem_switch())
    run_btn.addEventListener("click", run_proxy)

    # Bind retry button
    retry_btn = document.getElementById("retry-btn")
    retry_proxy = create_proxy(lambda *_: renderer.clear_grid())
    retry_btn.addEventListener("click", retry_proxy)

    # Bind restart button
    restart_btn = document.getElementById("restart-btn")
    restart_proxy = create_proxy(lambda *_: renderer.restart_game())
    restart_btn.addEventListener("click", restart_proxy)

    # Bind continue modal button and start timer
    continue_btn = document.getElementById("continue-btn")

    continue_proxy = create_proxy(lambda _evt: continue_modal("modal-bg"))
    continue_btn.addEventListener("click", continue_proxy)

    # Bind keyboard event inside the game manager
    handle_key_proxy = create_proxy(lambda evt: controller.handle_key(evt))
    window.addEventListener("keydown", handle_key_proxy)

    tick_proxy = create_proxy(lambda *_: (game_manager.tick(), renderer.render()))
    setInterval(tick_proxy, 500)

    renderer.render()
    renderer.show_problem()
    renderer.update_score_display()

    # Hide loading screen once game is ready
    loading_screen = document.getElementById("loading-screen")
    if loading_screen:
        loading_screen.classList.add("hidden")


main()
