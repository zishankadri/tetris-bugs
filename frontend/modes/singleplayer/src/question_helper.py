import random

from js import document
from shared.patterns import SingletonMeta
from shared.problem_helper import get_ques


class Question(metaclass=SingletonMeta):
    """Create a question instance so that the question can be updated after execution."""

    def __init__(self) -> None:
        self.ques_id = 0

    def send_question(self) -> dict:
        """Send question to block generator and question area in game."""
        ques = self.get_question()
        question = document.getElementById("question")
        question.textContent = ques["description"]
        return ques

    def get_question(self) -> dict:
        """Get question, while removing few questions."""
        # Here question 0 is excluded for funcitoning of the program
        # Question 6, 17, 18, 19, 20, 29 is removed due to the length of the answer
        # Question 26 is removed due to the complexity of the answer
        excluded_questions = [0, 6, 17, 18, 19, 20, 26, 29]

        while self.ques_id in excluded_questions:
            self.ques_id = random.randint(1, 29)  # noqa: S311
        return get_ques(self.ques_id)


question = Question()
