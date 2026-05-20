import sys
import pygame


class GameOverScreen:
    def __init__(self, screen):
        self.screen = screen

    def show(self):
        clock = pygame.time.Clock()
        font_big = pygame.font.SysFont("monospace", 48, bold=True)
        font_small = pygame.font.SysFont("monospace", 24)
        timer = 180
        while timer > 0:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    return
            timer -= 1
            self.screen.fill((10, 0, 0))
            title = font_big.render("GAME OVER", True, (255, 50, 50))
            hint = font_small.render("Reiniciando fase...", True, (150, 150, 150))
            w, h = self.screen.get_size()
            self.screen.blit(title, (w // 2 - title.get_width() // 2, h // 2 - 40))
            self.screen.blit(hint, (w // 2 - hint.get_width() // 2, h // 2 + 30))
            pygame.display.flip()
            clock.tick(60)
