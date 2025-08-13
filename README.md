This project uses **PyScript** to run Python in the browser, with **Tailwind CSS** for styling.
## Requirements

- Python 3
- Node.js & npm (for building Tailwind CSS)

## Setup

1. Go to the frontend folder
```
cd frontend
```

2. Install Tailwind dependencies:

```
npm install
```

3. Build Tailwind CSS:

```
npm run build
```

4. Start development server (Python):
```
python -m http.server
```

Then open `http://localhost:8000` in your browser.

Optional (for contributors only):

```
npm run dev
```

This updates your CSS automatically while you work.

## Notes

- Tailwind CSS is used for styling only.
- PyScript runs Python directly in the browser.
