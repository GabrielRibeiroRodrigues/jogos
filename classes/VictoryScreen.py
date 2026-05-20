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
            self.screen.fill((5, 10, 30))
            title = font_big.render("MISSAO COMPLETA!", True, (0, 255, 180))
            subtitle = font_small.render("Pontos: {:06d}".format(self.dashboard.points), True, (200, 200, 200))
            hint = font_small.render("ENTER para voltar ao menu", True, (120, 120, 120))
            w, h = self.screen.get_size()
            self.screen.blit(title, (w // 2 - title.get_width() // 2, h // 2 - 80))
            self.screen.blit(subtitle, (w // 2 - subtitle.get_width() // 2, h // 2))
            self.screen.blit(hint, (w // 2 - hint.get_width() // 2, h // 2 + 60))
            pygame.display.flip()
            clock.tick(60)
