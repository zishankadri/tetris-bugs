from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from collections.abc import Iterator

    from engine.objects.block import Block
    from engine.ui_manager import BaseUIManager

from engine.game import BaseGameManager
from game_state import update_result


class GameManager(BaseGameManager):
    # class GameManager(metaclass=SingletonMeta):
    """Game logic manager."""

    def __init__(self, *args: int, **kwargs: int) -> None:
        super().__init__(*args, **kwargs)
        self.block_gen: Iterator[Block] | None = None
        self.ui_manager: BaseUIManager = None

    def spawn_next_block(self) -> None:
        """Generate and spawn the next block."""
        try:
            self.spawn_block(next(self.block_gen))
        except StopIteration:
            update_result(self.format_grid_as_text())

    def lock_current_block(self) -> None:
        """Lock current block into grid."""
        super().lock_current_block()
        self.spawn_next_block()


game_manager = GameManager(40, 20)
