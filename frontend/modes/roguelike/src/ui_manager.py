from __future__ import annotations

from datetime import UTC, datetime
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from game import GameManager
from js import URL, Blob, document, localStorage
from problem import problem_manager
from problem_helper import check_code, get_ques


class UIManager:
    """Handles rendering and UI interactions for the game."""

    def __init__(self, game: GameManager) -> None:
        self.game = game
        self.cells: list[list] = []
        self._last_rendered_grid: list[list[str | None]] = [[None for _ in range(game.cols)] for _ in range(game.rows)]

    def create_visual_grid(self) -> None:
        """Create the visual grid in DOM."""
        game_div = document.getElementById("game")
        fragment = document.createDocumentFragment()

        for _y in range(self.game.rows):
            row = []
            for _x in range(self.game.cols):
                cell = document.createElement("div")
                cell.classList.add("cell")
                fragment.appendChild(cell)
                row.append(cell)
            self.cells.append(row)

        game_div.appendChild(fragment)

    def render(self) -> None:
        """Update only cells that have changed to match the current game state."""
        combined_grid = [row.copy() for row in self.game.grid]

        if self.game.current_block and self.game.current_block.falling:
            for i, ch in enumerate(self.game.current_block.text):
                tx = self.game.current_block.x + i
                ty = self.game.current_block.y
                if 0 <= tx < self.game.cols and 0 <= ty < self.game.rows:
                    combined_grid[ty][tx] = ch

        for y in range(self.game.rows):
            for x in range(self.game.cols):
                cell = self.cells[y][x]
                current_char = combined_grid[y][x]
                last_char = self._last_rendered_grid[y][x]

                if current_char != last_char:
                    if current_char is None:
                        cell.className = "cell"
                        cell.style.background = ""
                        cell.style.color = ""
                        cell.textContent = ""
                    else:
                        cell.className = "block"
                        cell.textContent = current_char

                self._last_rendered_grid[y][x] = current_char

    def save_grid_code_to_file(self) -> None:
        """Prompt user to download current grid code."""
        saved_code = self.game.format_grid_as_text()

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

    # TODO: Refactor this method before abstraction
    def clear_grid(self) -> None:
        """Clear the grid by resetting all cells to None."""
        self.game.current_block = None
        self.game.grid = [[None for _ in range(self.game.cols)] for _ in range(self.game.rows)]
        self._last_rendered_grid = [[None for _ in range(self.game.cols)] for _ in range(self.game.rows)]

        # Force clear all visual cells to ensure locked cells are reset
        for y in range(self.game.rows):
            for x in range(self.game.cols):
                cell = self.cells[y][x]
                cell.className = "cell"
                cell.style.background = ""
                cell.style.color = ""
                cell.textContent = ""
        self.render()
        # Clear the code output
        output = document.getElementById("code-output")
        if output:
            output.innerText = ""
        # Focus the input field
        input_box = document.getElementById("text-input")
        if input_box:
            input_box.focus()
        self.update_score_display()

    # TODO: Refactor this method before abstraction
    def lock_visual_cells(self) -> None:
        """Lock the cells occupied by the current block visually."""
        block_cords = self.game.current_block.get_cells_coords()

        block_cells = [self.cells[cord[1]][cord[0]] for cord in block_cords]

        for cell in block_cells:
            cell.className = "locked-cell"

        # Focus the input field
        input_box = document.getElementById("text-input")
        input_box.focus()

    # Mode-specific
    # TODO: Everything above will be abstracted in the next refactor

    def show_problem(self) -> None:
        """Show and update problem."""
        problem_manager.render()

    def update_score_display(self) -> None:
        """Update both current score and high score displays above the grid."""
        # Update current score
        current_score = problem_manager.problems_solved
        current_score_elem = document.getElementById("current-score")
        if current_score_elem:
            current_score_elem.innerText = str(current_score)

        # Update high score
        current_high_score = self.get_current_high_score()
        high_score_elem = document.getElementById("current-high-score")
        if high_score_elem:
            high_score_elem.innerText = str(current_high_score)

    def update_high_score_display(self) -> None:
        """Update the high score display above the grid."""
        current_high_score = self.get_current_high_score()
        high_score_elem = document.getElementById("current-high-score")
        if high_score_elem:
            high_score_elem.innerText = str(current_high_score)

    def get_current_high_score(self) -> int:
        """Get the current high score from localStorage."""
        current_high_score = localStorage.getItem("tetris_high_score")
        if current_high_score is None or str(current_high_score).lower() in ["null", "jsnull", "undefined"]:
            return 0
        try:
            return int(str(current_high_score))
        except ValueError:
            return 0

    def problem_switch(self) -> None:
        """Move to next problem."""
        output = document.getElementById("code-output")
        code = self.game.format_grid_as_text()
        if check_code(code, problem_manager.problem_id) == "correct":
            problem_manager.problem_id += 1
            problem_manager.switch_problem()
            current_high_score = self.get_current_high_score()
            current_score = problem_manager.problems_solved
            if current_score > current_high_score:
                localStorage.setItem("tetris_high_score", str(current_score))
            self.update_score_display()
            self.clear_grid()
            output.innerText = "Correct!"
        elif check_code(code, problem_manager.problem_id) == "wrong code":
            output.innerText = "Incorrect Code, try again"

        elif check_code(code, problem_manager.problem_id) == "incorrect function":
            output.innerText = "Check your function name"

        else:
            output.innerText = check_code(code, problem_manager.problem_id)

    def show_game_over(self) -> None:
        """Show game over screen with high score."""
        # Get current high score from localStorage
        current_high_score = self.get_current_high_score()
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
        self.update_score_display()
        # Pause the game
        self.game.paused = True

    def restart_game(self) -> None:
        """Restart the game."""
        problem_manager.problem_id = 1
        problem_manager.problems_solved = 0
        problem_manager.problem_title = get_ques(problem_manager.problem_id)["title"]
        problem_manager.problem_desc = get_ques(problem_manager.problem_id)["description"]
        problem_manager.render()
        self.update_score_display()
        self.clear_grid()
        game_over_modal = document.getElementById("game-over-modal")
        if game_over_modal:
            game_over_modal.classList.add("hidden")
        self.game.paused = False
        from timer import reset_timer, start_timer  # noqa: PLC0415

        reset_timer()
        start_timer()
        self.update_score_display()
