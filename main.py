import sys
import pygame

from classes.Dashboard import Dashboard
from classes.GameOverScreen import GameOverScreen
from classes.Level import Level
from classes.Menu import Menu
from classes.Sound import Sound
from classes.VictoryScreen import VictoryScreen
from entities.Yasmin import Yasmin

PHASES = ["Level2-1", "Level2-2", "Level2-3"]
PHASE_NAMES = ["1", "2", "3"]
windowSize = 640, 480


def run_phase(screen, sound, dashboard, phase_name, phase_display):
    level = Level(screen, sound, dashboard)
    level.loadLevel(phase_name)

    dashboard.state = "start"
    dashboard.time = 0
    dashboard.ticks = 0
    dashboard.levelName = phase_display

    yasmin = Yasmin(0, 0, level, screen, dashboard, sound)
    dashboard.yasmin = yasmin

    clock = pygame.time.Clock()

    while True:
        pygame.display.set_caption(
            "Crazy World - Fase {} - {:d} FPS".format(phase_display, int(clock.get_fps()))
        )

        if yasmin.pause:
            yasmin.pauseObj.update()
        else:
            level.drawLevel(yasmin.camera)
            dashboard.update()
            yasmin.update()

        pygame.display.update()
        clock.tick(60)

        if yasmin.restart_phase:
            return "restart"
        if yasmin.go_to_menu:
            return "menu"
        if level.checkEndPortal(yasmin.rect):
            return "next"


def make_menu_level(screen, sound, dashboard):
    return Level(screen, sound, dashboard)


def main():
    pygame.mixer.pre_init(44100, -16, 2, 4096)
    pygame.init()
    screen = pygame.display.set_mode(windowSize)
    pygame.display.set_caption("Crazy World")

    sound = Sound()
    dashboard = Dashboard(screen=screen)

    menu_level = make_menu_level(screen, sound, dashboard)
    menu = Menu(screen, dashboard, menu_level, sound)
    dashboard.state = "menu"

    while not menu.start:
        menu.update()

    sound.music_channel.stop()

    game_over_screen = GameOverScreen(screen)
    victory_screen = VictoryScreen(screen, dashboard)

    current_phase = 0

    while True:
        result = run_phase(
            screen, sound, dashboard,
            PHASES[current_phase],
            PHASE_NAMES[current_phase],
        )

        if result == "next":
            current_phase += 1
            if current_phase >= len(PHASES):
                victory_screen.show()
                current_phase = 0
                _back_to_menu(screen, sound, dashboard, menu)

        elif result == "restart":
            game_over_screen.show()

        elif result == "menu":
            current_phase = 0
            _back_to_menu(screen, sound, dashboard, menu)


def _back_to_menu(screen, sound, dashboard, menu):
    dashboard.state = "menu"
    dashboard.points = 0
    dashboard.time = 0
    dashboard.ticks = 0
    dashboard.yasmin = None
    menu.level = make_menu_level(screen, sound, dashboard)
    menu.start = False
    while not menu.start:
        menu.update()
    sound.music_channel.stop()


if __name__ == "__main__":
    main()
