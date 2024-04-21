import pygame

from components.base_component import BaseComponent
from components.render_priority import RenderPriority


class OmokBoard(BaseComponent):
    def __init__(self):
        super().__init__(RenderPriority.VERY_LOW)
        self._pieces = []
        self._rect = pygame.Rect(0, 0, 0, 0)
        self._board_size = 15  # Default Gomoku board size is 15x15
        self._board_x = 255
        self._board_y = 110

    @property
    def image(self) -> pygame.Surface | None:
        return None

    @property
    def rect(self) -> pygame.Rect | None:
        return self._rect

    def draw(self, screen: pygame.Surface) -> None:
        # Draw the 15x15 board with each tile being a square
        for i in range(self._board_size):
            for j in range(self._board_size):
                # Draw the board on the current board location
                pygame.draw.rect(screen, (255, 255, 255),
                                 ((i * 30) + self._board_x, (j * 30) + self._board_y, 30, 30),
                                 1)

        # Draw the pieces on the board
        for piece in self._pieces:
            pygame.draw.circle(screen, piece.color, piece.position, 10)

    def update(self) -> None:
        pass

    def handle_events(self, event) -> None:
        pass
