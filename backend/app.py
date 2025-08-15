# Define paths
from pathlib import Path

from flask import Flask, render_template

template_dir = Path(__file__).resolve().parent.parent / "frontend"
static_dir = template_dir  # if your CSS/JS/config are in frontend/

app = Flask(
    __name__,
    template_folder=template_dir,
    static_folder=static_dir,  # serve static files from frontend/
    static_url_path="",  # serve at root so /config.json works
)


@app.route("/")
def home() -> None:
    """Render the main page."""
    # Render the index.html file from the frontend directory
    return render_template("index.html")
