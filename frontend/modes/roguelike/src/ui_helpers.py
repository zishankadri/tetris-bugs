from __future__ import annotations

from datetime import UTC, datetime

from game import game_manager
from js import URL, Blob, document, localStorage
from problem import problem_manager
from problem_helper import check_code, get_ques


def show_problem() -> None:
    """Show and update problem."""
    problem_manager.render()


def create_visual_grid() -> None:
    """Create visual grid."""
    game_div = document.getElementById("game")
    fragment = document.createDocumentFragment()
    for _y in range(game_manager.rows):
        row = []
        for _x in range(game_manager.cols):
            cell = document.createElement("div")
            cell.classList.add("cell")
            fragment.appendChild(cell)
            row.append(cell)
        game_manager.cells.append(row)
    game_div.appendChild(fragment)


def lock_visual_cells() -> None:
    """Lock the cells occupied by the current block visually."""
    cells = game_manager.current_block.get_cells()
    for cell in cells:
        cell.className = "locked-cell"

    # Focus the input field
    input_box = document.getElementById("text-input")
    input_box.focus()


def save_grid_code_to_file() -> None:
    """Open a save dialog to save the current grid code as a file."""
    saved_code = game_manager.format_grid_as_text()

    blob = Blob.new([saved_code], {"type": "text/x-python"})
    url = URL.createObjectURL(blob)

    download_link = document.createElement("a")
    download_link.href = url

    timestamp = datetime.now(UTC).strftime("%Y-%m-%d_%H-%M-%S")
    download_link.download = f"tetris_code_{timestamp}.py"
    download_link.style.display = "none"

    document.body.appendChild(download_link)
    download_link.click()
    document.body.removeChild(download_link)

    URL.revokeObjectURL(url)


def clear_grid() -> None:
    """Clear the grid by resetting all cells to None."""
    game_manager.current_block = None
    game_manager.grid = [[None for _ in range(game_manager.cols)] for _ in range(game_manager.rows)]
    game_manager._last_rendered_grid = [[None for _ in range(game_manager.cols)] for _ in range(game_manager.rows)]  # noqa: SLF001

    # Force clear all visual cells to ensure locked cells are reset
    for y in range(game_manager.rows):
        for x in range(game_manager.cols):
            cell = game_manager.cells[y][x]
            cell.className = "cell"
            cell.style.background = ""
            cell.style.color = ""
            cell.textContent = ""
    game_manager.render()
    # Clear the code output
    output = document.getElementById("code-output")
    if output:
        output.innerText = ""
    # Focus the input field
    input_box = document.getElementById("text-input")
    if input_box:
        input_box.focus()
    update_score_display()


def problem_switch() -> None:
    """Move to next problem."""
    output = document.getElementById("code-output")
    code = game_manager.format_grid_as_text()
    if check_code(code, problem_manager.problem_id) == "correct":
        problem_manager.problem_id += 1
        problem_manager.switch_problem()
        current_high_score = get_current_high_score()
        current_score = problem_manager.problems_solved
        if current_score > current_high_score:
            localStorage.setItem("tetris_high_score", str(current_score))
        update_score_display()
        clear_grid()
        output.innerText = "Correct!"
    elif check_code(code, problem_manager.problem_id) == "wrong code":
        output.innerText = "Incorrect Code, try again"

    elif check_code(code, problem_manager.problem_id) == "incorrect function":
        output.innerText = "Check your function name"

    else:
        output.innerText = check_code(code, problem_manager.problem_id)


def get_current_high_score() -> int:
    """Get the current high score from localStorage."""
    current_high_score = localStorage.getItem("tetris_high_score")
    if current_high_score is None or str(current_high_score).lower() in ["null", "jsnull", "undefined"]:
        return 0
    try:
        return int(str(current_high_score))
    except ValueError:
        return 0


def update_score_display() -> None:
    """Update both current score and high score displays above the grid."""
    # Update current score
    current_score = problem_manager.problems_solved
    current_score_elem = document.getElementById("current-score")
    if current_score_elem:
        current_score_elem.innerText = str(current_score)

    # Update high score
    current_high_score = get_current_high_score()
    high_score_elem = document.getElementById("current-high-score")
    if high_score_elem:
        high_score_elem.innerText = str(current_high_score)


def update_high_score_display() -> None:
    """Update the high score display above the grid."""
    current_high_score = get_current_high_score()
    high_score_elem = document.getElementById("current-high-score")
    if high_score_elem:
        high_score_elem.innerText = str(current_high_score)


def show_game_over() -> None:
    """Show game over screen with high score."""
    # Get current high score from localStorage
    current_high_score = get_current_high_score()
    # Check if current score is higher
    current_score = problem_manager.problems_solved
    if current_score > current_high_score:
        localStorage.setItem("tetris_high_score", str(current_score))
        current_high_score = current_score
    # Update the game over modal
    problems_solved_elem = document.getElementById("problems-solved")
    high_score_elem = document.getElementById("high-score")
    if problems_solved_elem:
        problems_solved_elem.innerText = str(current_score)
    if high_score_elem:
        high_score_elem.innerText = str(current_high_score)
    # Show the game over modal
    game_over_modal = document.getElementById("game-over-modal")
    if game_over_modal:
        game_over_modal.classList.remove("hidden")
    # Update the score display
    update_score_display()
    # Pause the game
    game_manager.paused = True


def restart_game() -> None:
    """Restart the game."""
    problem_manager.problem_id = 1
    problem_manager.problems_solved = 0
    problem_manager.problem_title = get_ques(problem_manager.problem_id)["title"]
    problem_manager.problem_desc = get_ques(problem_manager.problem_id)["description"]
    problem_manager.render()
    update_score_display()
    clear_grid()
    game_over_modal = document.getElementById("game-over-modal")
    if game_over_modal:
        game_over_modal.classList.add("hidden")
    game_manager.paused = False
    from timer import reset_timer, start_timer  # noqa: PLC0415

    reset_timer()
    start_timer()
    update_score_display()
