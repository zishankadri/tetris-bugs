from js import document
from problem_helper import get_ques
from shared.audio_utils import win_sound
from shared.patterns import SingletonMeta


class Problem(metaclass=SingletonMeta):  # noqa: D101
    def __init__(self) -> None:
        self.problem_id = 1
        self.problems_solved = 0
        self.problem_title = get_ques(self.problem_id)["title"]
        self.problem_desc = get_ques(self.problem_id)["description"]
        self.title_elem = document.getElementById("problem-title")
        self.desc_elem = document.getElementById("problem-desc")

    def render(self) -> None:
        """Render question."""
        self.title_elem.innerText = self.problem_title
        self.desc_elem.innerText = self.problem_desc

    def switch_problem(self) -> None:
        """Switch_problem."""
        self.problems_solved += 1
        if get_ques(self.problem_id) != {}:
            self.problem_title = get_ques(self.problem_id)["title"]
            self.problem_desc = get_ques(self.problem_id)["description"]
            self.render()
        else:
            self.problem_title = "Winner!"
            self.problem_desc = "You beat the game!"
            self.render()
            win_sound()


problem_manager = Problem()
