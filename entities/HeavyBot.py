import pygame

from classes.Collider import Collider
from classes.Maths import Vec2D
from entities.EntityBase import EntityBase
from traits.leftrightwalk import LeftRightWalkTrait

# Soldado pesado — armadura cinza-aço, laranja quando danificado
_ARMOR      = (60,  70,  85)
_ARMOR_DMG  = (140, 70,  20)
_VISOR      = (200,  30,  10)
_JOINT      = (40,  50,  60)
_GUN        = (90,  80,  60)
_HIT        = (255, 180,  80)
_DEAD       = (35,  40,  45)


class HeavyBot(EntityBase):
    def __init__(self, screen, spriteColl, x, y, level, sound, dashboard):
        super().__init__(x, y - 1, 1.25)
        self.screen = screen
        self.leftrightTrait = LeftRightWalkTrait(self, level)
        self.collision = Collider(self, level)
        self.type = "Mob"
        self.hp = 2
        self.max_hp = 2
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
                self.dashboard.points += 200
            if (self.hit_stun // 4) % 2 == 0:
                self._draw(camera, hit=True)
            return

        self.leftrightTrait.update()
        self._draw(camera, hit=False)

    def _draw(self, camera, hit=False):
        # HeavyBot ocupa 32×48 (16px acima do rect normal)
        bx = self.rect.x + camera.x
        by = self.rect.y - 16

        armor = _HIT if hit else (_ARMOR_DMG if self.hp < 2 else _ARMOR)
        joint = _HIT if hit else _JOINT

        heading = self.leftrightTrait.direction  # 1=right, -1=left

        # --- capacete largo ---
        pygame.draw.rect(self.screen, armor,  (bx + 6,  by,      20, 12))
        # viseira
        pygame.draw.rect(self.screen, _VISOR, (bx + 7,  by + 3,  18,  5))
        # ombros (mais largos que o corpo)
        pygame.draw.rect(self.screen, armor,  (bx + 2,  by + 13,  6,  6))
        pygame.draw.rect(self.screen, armor,  (bx + 24, by + 13,  6,  6))
        # torso
        pygame.draw.rect(self.screen, armor,  (bx + 7,  by + 13, 18, 14))
        # juntas dos ombros
        pygame.draw.rect(self.screen, joint,  (bx + 3,  by + 15,  4,  4))
        pygame.draw.rect(self.screen, joint,  (bx + 25, by + 15,  4,  4))
        # braços
        pygame.draw.rect(self.screen, armor,  (bx + 1,  by + 19,  5, 10))
        pygame.draw.rect(self.screen, armor,  (bx + 26, by + 19,  5, 10))
        # cintura
        pygame.draw.rect(self.screen, joint,  (bx + 8,  by + 28,  16,  4))
        # pernas
        pygame.draw.rect(self.screen, armor,  (bx + 7,  by + 33,  7, 14))
        pygame.draw.rect(self.screen, armor,  (bx + 18, by + 33,  7, 14))
        # pés
        pygame.draw.rect(self.screen, joint,  (bx + 5,  by + 44, 10,  4))
        pygame.draw.rect(self.screen, joint,  (bx + 17, by + 44, 10,  4))
        # arma pesada
        if heading == 1:
            pygame.draw.rect(self.screen, _GUN, (bx + 30, by + 20, 8, 5))
            pygame.draw.rect(self.screen, _GUN, (bx + 32, by + 18, 4, 9))
        else:
            pygame.draw.rect(self.screen, _GUN, (bx - 6,  by + 20, 8, 5))
            pygame.draw.rect(self.screen, _GUN, (bx - 4,  by + 18, 4, 9))

    def _onDead(self, camera):
        if self.timer < self.timeAfterDeath:
            self.textPos.y -= 0.5
            self.dashboard.drawText("200", self.textPos.x + camera.x, self.textPos.y, 8,
                                    (255, 220, 60))
            bx = self.rect.x + camera.x
            by = self.rect.y - 16
            pygame.draw.rect(self.screen, _DEAD, (bx + 5, by + 2, 22, 44))
        else:
            self.alive = None
        self.timer += 0.1
