from __future__ import annotations

from js import document, localStorage, window
from problem import problem_manager
from problem_helper import check_code, get_ques
from shared.audio_utils import play_place_sound
from shared.ui_manager import BaseUIManager


class UIManager(BaseUIManager):
    """Handles rendering and UI interactions for the game."""

    def clear_grid(self, *args, **kwargs) -> None:  # noqa: ANN002, ANN003
        """Clear the grid by resetting all cells to None."""
        super().clear_grid(*args, **kwargs)

        # Clear the code output
        output = document.getElementById("code-output")
        if output:
            output.innerText = ""
        # Focus the input field
        input_box = document.getElementById("text-input")
        if input_box:
            input_box.focus()
        self.update_score_display()

    def lock_visual_cells(self, *args, **kwargs) -> None:  # noqa: ANN002, ANN003
        """Lock the cells occupied by the current block visually."""
        super().lock_visual_cells(*args, **kwargs)

        # Play place sound
        play_place_sound()

        # Focus the input field
        input_box = document.getElementById("text-input")
        input_box.focus()

    # Mode-specific methods

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
            # Play wrong answer sound
            if hasattr(window, "playWrongAnswerSound"):
                window.playWrongAnswerSound()
            output.innerText = "Incorrect Code, try again"

        elif check_code(code, problem_manager.problem_id) == "incorrect function":
            # Play wrong answer sound
            if hasattr(window, "playWrongAnswerSound"):
                window.playWrongAnswerSound()
            output.innerText = "Check your function name"

        else:
            # Play wrong answer sound for any other incorrect result
            if hasattr(window, "playWrongAnswerSound"):
                window.playWrongAnswerSound()
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
