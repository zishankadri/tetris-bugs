from flask import Flask, render_template

# Create a Flask app instance
app = Flask(__name__)

# Define a route for the homepage
@app.route('/')  # noqa: Q000
def home() -> str:
    """Execute the base function."""
    return render_template("index.html")

# Start the server on localhost:8000
if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=8000)  # noqa: S104, S201
