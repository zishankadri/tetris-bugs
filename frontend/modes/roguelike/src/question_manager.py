import random
from typing import ClassVar

from js import document
from shared.patterns import SingletonMeta
from shared.problem_helper import get_ques


class QuestionManager(metaclass=SingletonMeta):
    """Manages question selection and updates the displayed question."""

    TOTAL_QUESTIONS: ClassVar[int] = 29
    # Questions excluded because they cause issues in this game mode
    DEFAULT_EXCLUDED: ClassVar[set[int]] = {0, 6, 17, 18, 19, 20, 26, 29}

    def __init__(self) -> None:
        self.ques_id: int | None = None
        # Keep track of excluded questions and avoid duplicates
        self.excluded_questions = set(self.DEFAULT_EXCLUDED)

    def get_question(self) -> dict:
        """Select a new question while avoiding excluded questions."""
        remaining_questions = set(range(1, self.TOTAL_QUESTIONS + 1)) - self.excluded_questions

        if not remaining_questions:
            # TODO: Add end game logic
            pass

        self.ques_id = random.choice(list(remaining_questions))  # noqa: S311
        self.excluded_questions.add(self.ques_id)

        ques = get_ques(self.ques_id)
        document.getElementById("question").textContent = ques["description"]
        return ques


question_manager = QuestionManager()
