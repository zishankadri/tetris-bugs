import random
from collections.abc import Generator

from game import game_manager
from js import console, document
from shared.problem_helper import get_ques


def split_into_blocks(s: str, block_size: int = 5) -> list[str]:
    """Split a string into blocks of given size, last block may be shorter."""
    return [s[i : i + block_size] for i in range(0, len(s), block_size)]


def block_generator(renderer: str) -> Generator[str]:
    """Yield blocks of a program string from bottom to top for gameplay.

    Each line of the program is split into mostly 5-character blocks,
    and blocks are yielded in random order. After yielding a line's
    blocks, the generator checks the corresponding player's line:
    if it matches, the row is cleared from both the game state and renderer.

    Args:
        renderer (str): The GridRenderer instance used to update the visual grid.

    Yields:
        str: Individual blocks of code from the program string, in random order.

    """

    def first_empty_row_from_bottom() -> int:
        """Return the 1-based index of the first completely empty row from the bottom."""
        n = len(game_manager.grid)
        for i in range(n - 1, -1, -1):
            if all(not cell for cell in game_manager.grid[i]):
                # Distance from bottom
                return n - i
        return 1  # fallback if no empty row

    question_id = random.randint(1, 28)  # noqa: S311
    question_details = get_ques(question_id)
    send_question(question_details)
    lines = question_details["solution_code"].splitlines()
    bottom_pointer = 1
    for line in reversed(lines):
        blocks = split_into_blocks(line.strip())

        while len(blocks):
            rand_j = random.randint(0, len(blocks) - 1)  # noqa: S311
            yield blocks[rand_j]
            console.log(len(blocks[rand_j]))
            blocks.pop(rand_j)

        player_line = game_manager.format_grid_line_as_text(-(bottom_pointer))

        if player_line.strip() == line.strip():
            # Clear the row if correctly answered
            game_manager.clear_row(-(bottom_pointer))
            renderer.clear_row(-(bottom_pointer))
        else:
            # Incorrect answer
            # Increment the pointer, as the current row will stay stuck
            bottom_pointer = first_empty_row_from_bottom()


def send_question(ques: dict) -> None:
    """Send question to the question place in the game."""
    question = document.getElementById("question")
    question.textContent = ques["description"]
