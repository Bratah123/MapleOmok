from pathlib import Path

from components.base_scene import BaseScene
from components.static_image import StaticImage
from interactables.button import TextButton
from text.text import NormalText

WINDOW_WIDTH = 1000
WINDOW_HEIGHT = 700


class MainMenu(BaseScene):
    def __init__(self, game):
        super().__init__(game)
        title = NormalText(
            WINDOW_WIDTH // 2,
            80,
            "MapleStory Omok",
            font_size=48,
        )
        credits_text = NormalText(WINDOW_WIDTH // 2, 650, "Created by: Brandon Nguyen", font_size=16)
        play_button = TextButton(WINDOW_WIDTH // 2, 550, "Play", on_click=self.on_click_play, font_size=32)

        slime = StaticImage(Path("assets", "game", "SlimePiece.png"), x_pos=210, y_pos=250)
        mushroom = StaticImage(Path("assets", "game", "MushroomPiece.png"), x_pos=360, y_pos=250)
        pink_bear = StaticImage(Path("assets", "game", "PinkBearPiece.png"), x_pos=510, y_pos=250)
        panda = StaticImage(Path("assets", "game", "PandaBearPiece.png"), x_pos=660, y_pos=250)

        self._components = [
            title,
            play_button,
            credits_text,
            slime,
            mushroom,
            pink_bear,
            panda,
        ]

    @property
    def components(self):
        return self._components

    # Event Handler that fires off when this scene is switched to the active scene
    def on_switch_to_active_scene(self, kwargs):
        pass

    def on_click_play(self):
        print("Play button clicked!")

    def on_click_high_score(self):
        print("High Score button clicked!")
