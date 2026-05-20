import sys
import pygame


class VictoryScreen:
    def __init__(self, screen, dashboard):
        self.screen = screen
        self.dashboard = dashboard

    def show(self):
        clock = pygame.time.Clock()
        font_big = pygame.font.SysFont("monospace", 48, bold=True)
        font_small = pygame.font.SysFont("monospace", 24)
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key in (pygame.K_RETURN, pygame.K_SPACE, pygame.K_ESCAPE):
                        return "menu"
            self.screen.fill((5, 8, 0))
            w, h = self.screen.get_size()
            # grade decorativa
            for gx in range(0, w, 40):
                for gy in range(0, h, 40):
                    pygame.draw.circle(self.screen, (25, 35, 10), (gx, gy), 1)
            title    = font_big.render("MISSION COMPLETE", True, (255, 220, 0))
            subtitle = font_small.render("SCORE  {:06d}".format(self.dashboard.points), True, (255, 160, 40))
            hint     = font_small.render("PRESS ENTER", True, (160, 130, 50))
            # linha decorativa
            pygame.draw.line(self.screen, (180, 130, 0),
                             (w//2 - 200, h//2 - 55), (w//2 + 200, h//2 - 55), 1)
            pygame.draw.line(self.screen, (180, 130, 0),
                             (w//2 - 200, h//2 + 30), (w//2 + 200, h//2 + 30), 1)
            self.screen.blit(title,    (w//2 - title.get_width()//2,    h//2 - 90))
            self.screen.blit(subtitle, (w//2 - subtitle.get_width()//2, h//2 - 20))
            self.screen.blit(hint,     (w//2 - hint.get_width()//2,     h//2 + 50))
            pygame.display.flip()
            clock.tick(60)
