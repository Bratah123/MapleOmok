from components.base_scene import BaseScene
from game.omok_board import OmokBoard
from interactables.button import TextButton

WINDOW_WIDTH = 1000
WINDOW_HEIGHT = 700


class GameScene(BaseScene):
    def __init__(self, game):
        super().__init__(game)

        self.omok_board = OmokBoard(game.screen)
        go_home_button = TextButton(850, 300, "Go Home", on_click=self.on_click_go_home, font_size=24)
        restart_button = TextButton(850, 350, "Restart", on_click=self.on_click_restart, font_size=24)

        self._components = [
            self.omok_board,
            go_home_button,
            restart_button,
        ]

    @property
    def components(self):
        return self._components

    # Event Handler that fires off when this scene is switched to the active scene
    def on_switch_to_active_scene(self, kwargs):
        pass

    def on_click_go_home(self):
        # Switch to the main menu scene
        self.omok_board.reset_board()
        self.game.switch_scenes("MainMenu")

    def on_click_restart(self):
        # Restart the game
        self.omok_board.reset_board()
