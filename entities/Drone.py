import pygame

from classes.Collider import Collider
from classes.Maths import Vec2D
from entities.EntityBase import EntityBase
from traits.leftrightwalk import LeftRightWalkTrait

# Soldado de infantaria — verde militar
_HELMET  = (30,  70,  20)
_VISOR   = (180,  40,  10)
_BODY    = (45,  100,  30)
_LIMB    = (35,   80,  20)
_GUN     = (80,   70,  50)

_BODY_HIT   = (255, 160,  80)
_BODY_DEAD  = (30,   45,  15)


class Drone(EntityBase):
    def __init__(self, screen, spriteColl, x, y, level, sound, dashboard):
        super().__init__(x, y - 1, 1.25)
        self.screen = screen
        self.leftrightTrait = LeftRightWalkTrait(self, level)
        self.collision = Collider(self, level)
        self.type = "Mob"
        self.hp = 1
        self.max_hp = 1
        self.dashboard = dashboard
        self.levelObj = level
        self.sound = sound
        self.textPos = Vec2D(0, 0)

    def update(self, camera):
        if self.alive is None:
            return

        if not self.alive:
            self._onDead(camera)
            return

        self.applyGravity()

        if self.hit_stun > 0:
            self.hit_stun -= 1
            self.rect.y += int(self.vel.y)
            self.collision.checkY()
            self.rect.x += int(self.knockback_vel)
            self.knockback_vel *= 0.8
            if self.hit_stun == 0 and self.hp <= 0:
                self.alive = False
                self.timer = 0
                self.textPos = Vec2D(self.rect.x + 3, self.rect.y)
                self.dashboard.points += 100
            if (self.hit_stun // 4) % 2 == 0:
                self._draw(camera, hit=True)
            return

        self.leftrightTrait.update()
        self._draw(camera, hit=False)

    def _draw(self, camera, hit=False):
        bx = self.rect.x + camera.x
        by = self.rect.y
        body  = _BODY_HIT  if hit else _BODY
        limb  = _BODY_HIT  if hit else _LIMB
        helm  = _BODY_HIT  if hit else _HELMET

        heading = self.leftrightTrait.direction  # 1=right, -1=left

        # cabeça / capacete
        pygame.draw.rect(self.screen, helm,  (bx + 10, by + 1,  12, 9))
        # viseira
        pygame.draw.rect(self.screen, _VISOR, (bx + 11, by + 4,  10, 4))
        # corpo
        pygame.draw.rect(self.screen, body,  (bx + 8,  by + 11, 16, 11))
        # braço esquerdo
        pygame.draw.rect(self.screen, limb,  (bx + 3,  by + 11,  5,  7))
        # braço direito
        pygame.draw.rect(self.screen, limb,  (bx + 24, by + 11,  5,  7))
        # perna esquerda
        pygame.draw.rect(self.screen, limb,  (bx + 9,  by + 23,  5,  8))
        # perna direita
        pygame.draw.rect(self.screen, limb,  (bx + 17, by + 23,  5,  8))
        # arma (direção do movimento)
        if heading == 1:
            pygame.draw.rect(self.screen, _GUN, (bx + 28, by + 13, 6, 3))
        else:
            pygame.draw.rect(self.screen, _GUN, (bx - 2,  by + 13, 6, 3))

    def _onDead(self, camera):
        if self.timer < self.timeAfterDeath:
            self.textPos.y -= 0.5
            self.dashboard.drawText("100", self.textPos.x + camera.x, self.textPos.y, 8,
                                    (255, 220, 60))
            bx = self.rect.x + camera.x
            by = self.rect.y
            pygame.draw.rect(self.screen, _BODY_DEAD, (bx + 8, by + 5, 16, 24))
        else:
            self.alive = None
        self.timer += 0.1
