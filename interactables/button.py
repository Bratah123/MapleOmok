import pygame
from text.text import NormalText


class TextButton(NormalText):
    def __init__(self, x, y, text, on_click=lambda: None, font_size=24):
        super().__init__(x_pos=x, y_pos=y, message=text, font_size=font_size)
        self._click_callback = on_click

    def handle_events(self, event) -> None:
        # Check if the mouse is hovering over the button
        if self.rect.collidepoint(pygame.mouse.get_pos()):
            # Change the color of the text
            self.text = self.font.render(self.message, self.anti_alias, (80, 80, 80))
        else:
            self.text = self.font.render(self.message, self.anti_alias, self.color)

        # Check if the mouse is clicking on the button
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                if self.rect.collidepoint(pygame.mouse.get_pos()):
                    self.on_click()

    def on_click(self):
        self._click_callback()
