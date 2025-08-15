from js import document
from timer import pause_timer, resume_timer


def pause() -> None:
    """Pause the game."""
    document.getElementById("pause-screen").hidden = False  # unhide
    pause_timer()


def resume() -> None:
    """Resume the game."""
    document.getElementById("pause-screen").hidden = True  # hide
    # Focus the input field
    input_box = document.getElementById("text-input")
    input_box.focus()
    resume_timer()
