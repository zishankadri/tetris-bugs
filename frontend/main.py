from controls import handle_input, handle_key
from game import GameManager
from js import document, setInterval, window

# pyright: reportMissingImports=false
from pyodide.ffi import create_proxy


def main() -> None:
    """Initialize the game."""
    game_manager = GameManager()

    # Bind events
    input_box = document.getElementById("text-input")
    input_proxy = create_proxy(lambda evt: handle_input(evt, input_box))
    input_box.addEventListener("keydown", input_proxy)

    handle_key_proxy = create_proxy(handle_key)
    window.addEventListener("keydown", handle_key_proxy)

    tick_proxy = create_proxy(lambda *_: game_manager.tick())
    setInterval(tick_proxy, 500)

    game_manager.render()


main()
