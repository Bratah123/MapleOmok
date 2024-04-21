from components.base_scene import BaseScene
from game.omok_board import OmokBoard
from interactables.button import TextButton

WINDOW_WIDTH = 1000
WINDOW_HEIGHT = 700


class GameScene(BaseScene):
    def __init__(self, game):
        super().__init__(game)

        omok_board = OmokBoard()
        go_home_button = TextButton(850, WINDOW_HEIGHT // 2, "Go Home", on_click=self.on_click_go_home, font_size=24)

        self._components = [
            omok_board,
            go_home_button,
        ]

    @property
    def components(self):
        return self._components

    # Event Handler that fires off when this scene is switched to the active scene
    def on_switch_to_active_scene(self, kwargs):
        pass

    def on_click_go_home(self):
        # Switch to the main menu scene
        self.game.switch_scenes("MainMenu")

        # TODO: Clean up the Omok Game
