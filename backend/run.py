import shutil
import subprocess
import sys
from pathlib import Path

from flask.cli import main as flask_main

DEFAULT_ARG_COUNT = 2  # Avoid magic number


def main() -> None:
    """Run the Flask application and start the frontend development server."""
    frontend_dir = Path(__file__).parent.parent / "frontend"

    # Locate npm safely
    npm_path = shutil.which("npm")
    if npm_path is None:
        print("npm not found in PATH.")
        sys.exit(1)

    # Start npm dev server
    try:
        subprocess.Popen(  # noqa: S603
            [npm_path, "run", "dev"],
            cwd=frontend_dir,
        )
        print("Frontend dev server started.")
    except OSError as err:
        print(f"Failed to start frontend: {err}")

    sys.argv.insert(1, "--app=backend.app")

    if len(sys.argv) == DEFAULT_ARG_COUNT:
        sys.argv.append("run")

    flask_main()


if __name__ == "__main__":
    main()
