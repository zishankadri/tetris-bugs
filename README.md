# Tetris Bugs

A fun browser-based **Tetris with a twist**, making the game unpredictable and exciting!  
Built with a **Flask backend** and **PyScript + TailwindCSS frontend**.

---

## 🚀 Features

- **Flask backend** (`backend/`) – serves game assets and API routes.
- **PyScript frontend** (`frontend/`) – game logic written in Python, runs in the browser.
- **TailwindCSS** – modern CSS framework for styling.
- **Poetry** – for Python dependency management.
- **Ruff** – for linting and formatting.
- Single `poetry run start` command to run backend and frontend together.

---

## 📦 Requirements

- Python 3.13+
- [Poetry](https://python-poetry.org/)
- Node.js & npm

---

## ⚙️ Installation

```bash
# Clone the repository
git clone https://github.com/your-username/tetris-bugs.git
cd tetris-bugs

# Install Python dependencies
poetry install

# Install frontend dependencies
cd frontend
npm install
cd ..
```

---

## ▶️ Development

Start both backend and frontend in one command:

```bash
poetry run start
```

Backend runs at:  
```
http://127.0.0.1:5000
```

Frontend assets are served from `frontend/dist`.

---

## 📁 Project Structure

```
tetris-bugs/
│   README.md
│   pyproject.toml
│   poetry.lock
│
├── backend/        # Flask backend
│   ├── app.py
│   └── ...
│
└── frontend/       # PyScript + Tailwind frontend
    ├── src/        # Python game code
    ├── styles/     # TailwindCSS input
    ├── dist/       # Compiled output
    └── index.html
```

---

## 🛠 Linting & Formatting

```bash
# Run Ruff to check code style
poetry run ruff check .

# Run Ruff and automatically fix issues
poetry run ruff check . --fix

# Run pre-commit hooks on all files
poetry run pre-commit run --all-files
```

---
