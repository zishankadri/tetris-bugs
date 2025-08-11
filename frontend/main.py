from random import randint

from js import HTMLInputElement, KeyboardEvent, document, setInterval, window

# pyright: reportMissingImports=false
from pyodide.ffi import create_proxy

MAX_BLOCK_LENGTH = 4


class SingletonMeta(type):  # noqa: D101
    _instance = None  # type: object | None

    def __call__(cls: type["SingletonMeta"], *args: object, **kwargs: object) -> object:
        """Return the singleton instance, creating it if necessary."""
        if cls._instance is None:
            cls._instance = super().__call__(*args, **kwargs)
        return cls._instance


class Block:
    """Represents a horizontal text block moving on a grid."""

    def __init__(self, text: str, grid_cols: int, grid_rows: int) -> None:
        self.max_start_y = 2
        self.text = text[: min(MAX_BLOCK_LENGTH, grid_cols)]
        self.cols = grid_cols
        self.rows = grid_rows
        # Spawns block randomly
        self.x = randint(0, self.cols - len(self.text))  # noqa: S311
        self.y = randint(0, self.max_start_y)  # noqa: S311
        self.falling = True

    def can_move(self, dx: int, dy: int, grid: list[list[str | None]]) -> bool:
        """Check if move is valid."""
        new_x = self.x + dx
        new_y = self.y + dy
        for i in range(len(self.text)):
            tx, ty = new_x + i, new_y
            if tx < 0 or tx >= self.cols or ty >= self.rows:
                return False
            if ty >= 0 and grid[ty][tx] is not None:
                return False
        return True

    def move(self, dx: int, dy: int, grid: list[list[str | None]]) -> bool:
        """Try moving the block, return True if moved."""
        if self.can_move(dx, dy, grid):
            # Update position if move is valid
            self.x += dx
            self.y += dy
            return True
        return False

    def lock(self, grid: list[list[str | None]]) -> None:
        """Place the block into the grid and stop it from falling."""
        for i, ch in enumerate(self.text):
            tx = self.x + i
            ty = self.y
            if 0 <= tx < self.cols and 0 <= ty < self.rows:
                grid[ty][tx] = ch
        self.falling = False


class GameManager(metaclass=SingletonMeta):  # noqa: D101
    def __init__(self) -> None:
        # Grid size
        self.cols, self.rows = 40, 20
        self.grid = [[None for _ in range(self.cols)] for _ in range(self.rows)]
        self.current_block: Block | None = None

        # Create visual grid
        game_div = document.getElementById("game")
        self.cells = []
        fragment = document.createDocumentFragment()
        for _y in range(self.rows):
            row = []
            for _x in range(self.cols):
                cell = document.createElement("div")
                cell.classList.add("cell")
                fragment.appendChild(cell)
                row.append(cell)
            self.cells.append(row)
        game_div.appendChild(fragment)

        # Keep track of last rendered state to minimize DOM updates
        self._last_rendered_grid = [[None for _ in range(self.cols)] for _ in range(self.rows)]

    def render(self) -> None:
        """Render grid and current block efficiently by updating only changed cells."""
        # Copy current grid state including current_block overlay
        combined_grid = [row.copy() for row in self.grid]

        if self.current_block and self.current_block.falling:
            for i, ch in enumerate(self.current_block.text):
                tx = self.current_block.x + i
                ty = self.current_block.y
                if 0 <= tx < self.cols and 0 <= ty < self.rows:
                    combined_grid[ty][tx] = ch

        # Update only changed cells
        for y in range(self.rows):
            for x in range(self.cols):
                cell = self.cells[y][x]
                current_char = combined_grid[y][x]
                last_char = self._last_rendered_grid[y][x]

                if current_char != last_char:
                    if current_char is None:
                        cell.classList.remove("block", "locked")
                        cell.style.background = ""
                        cell.style.color = ""
                        cell.textContent = ""
                    else:
                        cell.classList.add("block")
                        cell.textContent = current_char
                        cell.style.background = "lime"
                        cell.style.color = "black"

                self._last_rendered_grid[y][x] = current_char

    def tick(self) -> None:
        """Advance game state by one step."""
        if not self.current_block or not self.current_block.falling:
            return

        # Try to move block down
        if not self.current_block.move(0, 1, self.grid):
            # If can't move down, lock block and clear current_block
            self.current_block.lock(self.grid)
            self.current_block = None

        self.render()

    def format_grid_as_text(self) -> str:
        """Format the grid as a text representation."""
        return "\n".join("".join(cell if cell is not None else "." for cell in row) for row in self.grid)


def handle_key(evt: KeyboardEvent) -> None:
    """Handle arrow keys and spacebar."""
    game_manager = GameManager()

    # Ignore input if typing in text box
    active = document.activeElement
    if active and active.id == "text-input":
        return

    if not game_manager.current_block:
        return

    moved = False
    if evt.key == "ArrowLeft":
        moved = game_manager.current_block.move(-1, 0, game_manager.grid)
    elif evt.key == "ArrowRight":
        moved = game_manager.current_block.move(1, 0, game_manager.grid)
    elif evt.key == " ":
        game_manager.current_block.lock(game_manager.grid)
        game_manager.current_block = None
        moved = True

    if moved:
        game_manager.render()


def handle_input(evt: KeyboardEvent, input_box: HTMLInputElement) -> None:
    """Spawn a new block when Enter is pressed."""
    game_manager = GameManager()

    # Only allow new block if none is falling
    if game_manager.current_block and game_manager.current_block.falling:
        return

    if evt.key == "Enter":
        text = input_box.value.strip()
        if 1 <= len(text) <= MAX_BLOCK_LENGTH:
            new_block = Block(text, game_manager.cols, game_manager.rows)
            game_manager.current_block = new_block
            input_box.value = ""
            input_box.blur()
            game_manager.render()


def main() -> None:
    """Initialize the game."""
    game_manager = GameManager()

    # Bind events
    input_box = document.getElementById("text-input")
    input_proxy = create_proxy(lambda evt: handle_input(evt, input_box))
    input_box.addEventListener("keydown", input_proxy)

    handle_key_proxy = create_proxy(handle_key)
    window.addEventListener("keydown", handle_key_proxy)

    tick_proxy = create_proxy(lambda *_: game_manager.tick())
    setInterval(tick_proxy, 500)

    game_manager.render()


main()
