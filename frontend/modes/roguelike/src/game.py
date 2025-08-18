from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from collections.abc import Iterator

    from shared.objects.block import Block
    from shared.ui_manager import BaseUIManager

from shared.game import BaseGameManager


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
            self.update_result(self.format_grid_as_text())

    def lock_current_block(self) -> None:
        """Lock current block into grid."""
        super().lock_current_block()
        self.spawn_next_block()

    def update_result(self) -> None:
        """Update result."""


game_manager = GameManager(40, 20)
