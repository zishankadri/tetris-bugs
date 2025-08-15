import random
from collections.abc import Generator

from js import console

BLOCK_SIZE = 5


def split_into_blocks(s: str, block_size: int = 5) -> list[str]:
    """Split a string into blocks of given size, last block may be shorter."""
    return [s[i : i + block_size] for i in range(0, len(s), block_size)]


def block_generator(program_str: str) -> Generator[str]:
    """Yield lines of a program string from bottom to top in mostly 5-char random blocks."""
    lines = program_str.splitlines()
    for line in reversed(lines):
        blocks = split_into_blocks(line.strip())
        console.log(f"{line = }")

        while len(blocks):
            i = random.randint(0, len(blocks) - 1)  # noqa: S311
            console.log(blocks[i])
            yield blocks[i]
            blocks.pop(i)
