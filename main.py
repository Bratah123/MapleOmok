import pygame
from scenes import *
from components.base_scene import BaseScene

FPS_CAP = 60


class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((1000, 700))
        self.icon = pygame.image.load("./assets/game/SlimePiece.png")
        pygame.display.set_caption("MapleStory Omok")
        self.running = True

        self.active_scene = ""
        self.scenes = {
            scene.__name__: scene(self) for scene in BaseScene.__subclasses__()
        }
        self.switch_scenes("MainMenu")

    def run(self):
        pygame.display.set_icon(self.icon)

        clock = pygame.time.Clock()
        while self.running:
            clock.tick(FPS_CAP)
            self.screen.fill((0, 0, 0))

            self.scenes[self.active_scene].render_and_update()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

                self.scenes[self.active_scene].handle_events(event)

            pygame.display.update()

        pygame.quit()

    def switch_scenes(self, scene_name, **kwargs):
        if self.scenes.get(self.active_scene) is not None:
            self.scenes[self.active_scene].is_active_scene = False

        self.active_scene = scene_name
        new_scene = self.scenes[self.active_scene]
        new_scene.is_active_scene = True
        new_scene.on_switch_to_active_scene(kwargs)


def main():
    game = Game()
    game.run()


if __name__ == "__main__":
    main()
