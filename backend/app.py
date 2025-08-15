from flask import Flask, render_template
import os

# Define paths
template_dir = os.path.join(os.path.dirname(__file__), "../frontend")
static_dir = template_dir  # if your CSS/JS/config are in frontend/

app = Flask(
    __name__,
    template_folder=template_dir,
    static_folder=static_dir,  # serve static files from frontend/
    static_url_path=""         # serve at root so /config.json works
)

@app.route("/")
def home():
    return render_template("index.html")
