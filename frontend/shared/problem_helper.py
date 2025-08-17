import json


def check_code(code: str, id: int) -> str:  # noqa: C901
    """Check code and test case."""
    if not code:
        return "Write some code, dumbo."
    ques = get_ques(id)
    namespace = {}
    try:
        exec(code, namespace)  # noqa: S102
        try:
            func = namespace[ques["func_name"]]
            validity_list = []

            for i in ques["test_cases"]:
                if isinstance(i["input"], list) and len(i["input"]) == 2:  # noqa: PLR2004
                    if func(*tuple(i["input"])) == i["expected_output"]:
                        validity_list.append((True, i["input"]))
                    else:
                        validity_list.append((False, i["input"]))
                elif str(func(i["input"])) == str(i["expected_output"]):
                    validity_list.append((True, i["input"]))
                else:
                    validity_list.append((False, i["input"]))
            failed_case = []
            for i, test_case in validity_list:
                if not i:
                    failed_case.append((i, test_case))
            if failed_case:
                return f"Incorrect: {failed_case} {len(failed_case)} test case(s) failed"
            return "correct"  # noqa: TRY300

        except (KeyError, TypeError):
            return "incorrect function"

    except (NameError, IndentationError, SyntaxError):
        return "wrong code"


# Get questions from json file
def get_ques(id: int) -> dict:
    """Get ques from json file."""
    try:
        with open(r"problems.json") as f:  # noqa: PTH123
            return json.loads(f.read())[id - 1]
    except IndexError:
        return {}
