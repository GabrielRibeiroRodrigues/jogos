import pygame

from classes.Font import Font


class Dashboard(Font):
    def __init__(self, filePath=None, size=None, screen=None):
        Font.__init__(self)
        self.state = "menu"
        self.screen = screen
        self.levelName = ""
        self.points = 0
        self.coins = 0
        self.ticks = 0
        self.time = 0

    def update(self):
        self.drawText("CRAZY WORLD", 50, 20, 15)
        self.drawText(self.pointString(), 50, 37, 15)

        self.drawText("@x{}".format(self.coinString()), 250, 37, 15)

        self.drawText("FASE", 380, 20, 15)
        self.drawText(str(self.levelName), 388, 37, 15)

        self.drawText("TEMPO", 505, 20, 15)
        if self.state != "menu":
            self.drawText(self.timeString(), 520, 37, 15)

        # update Time
        self.ticks += 1
        if self.ticks == 60:
            self.ticks = 0
            self.time += 1

    def coinString(self):
        return "{:02d}".format(self.coins)

    def pointString(self):
        return "{:06d}".format(self.points)

    def timeString(self):
        return "{:03d}".format(self.time)
