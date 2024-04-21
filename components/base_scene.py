from abc import ABC, abstractmethod
from typing import List
from .base_component import BaseComponent


class BaseScene(ABC):
    def __init__(self, game):
        self.game = game
        self.is_active_scene = False

    @property
    @abstractmethod
    def components(self) -> List[BaseComponent]:
        pass

    # Called every frame
    def render_and_update(self):
        for component in self.components:
            component.update()
            component.draw(self.game.screen)

    # Called every frame
    def handle_events(self, event):
        for component in self.components:
            component.handle_events(event)

    def clear_components(self):
        self.components.clear()

    def add_component(self, component: BaseComponent):
        self.components.append(component)
        self.components.sort(key=lambda x: x.render_priority.value)

    @abstractmethod
    def on_switch_to_active_scene(self, kwargs):
        pass
