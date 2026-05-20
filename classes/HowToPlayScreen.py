import sys
import pygame


class HowToPlayScreen:
    def __init__(self, screen, dashboard):
        self.screen = screen
        self.dashboard = dashboard

    def show(self):
        clock = pygame.time.Clock()
        blink = 0

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key in (pygame.K_RETURN, pygame.K_SPACE, pygame.K_ESCAPE):
                        return

            blink = (blink + 1) % 60
            self._draw(blink)
            pygame.display.flip()
            clock.tick(60)

    def _draw(self, blink):
        W, H = self.screen.get_size()
        self.screen.fill((5, 8, 0))

        # ── grade de pontos decorativa ─────────────────────────────────────────
        for gx in range(0, W, 40):
            for gy in range(0, H, 40):
                pygame.draw.circle(self.screen, (25, 35, 10), (gx, gy), 1)

        # ── painel central ─────────────────────────────────────────────────────
        PW, PH = 580, 390
        px, py = (W - PW) // 2, (H - PH) // 2
        panel = pygame.Surface((PW, PH), pygame.SRCALPHA)
        panel.fill((10, 8, 0, 220))
        self.screen.blit(panel, (px, py))
        pygame.draw.rect(self.screen, (180, 130, 0), (px, py, PW, PH), 2)

        # cantos
        accent = (255, 200, 0)
        sz = 8
        for cx, cy in [(px, py), (px+PW-sz, py), (px, py+PH-sz), (px+PW-sz, py+PH-sz)]:
            pygame.draw.rect(self.screen, accent, (cx, cy, sz, sz))

        # ── título ─────────────────────────────────────────────────────────────
        self.dashboard.drawText("COMO JOGAR", px + PW//2 - 105, py + 14, 28, (255, 200, 0))
        pygame.draw.line(self.screen, (130, 90, 0), (px + 20, py + 52), (px + PW - 20, py + 52), 1)

        # ── controles ──────────────────────────────────────────────────────────
        self.dashboard.drawText("CONTROLES", px + 28, py + 64, 16, (160, 140, 80))

        controls = [
            (" <- / ->",      "Mover para os lados"),
            (" ESPACO",       "Pular  (2x = pulo duplo)"),
            (" CLICK ESQ",    "Ataque corpo a corpo"),
            (" CLICK DIR",    "Atirar projétil  (requer power-up)"),
            (" ESC",          "Pausar"),
        ]
        for i, (key, desc) in enumerate(controls):
            y = py + 86 + i * 30
            self.dashboard.drawText(key,  px + 28,  y, 15, (255, 180, 40))
            self.dashboard.drawText(desc, px + 170, y, 15, (210, 200, 160))

        pygame.draw.line(self.screen, (100, 70, 0), (px + 20, py + 245), (px + PW - 20, py + 245), 1)

        # ── objetivo ───────────────────────────────────────────────────────────
        self.dashboard.drawText("OBJETIVO", px + 28, py + 255, 16, (160, 140, 80))

        tips = [
            "Atravesse as plataformas moveis sobre os buracos",
            "Soldados=1HP   Soldado Pesado=2HP",
            "Encontre o portal para avancar de fase",
        ]
        for i, tip in enumerate(tips):
            y = py + 277 + i * 28
            self.dashboard.drawText(">>  " + tip, px + 28, y, 13, (200, 190, 140))

        # ── pressione enter ─────────────────────────────────────────────────────
        if blink < 40:
            self.dashboard.drawText(
                "PRESSIONE  ENTER  PARA  COMECAR",
                px + PW//2 - 158, py + PH - 28, 16, (255, 200, 0)
            )
