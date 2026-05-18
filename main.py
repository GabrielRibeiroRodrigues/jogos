import sys
import pygame
from classes.Dashboard import Dashboard
from classes.Level import Level
from classes.LevelComplete import LevelComplete
from classes.Menu import Menu
from classes.Sound import Sound
from entities.Yasmin import Yasmin


windowSize = 640, 480


def main():
    pygame.mixer.pre_init(44100, -16, 2, 4096)
    pygame.init()
    screen = pygame.display.set_mode(windowSize)
    max_frame_rate = 60
    dashboard = Dashboard(screen=screen)
    sound = Sound()
    level = Level(screen, sound, dashboard)
    menu = Menu(screen, dashboard, level, sound)

    while not menu.start:
        menu.update()

    yasmin = Yasmin(0, 0, level, screen, dashboard, sound)
    clock = pygame.time.Clock()
    startTime = pygame.time.get_ticks()

    while not yasmin.restart:
        pygame.display.set_caption("Crazy World running with {:d} FPS".format(int(clock.get_fps())))
        if yasmin.pause:
            yasmin.pauseObj.update()
        else:
            level.drawLevel(yasmin.camera)
            dashboard.update()
            yasmin.update()

            # Check end portal collision
            if level.checkEndPortal(yasmin.rect):
                elapsed = (pygame.time.get_ticks() - startTime) / 1000.0
                levelComplete = LevelComplete(screen, dashboard, sound,
                                               coins=dashboard.coins,
                                               time_elapsed=elapsed)
                while levelComplete.active:
                    events = pygame.event.get()
                    for event in events:
                        if event.type == pygame.QUIT:
                            pygame.quit()
                            sys.exit()
                    levelComplete.update(events)
                    levelComplete.draw()
                    pygame.display.flip()
                    clock.tick(60)

                if levelComplete.nextLevel:
                    break
                elif levelComplete.goMenu:
                    yasmin.restart = True
                    break

        pygame.display.update()
        clock.tick(max_frame_rate)
    return 'restart'


if __name__ == "__main__":
    exitmessage = 'restart'
    while exitmessage == 'restart':
        exitmessage = main()
