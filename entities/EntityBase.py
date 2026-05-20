import pygame

from classes.Maths import Vec2D


class EntityBase(object):
    def __init__(self, x, y, gravity):
        self.vel = Vec2D()
        self.rect = pygame.Rect(x * 32, y * 32, 32, 32)
        self.gravity = gravity
        self.traits = None
        self.alive = True
        self.active = True
        self.bouncing = False
        self.timeAfterDeath = 5
        self.timer = 0
        self.type = ""
        self.onGround = False
        self.obeyGravity = True
        self.hp = 1
        self.max_hp = 1
        self.hit_stun = 0
        self.knockback_vel = 0

    def on_hit(self, direction):
        """direction: 1=right, -1=left (knockback vai nessa direção)"""
        self.hp -= 1
        self.hit_stun = 20
        self.knockback_vel = direction * 4
        
    def applyGravity(self):
        if self.obeyGravity:
            self.vel.y += self.gravity

    def updateTraits(self):
        for trait in self.traits.values():
            try:
                trait.update()
            except AttributeError:
                pass

    def getPosIndex(self):
        return Vec2D(self.rect.x // 32, self.rect.y // 32)

    def getPosIndexAsFloat(self):
        return Vec2D(self.rect.x / 32.0, self.rect.y / 32.0)
