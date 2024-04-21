import pygame

from abc import ABC, abstractmethod
from .render_priority import RenderPriority
from pygame.sprite import Sprite


class BaseComponent(ABC, Sprite):
    def __init__(self, render_priority=RenderPriority.VERY_LOW):
        super().__init__()
        self.render_priority: RenderPriority = render_priority

    @property
    @abstractmethod
    def image(self) -> pygame.Surface | None:
        pass

    @property
    @abstractmethod
    def rect(self) -> pygame.Rect | None:
        pass

    # To be run at every frame, before drawing
    @abstractmethod
    def update(self) -> None:
        pass

    # To be run at every frame
    @abstractmethod
    def handle_events(self, event) -> None:
        pass

    def draw(self, screen) -> None:
        if self.image is not None:
            screen.blit(self.image, self.rect)
