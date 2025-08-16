import io
import sys

from game import game_manager
from js import document


def run_python_code() -> str:
    """Run the python code in the grid."""
    code = game_manager.format_grid_as_text()
    buffer = io.StringIO()
    sys_stdout = sys.stdout  # Save the current stdout
    try:
        sys.stdout = buffer  # Redirect stdout to buffer
        exec(code)  # noqa: S102
        output = buffer.getvalue()
    except Exception as e:  # noqa: BLE001
        # We don't know what exception may arise so this is a catch all solution
        output = f"Error: {e}"
    finally:
        sys.stdout = sys_stdout  # Restore original stdout
    document.getElementById("CodeOutput").textContent = output
