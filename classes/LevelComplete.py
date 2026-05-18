import pygame
import random
import math
from classes.GaussianBlur import GaussianBlur

class Confetti:
    def __init__(self, screen_width, screen_height):
        self.x = random.randint(0, screen_width)
        self.y = random.randint(-50, 0)
        self.vel_x = random.uniform(-1, 1)
        self.vel_y = random.uniform(2, 5)
        self.color = random.choice([
            (255, 50, 50), (50, 255, 50), (50, 50, 255),
            (255, 255, 50), (255, 50, 255), (50, 255, 255)
        ])
        self.size = random.randint(4, 10)
        self.rotation = random.uniform(0, 360)
        self.rot_speed = random.uniform(-5, 5)

    def update(self):
        self.x += self.vel_x
        self.y += self.vel_y
        self.rotation += self.rot_speed

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, (int(self.x), int(self.y), self.size, self.size))

    def offscreen(self, height):
        return self.y > height


class LevelComplete:
    def __init__(self, screen, dashboard, sound, coins=0, time_elapsed=0):
        self.screen = screen
        self.dashboard = dashboard  # for font rendering
        self.sound = sound
        self.coins = coins
        self.time_elapsed = time_elapsed  # in seconds
        self.confetti = [Confetti(screen.get_width(), screen.get_height()) for _ in range(80)]
        self.active = True
        self.nextLevel = False  # True when user clicks "next level"
        self.goMenu = False     # True when user clicks "menu"
        self.blurSurface = None
        self.alpha = 0  # fade in

        # Play a victory sound if available, else stop current music
        try:
            pygame.mixer.music.stop()
        except:
            pass

    def createBlur(self):
        blur = GaussianBlur()
        return blur.gaussianBlur(self.screen, 5)

    def update(self, events):
        # Fade in
        if self.alpha < 180:
            self.alpha = min(180, self.alpha + 5)

        # Update confetti
        for c in self.confetti[:]:
            c.update()
            if c.offscreen(self.screen.get_height()):
                self.confetti.remove(c)
                self.confetti.append(Confetti(self.screen.get_width(), self.screen.get_height()))

        # Handle input
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN or event.key == pygame.K_SPACE:
                    self.nextLevel = True
                    self.active = False
                elif event.key == pygame.K_ESCAPE:
                    self.goMenu = True
                    self.active = False

    def draw(self):
        # Dark overlay
        overlay = pygame.Surface(self.screen.get_size(), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, self.alpha))
        self.screen.blit(overlay, (0, 0))

        # Draw confetti
        for c in self.confetti:
            c.draw(self.screen)

        sw, sh = self.screen.get_size()

        # Main panel
        panel_w, panel_h = 400, 220
        panel_x = (sw - panel_w) // 2
        panel_y = (sh - panel_h) // 2
        panel = pygame.Surface((panel_w, panel_h), pygame.SRCALPHA)
        panel.fill((20, 20, 40, 210))
        self.screen.blit(panel, (panel_x, panel_y))
        pygame.draw.rect(self.screen, (100, 200, 100), (panel_x, panel_y, panel_w, panel_h), 3)

        # Title text using dashboard font
        # Use dashboard.drawText or direct font rendering
        font = pygame.font.SysFont("Arial", 28, bold=True)
        title = font.render("FASE CONCLUIDA!", True, (100, 255, 100))
        self.screen.blit(title, (panel_x + (panel_w - title.get_width())//2, panel_y + 20))

        # Stats
        font_sm = pygame.font.SysFont("Arial", 16)
        mins = int(self.time_elapsed) // 60
        secs = int(self.time_elapsed) % 60
        stats = [
            f"Gemas: {self.coins}",
            f"Tempo: {mins:02d}:{secs:02d}",
        ]
        for i, line in enumerate(stats):
            surf = font_sm.render(line, True, (200, 200, 255))
            self.screen.blit(surf, (panel_x + 30, panel_y + 80 + i * 25))

        # Buttons
        btn_font = pygame.font.SysFont("Arial", 16, bold=True)

        # Next level button
        btn1 = btn_font.render("[ENTER] Proxima Fase", True, (255, 255, 100))
        self.screen.blit(btn1, (panel_x + (panel_w - btn1.get_width())//2, panel_y + 155))

        # Menu button
        btn2 = btn_font.render("[ESC] Menu", True, (180, 180, 180))
        self.screen.blit(btn2, (panel_x + (panel_w - btn2.get_width())//2, panel_y + 185))
