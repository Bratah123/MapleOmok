from pathlib import Path

import pygame

from components.base_component import BaseComponent


class OmokPiece(BaseComponent):
    def __init__(self, piece_type="SlimePiece.png"):
        super().__init__()
        self._image = pygame.image.load(Path("assets", "game", piece_type)).convert_alpha()
        self._rect = self._image.get_rect()
        # Scale the piece to 28x28 pixels to fit the board
        self._image = pygame.transform.scale(self._image, (28, 28))
        # 0-224 index of the board where 0-14 is the first column 15-29 is the second column, etc.
        self.board_position = 15

    @property
    def image(self):
        return self._image

    @property
    def rect(self):
        return self._rect

    def update(self):
        pass

    def handle_events(self, event):
        pass
