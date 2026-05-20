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
            # pisca o fundo entre preto e vermelho escuro
            flash = (timer % 20) < 10
            self.screen.fill((18, 0, 0) if flash else (8, 0, 0))
            w, h = self.screen.get_size()
            title = font_big.render("GAME OVER", True, (255, 40, 40))
            hint  = font_small.render("RESTARTING...", True, (140, 90, 60))
            pygame.draw.line(self.screen, (120, 20, 0),
                             (w//2 - 160, h//2 + 10), (w//2 + 160, h//2 + 10), 1)
            self.screen.blit(title, (w//2 - title.get_width()//2, h//2 - 50))
            self.screen.blit(hint,  (w//2 - hint.get_width()//2,  h//2 + 20))
            pygame.display.flip()
            clock.tick(60)
