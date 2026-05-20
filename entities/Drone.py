import pygame

from classes.Collider import Collider
from classes.Maths import Vec2D
from entities.EntityBase import EntityBase
from traits.leftrightwalk import LeftRightWalkTrait

COLOR       = (220, 60,  60)   # red
COLOR_DEAD  = (160, 40,  40)
COLOR_HIT   = (255, 160, 160)


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
                self._draw(camera, COLOR_HIT)
            return

        self.leftrightTrait.update()
        self._draw(camera, COLOR)

    def _draw(self, camera, color):
        pygame.draw.rect(
            self.screen, color,
            (self.rect.x + camera.x, self.rect.y, self.rect.width, self.rect.height)
        )

    def _onDead(self, camera):
        if self.timer < self.timeAfterDeath:
            self.textPos.y -= 0.5
            self.dashboard.drawText("100", self.textPos.x + camera.x, self.textPos.y, 8)
            self._draw(camera, COLOR_DEAD)
        else:
            self.alive = None
        self.timer += 0.1
