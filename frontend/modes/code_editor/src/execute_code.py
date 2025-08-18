from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from engine.game import BaseGameManager

import io
import sys

from js import document


def run_python_code(game_manager: BaseGameManager) -> str:
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
