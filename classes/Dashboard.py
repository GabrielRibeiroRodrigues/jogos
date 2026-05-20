import pygame

from classes.Font import Font


class Dashboard(Font):
    def __init__(self, filePath=None, size=None, screen=None):
        Font.__init__(self)
        self.state = "menu"
        self.screen = screen
        self.levelName = ""
        self.points = 0
        self.ticks = 0
        self.time = 0
        self.yasmin = None

    def update(self):
        self.drawText("CRAZY WORLD", 50, 20, 15)
        self.drawText(self.pointString(), 50, 37, 15)

        self.drawText("FASE", 380, 20, 15)
        self.drawText(str(self.levelName), 388, 37, 15)

        self.drawText("TEMPO", 505, 20, 15)
        if self.state != "menu":
            self.drawText(self.timeString(), 520, 37, 15)

        if self.yasmin and self.yasmin.powerup_active:
            ratio = self.yasmin.powerup_timer / self.yasmin.powerup_duration
            bar_width = int(100 * ratio)
            pygame.draw.rect(self.screen, (0, 0, 0), (248, 20, 104, 20))
            pygame.draw.rect(self.screen, (0, 200, 255), (250, 22, bar_width, 16))
            pygame.draw.rect(self.screen, (255, 255, 255), (250, 22, 100, 16), 1)
            self.drawText("ARMA", 260, 20, 10)

        self.ticks += 1
        if self.ticks == 60:
            self.ticks = 0
            self.time += 1

    def pointString(self):
        return "{:06d}".format(self.points)

    def timeString(self):
        return "{:03d}".format(self.time)
