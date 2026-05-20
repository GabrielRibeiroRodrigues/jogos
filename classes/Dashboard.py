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
        # faixa de fundo semitransparente no topo
        hud_bar = pygame.Surface((640, 52), pygame.SRCALPHA)
        hud_bar.fill((8, 5, 0, 180))
        self.screen.blit(hud_bar, (0, 0))
        pygame.draw.line(self.screen, (140, 100, 0), (0, 52), (640, 52), 1)

        self.drawText("SCORE",            50, 8,  11, (160, 140, 80))
        self.drawText(self.pointString(), 50, 22, 15, (255, 220, 60))

        self.drawText("STAGE",           310, 8,  11, (160, 140, 80))
        self.drawText(str(self.levelName), 318, 22, 15, (255, 220, 60))

        self.drawText("TIME",            505, 8,  11, (160, 140, 80))
        if self.state != "menu":
            self.drawText(self.timeString(), 512, 22, 15, (255, 220, 60))

        if self.yasmin and self.yasmin.powerup_active:
            ratio = self.yasmin.powerup_timer / self.yasmin.powerup_duration
            bar_width = int(100 * ratio)
            pygame.draw.rect(self.screen, (20, 15, 0),   (178, 10, 104, 14))
            pygame.draw.rect(self.screen, (200, 160, 0), (180, 12, bar_width, 10))
            pygame.draw.rect(self.screen, (255, 200, 0), (180, 12, 100, 10), 1)
            self.drawText("WEAPON", 184, 6, 10, (255, 200, 0))

        self.ticks += 1
        if self.ticks == 60:
            self.ticks = 0
            self.time += 1

    def pointString(self):
        return "{:06d}".format(self.points)

    def timeString(self):
        return "{:03d}".format(self.time)
