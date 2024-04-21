from pathlib import Path
from components.base_component import BaseComponent

import pygame as pg
import pygame


class BaseText(BaseComponent):
    def __init__(self, x_pos, y_pos, message, font_name, font_size, anti_alias, color, render_priority):
        super().__init__(render_priority)
        self.font = pg.font.Font(Path("assets", "fonts", font_name), font_size)
        self.color = color
        self.anti_alias = anti_alias
        self.message = message

        # create text object, and set its center to the designated coordinates
        self.text = self.font.render(self.message, self.anti_alias, self.color)
        self.location = self.text.get_rect()
        self.location.centerx = x_pos
        self.location.centery = y_pos

    @property
    def image(self) -> pygame.Surface:
        return self.text

    @property
    def rect(self) -> pygame.Rect:
        return self.location

    def update(self) -> None:
        pass

    def handle_events(self, event) -> None:
        pass

    def update_color(self, color):
        self.color = color
        self.text = self.font.render(self.message, self.anti_alias, self.color)


class MultilineBaseText:
    def __init__(self, game, x_pos, y_pos, message, font_name, font_size,
                 anti_alias, color, line_space):
        if message is None:
            print("[WARN] Empty text box created!")
            message = [""]
        self.game = game
        font = pg.font.Font(Path("assets", "fonts", font_name), font_size)

        # create a text object for every line in the given message
        # and set the center of the first line to the designated coordinates
        # and vary the y-coordinate of subsequent lines using the specified
        # line spacing
        lines = [font.render(line, anti_alias, color) for line in message]
        locations = [line.get_rect() for line in lines]
        for index, location in enumerate(locations):
            location.centerx = x_pos
            location.centery = y_pos + index * line_space

        self.line_pairs = zip(lines, locations)
        self.draw()

    def draw(self):
        for line, location in self.line_pairs:
            self.game.screen.blit(line, location)