from js import document
from problem_helper import check_code, question


def check_win(code: str) -> bool:  # noqa: RET503
    """Check Whether the player has won or lost."""
    result = check_code(code, question.ques_id)
    if result in {"wrong code", "incorrect function"}:
        return False
    if result == "correct":
        return True


def update_result(code: str) -> None:
    """Update the UI after checking of the game status."""
    winning_status = check_win(code)
    game_state = document.getElementById("game-state")
    game_end_box = document.getElementById("game-end")
    game_end_box.classList.remove("hidden")
    if winning_status:
        game_state.textContent = "Wow you got the code right"
    else:
        game_state.textContent = "No.. That is not right"
