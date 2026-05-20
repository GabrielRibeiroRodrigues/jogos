import pygame

from entities.EntityBase import EntityBase


# Caixa de armamento — estilo militar
_FILL      = (55,  70,  20)   # verde-oliva escuro
_BORDER    = (160, 130,  30)  # âmbar/dourado
_ACCENT    = (220, 190,  60)  # dourado claro
_MARK      = (255, 240, 100)  # amarelo brilhante para o "W"

# Caixa usada
_FILL_USED   = (40, 40, 35)
_BORDER_USED = (75, 70, 55)


class PowerBox(EntityBase):
    def __init__(self, screen, spriteCollection, x, y, sound, dashboard, level, gravity=0):
        super().__init__(x, y, gravity)
        self.screen = screen
        self.type = "Block"
        self.triggered = False
        self.spawned = False
        self.time = 0
        self.maxTime = 10
        self.sound = sound
        self.dashboard = dashboard
        self.level = level
        self.vel_anim = 1
        self._pulse = 0

    def update(self, cam):
        if self.triggered and not self.spawned:
            self.level.addWeaponPowerup(self.rect.x // 32, self.rect.y // 32 - 1)
            self.spawned = True

        if self.triggered:
            if self.time < self.maxTime:
                self.time += 1
                self.rect.y -= self.vel_anim
            elif self.time < self.maxTime * 2:
                self.time += 1
                self.rect.y += self.vel_anim
        else:
            self._pulse = (self._pulse + 1) % 60

        self._draw(cam)

    def _draw(self, cam):
        rx = self.rect.x + cam.x
        ry = self.rect.y
        S = 32

        if self.triggered:
            pygame.draw.rect(self.screen, _FILL_USED,   (rx,     ry,     S,     S))
            pygame.draw.rect(self.screen, _BORDER_USED, (rx,     ry,     S,     S), 2)
            return

        # Pulso: varia o brilho ligeiramente
        glow = int(20 * abs((self._pulse - 30) / 30))
        fill = (_FILL[0] + glow, _FILL[1], min(255, _FILL[2] + glow * 2))

        pygame.draw.rect(self.screen, fill,    (rx,     ry,     S,     S))
        pygame.draw.rect(self.screen, _BORDER, (rx,     ry,     S,     S), 2)

        # brilho no canto superior esquerdo
        pygame.draw.line(self.screen, _ACCENT, (rx + 3, ry + 3), (rx + S - 4, ry + 3), 1)
        pygame.draw.line(self.screen, _ACCENT, (rx + 3, ry + 3), (rx + 3,     ry + S - 4), 1)

        # símbolo "W" (weapon) desenhado com 5 barras verticais em V
        cx = rx + S // 2
        pygame.draw.rect(self.screen, _MARK, (cx - 10, ry + 8,  3, 14))  # esq
        pygame.draw.rect(self.screen, _MARK, (cx - 6,  ry + 14, 3,  8))  # centro-esq
        pygame.draw.rect(self.screen, _MARK, (cx - 2,  ry + 8,  3, 14))  # meio
        pygame.draw.rect(self.screen, _MARK, (cx + 3,  ry + 14, 3,  8))  # centro-dir
        pygame.draw.rect(self.screen, _MARK, (cx + 7,  ry + 8,  3, 14))  # dir
