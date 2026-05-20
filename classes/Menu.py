import json
import sys
import pygame


class Menu:
    def __init__(self, screen, dashboard, level, sound):
        self.screen = screen
        self.sound = sound
        self.start = False
        self.inSettings = False
        self.state = 0
        self.level = level
        self.music = True
        self.sfx = True
        self.dashboard = dashboard
        self.blink_timer = 0
        self.pulse_timer = 0
        self.loadSettings("./settings.json")

    def update(self):
        self.checkInput()
        self.pulse_timer = (self.pulse_timer + 1) % 120
        self.blink_timer = (self.blink_timer + 1) % 60

        self._drawBackground()

        if not self.inSettings:
            self._drawTitleBox()
            self._drawMenu()
        else:
            self._drawTitleBox()
            self._drawSettings()

        pygame.display.update()

    # ── background ────────────────────────────────────────────────────────────

    def _drawBackground(self):
        offset_x = int(self.pulse_timer * 0.4) % self.level.bgWidth
        self.screen.blit(self.level.background, (-offset_x, 0))
        self.screen.blit(self.level.background, (self.level.bgWidth - offset_x, 0))

        # ground strip at bottom
        for x in range(20):
            self.screen.blit(
                self.level.sprites.spriteCollection.get("ground").image,
                (x * 32, 13 * 32),
            )
            self.screen.blit(
                self.level.sprites.spriteCollection.get("ground_dirt").image,
                (x * 32, 14 * 32),
            )

        # yasmin standing on ground
        yasmin_img = self.level.sprites.spriteCollection.get("yasmin_idle").image
        if yasmin_img:
            self.screen.blit(yasmin_img, (2 * 32, 12 * 32))

    # ── title box ─────────────────────────────────────────────────────────────

    def _drawTitleBox(self):
        W, H = 340, 120
        bx, by = (640 - W) // 2, 55

        # pulsing border brightness
        pulse = abs(self.pulse_timer - 60) / 60.0   # 0.0 → 1.0 → 0.0
        border_color = (
            int(0   + pulse * 80),
            int(180 + pulse * 75),
            int(160 + pulse * 95),
        )

        # dark panel
        panel = pygame.Surface((W, H), pygame.SRCALPHA)
        panel.fill((0, 10, 25, 210))
        self.screen.blit(panel, (bx, by))

        # border
        pygame.draw.rect(self.screen, border_color, (bx, by, W, H), 2)

        # corner accents
        accent = (0, 255, 220)
        size = 8
        for cx, cy in [(bx, by), (bx + W - size, by),
                       (bx, by + H - size), (bx + W - size, by + H - size)]:
            pygame.draw.rect(self.screen, accent, (cx, cy, size, size))

        # title text
        self.dashboard.drawText("CRAZY", bx + 30, by + 10, 52, (220,  30,  30))
        self.dashboard.drawText("WORLD", bx + 30, by + 62, 52, (255, 200,   0))

    # ── cursor ────────────────────────────────────────────────────────────────

    def _drawCursor(self, y_positions):
        if self.blink_timer < 45:
            y = y_positions[self.state]
            pts = [(150, y + 6), (150, y + 22), (166, y + 14)]
            pygame.draw.polygon(self.screen, (255, 50, 50), pts)

    # ── menu ──────────────────────────────────────────────────────────────────

    def _drawMenu(self):
        options = [("JOGAR", 280), ("OPCOES", 320), ("SAIR", 360)]
        y_positions = [y for _, y in options]
        self._drawCursor(y_positions)

        for i, (label, y) in enumerate(options):
            color = (255, 220, 60) if i == self.state else (200, 190, 160)
            self.dashboard.drawText(label, 180, y, 24, color)

    # ── settings ──────────────────────────────────────────────────────────────

    def _drawSettings(self):
        y_positions = [280, 320, 360]
        self._drawCursor(y_positions)

        rows = [
            ("MUSICA", "SIM" if self.music else "NAO"),
            ("SONS",   "SIM" if self.sfx   else "NAO"),
            ("VOLTAR", ""),
        ]
        for i, (label, value) in enumerate(rows):
            color = (255, 220, 60) if i == self.state else (200, 190, 160)
            self.dashboard.drawText(label, 180, y_positions[i], 24, color)
            if value:
                self.dashboard.drawText(value, 340, y_positions[i], 24, color)

    # ── settings persistence ───────────────────────────────────────────────────

    def loadSettings(self, url):
        try:
            with open(url) as jsonData:
                data = json.load(jsonData)
                self.music = bool(data.get("sound", False))
                self.sfx   = bool(data.get("sfx",   False))
                if self.music:
                    self.sound.music_channel.play(self.sound.soundtrack, loops=-1)
                self.sound.allowSFX = self.sfx
        except (IOError, OSError):
            self.music = False
            self.sfx   = False
            self.sound.allowSFX = False
            self.saveSettings(url)

    def saveSettings(self, url):
        with open(url, "w") as f:
            json.dump({"sound": self.music, "sfx": self.sfx}, f)

    # ── input ─────────────────────────────────────────────────────────────────

    def checkInput(self):
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type != pygame.KEYDOWN:
                continue

            key = event.key

            if key == pygame.K_ESCAPE:
                if self.inSettings:
                    self.inSettings = False
                    self.state = 0
                else:
                    pygame.quit()
                    sys.exit()

            elif key in (pygame.K_UP, pygame.K_k):
                if self.state > 0:
                    self.state -= 1

            elif key in (pygame.K_DOWN, pygame.K_j):
                if self.state < 2:
                    self.state += 1

            elif key == pygame.K_RETURN:
                self._handleEnter()

    def _handleEnter(self):
        if not self.inSettings:
            if self.state == 0:
                self.dashboard.state = "start"
                self.dashboard.time  = 0
                self.start = True
            elif self.state == 1:
                self.inSettings = True
                self.state = 0
            elif self.state == 2:
                pygame.quit()
                sys.exit()
        else:
            if self.state == 0:
                self.music = not self.music
                if self.music:
                    self.sound.music_channel.play(self.sound.soundtrack, loops=-1)
                else:
                    self.sound.music_channel.stop()
                self.saveSettings("./settings.json")
            elif self.state == 1:
                self.sfx = not self.sfx
                self.sound.allowSFX = self.sfx
                self.saveSettings("./settings.json")
            elif self.state == 2:
                self.inSettings = False
                self.state = 0
