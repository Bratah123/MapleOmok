from abc import ABC
from pathlib import Path

import pygame

from components.base_component import BaseComponent


class StaticImage(BaseComponent, ABC):
    def __init__(self, image_path, x_pos=0, y_pos=0):
        super().__init__()
        self.image_path = image_path
        self._image = pygame.image.load(image_path)

        self._rect = self._image.get_rect()
        self._rect.x = x_pos
        self._rect.y = y_pos

    @property
    def image(self) -> pygame.Surface | None:
        return self._image

    @property
    def rect(self) -> pygame.Rect | None:
        return self._rect

    def update(self) -> None:
        pass

    def handle_events(self, event) -> None:
        pass

    def set_position(self, x, y):
        self.rect.x = x
        self.rect.y = y
