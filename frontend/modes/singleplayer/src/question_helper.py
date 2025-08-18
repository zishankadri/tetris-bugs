import random

from js import document
from shared.problem_helper import get_ques


def send_question() -> dict:
    """Send question to block generator and question area in game."""
    ques = get_question()
    question = document.getElementById("question")
    question.textContent = ques["description"]
    return ques


def get_question() -> dict:
    """Get question, while removing few questions."""
    # Here question 0 is excluded for funcitoning of the program
    # Question 6, 17, 18, 19, 20, 29 is removed due to the length of the answer
    # Question 26 is removed due to the complexity of the answer
    excluded_questions = [0, 6, 17, 18, 19, 20, 26, 29]
    ques_id = 0
    while ques_id in excluded_questions:
        ques_id = random.randint(1, 29)  # noqa: S311
    return get_ques(ques_id)
