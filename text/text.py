from text.base_text import BaseText, MultilineBaseText
from components.render_priority import RenderPriority


class NormalText(BaseText):
    def __init__(self, x_pos=0, y_pos=0, message="LOREM IPSUM",
                 font_size=24, anti_alias=True, color=(255, 255, 255), render_priority=RenderPriority.VERY_LOW):
        super().__init__(x_pos=x_pos, y_pos=y_pos, message=message, font_size=font_size,
                         font_name="daydream.ttf", anti_alias=anti_alias,
                         color=color, render_priority=render_priority)


class MultilineNormalText(MultilineBaseText):
    def __init__(self, game, x_pos=0, y_pos=0, message=None,
                 font_size=24, anti_alias=True, color=(255, 255, 255),
                 line_space=40):
        if message is None:
            message = ["LOREM", "IPSUM"]
        super().__init__(game, x_pos, y_pos, message, font_name="daydream.ttf",
                         font_size=font_size, anti_alias=anti_alias,
                         color=color, line_space=line_space)