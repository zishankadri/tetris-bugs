import timer
from controls import Controller
from engine.game import BaseGameManager
from js import KeyboardEvent, document, setInterval, window
from modal import continue_modal
from pyodide.ffi import create_proxy
from ui_manager import UIManager

game_manager = BaseGameManager(40, 25)


def pause() -> None:
    """Pause the game."""
    document.getElementById("pause-screen").hidden = False  # unhide
    timer.pause_timer()


def resume() -> None:
    """Resume the game."""
    document.getElementById("pause-screen").hidden = True  # hide
    # Focus the input field
    input_box = document.getElementById("text-input")
    if input_box:
        input_box.focus()
    timer.resume_timer()


def bind_dom_elements() -> None:
    """Bind the elements from the DOM to their respective functions."""
    ui_manager = UIManager(game_manager)
    game_manager.ui_manager = ui_manager  # Inject ui_manager instance (dependency injection)

    ui_manager.create_visual_grid()  # Create display grid

    controller = Controller(game_manager, ui_manager)  # Inject game_manager and ui_manager instance
    # Bind text-input
    input_box = document.getElementById("text-input")
    input_proxy = create_proxy(lambda evt: controller.handle_input(evt, input_box))
    input_box.addEventListener("keydown", input_proxy)

    # Bind save button
    save_btn = document.getElementById("save-btn")
    save_proxy = create_proxy(lambda *_: ui_manager.save_grid_code_to_file())
    save_btn.addEventListener("click", save_proxy)

    # Bind run button
    run_btn = document.getElementById("run-btn")
    run_proxy = create_proxy(lambda *_: ui_manager.problem_switch())
    run_btn.addEventListener("click", run_proxy)

    # Bind retry button
    retry_btn = document.getElementById("retry-btn")
    retry_proxy = create_proxy(lambda *_: ui_manager.clear_grid())
    retry_btn.addEventListener("click", retry_proxy)

    # Bind restart button
    restart_btn = document.getElementById("restart-btn")
    restart_proxy = create_proxy(lambda *_: ui_manager.restart_game())
    restart_btn.addEventListener("click", restart_proxy)

    # Bind pause button
    pause_btn = document.getElementById("pause-btn")
    if pause_btn:
        pause_proxy = create_proxy(lambda *_: pause())
        pause_btn.addEventListener("click", pause_proxy)

    # Bind resume button
    resume_btn = document.getElementById("resume-btn")
    if resume_btn:
        resume_proxy = create_proxy(lambda *_: resume())
        resume_btn.addEventListener("click", resume_proxy)

    # Bind continue modal button and start timer
    continue_btn = document.getElementById("continue-btn")
    continue_proxy = create_proxy(lambda _evt: continue_modal("modal-bg"))
    continue_btn.addEventListener("click", continue_proxy)

    # Bind keyboard event inside the game manager
    handle_key_proxy = create_proxy(lambda evt: controller.handle_key(evt))
    window.addEventListener("keydown", handle_key_proxy)


def main() -> None:
    """Initialize the game."""
    ui_manager = UIManager(game_manager)
    game_manager.ui_manager = ui_manager  # Inject ui_manager instance (dependency injection)

    ui_manager.create_visual_grid()  # Create display grid

    # Set timer callback for game over
    timer.on_time_up = ui_manager.show_game_over

    bind_dom_elements()

    # ✅ Global ESC key handler
    def handle_global_keys(evt: KeyboardEvent) -> None:
        if evt.key == "Escape":
            pause_screen = document.getElementById("pause-screen")
            if pause_screen.hidden:
                pause()
            else:
                resume()

    esc_proxy = create_proxy(handle_global_keys)
    window.addEventListener("keydown", esc_proxy)

    # Game tick loop
    tick_proxy = create_proxy(lambda *_: (game_manager.tick(), ui_manager.render()))
    setInterval(tick_proxy, 500)

    # Kick start
    ui_manager.render()
    ui_manager.show_problem()
    ui_manager.update_score_display()

    # Hide loading screen once game is ready
    loading_screen = document.getElementById("loading-screen")
    if loading_screen:
        loading_screen.classList.add("hidden")


main()
