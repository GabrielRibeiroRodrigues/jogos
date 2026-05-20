import pygame

from classes.Animation import Animation
from classes.Camera import Camera
from classes.Collider import Collider
from classes.EntityCollider import EntityCollider
from classes.Input import Input
from classes.Sprites import Sprites
from entities.EntityBase import EntityBase
from entities.Projectile import Projectile
from traits.bounce import bounceTrait
from traits.dash import DashTrait
from traits.go import GoTrait
from traits.jump import JumpTrait
from traits.melee import MeleeTrait
from classes.Pause import Pause

spriteCollection = Sprites().spriteCollection
smallAnimation = Animation(
    [
        spriteCollection["yasmin_run1"].image,
        spriteCollection["yasmin_run2"].image,
        spriteCollection["yasmin_run3"].image,
    ],
    spriteCollection["yasmin_idle"].image,
    spriteCollection["yasmin_jump"].image,
)


class Yasmin(EntityBase):
    def __init__(self, x, y, level, screen, dashboard, sound, gravity=0.8):
        super(Yasmin, self).__init__(x, y, gravity)
        self.camera = Camera(self.rect, self)
        self.sound = sound
        self.input = Input(self)
        self.inAir = False
        self.inJump = False
        self.powerUpState = 0
        self.invincibilityFrames = 0
        self.traits = {
            "jumpTrait": JumpTrait(self),
            "goTrait": GoTrait(smallAnimation, screen, self.camera, self),
            "bounceTrait": bounceTrait(self),
            "dashTrait": DashTrait(self),
        }
        self.dashTrait = self.traits["dashTrait"]
        self.meleeTrait = MeleeTrait(self)
        self.attackImage = spriteCollection["yasmin_break"].image
        self.powerup_active = False
        self.powerup_timer = 0
        self.powerup_duration = 600
        self.projectiles = []
        self.levelObj = level
        self.collision = Collider(self, level)
        self.screen = screen
        self.EntityCollider = EntityCollider(self)
        self.dashboard = dashboard
        self.restart = False
        self.restart_phase = False
        self.go_to_menu = False
        self.pause = False
        self.pauseObj = Pause(screen, self, dashboard)

    def update(self):
        if self.invincibilityFrames > 0:
            self.invincibilityFrames -= 1
        self.dashTrait.update()
        self.dashTrait.draw(self.screen, self.camera)
        self.updateTraits()
        self.meleeTrait.update()
        self._checkMeleeHits()
        self._updateProjectiles()
        if self.powerup_active:
            self.powerup_timer -= 1
            if self.powerup_timer <= 0:
                self.powerup_active = False
        self.moveYasmin()
        self.camera.move()
        self.applyGravity()
        self.checkEntityCollision()
        self.input.checkForInput()

    def moveYasmin(self):
        self.rect.y += self.vel.y
        self.collision.checkY()
        self.rect.x += self.vel.x
        self.collision.checkX()

    def _checkMeleeHits(self):
        hitbox = self.meleeTrait.get_hitbox()
        if hitbox is None:
            return
        for ent in self.levelObj.entityList:
            if ent.alive and ent.alive is not None and ent.type == "Mob":
                if hitbox.colliderect(ent.rect):
                    ent.on_hit(self.traits["goTrait"].heading)

    def _updateProjectiles(self):
        for proj in self.projectiles[:]:
            proj.update(self.camera, self.levelObj.entityList)
            if not proj.alive:
                self.projectiles.remove(proj)

    def checkEntityCollision(self):
        for ent in self.levelObj.entityList[:]:
            collisionState = self.EntityCollider.check(ent)
            if collisionState.isColliding:
                if ent.type == "Item":
                    self._onCollisionWithItem(ent)
                elif ent.type == "Block":
                    self._onCollisionWithBlock(ent)
                elif ent.type == "Mob":
                    self._onCollisionWithMob(ent, collisionState)

    def _onCollisionWithItem(self, item):
        if item in self.levelObj.entityList:
            self.levelObj.entityList.remove(item)
        self.activatePowerup()
        self.sound.play_sfx(self.sound.powerup)

    def _onCollisionWithBlock(self, block):
        if not block.triggered:
            self.sound.play_sfx(self.sound.bump)
        block.triggered = True

    def _onCollisionWithMob(self, mob, collisionState):
        if (mob.alive and mob.alive is not None
                and mob.hit_stun == 0
                and collisionState.isColliding
                and not self.invincibilityFrames):
            self.gameOver()

    def activatePowerup(self):
        self.powerup_active = True
        self.powerup_timer = self.powerup_duration

    def fireProjectile(self):
        if not self.powerup_active:
            return
        direction = self.traits["goTrait"].heading
        px = self.rect.centerx
        py = self.rect.centery - 4
        self.projectiles.append(Projectile(px, py, direction, self.screen))

    def bounce(self):
        self.traits["bounceTrait"].jump = True

    def killEntity(self, ent):
        ent.alive = False
        self.dashboard.points += 100

    def gameOver(self):
        if self.restart_phase:
            return
        srf = pygame.Surface((640, 480))
        srf.set_colorkey((255, 255, 255), pygame.RLEACCEL)
        srf.set_alpha(128)
        self.sound.music_channel.stop()
        self.sound.music_channel.play(self.sound.death)
        for i in range(500, 20, -2):
            srf.fill((0, 0, 0))
            pygame.draw.circle(
                srf,
                (255, 255, 255),
                (int(self.camera.x + self.rect.x) + 16, self.rect.y + 16),
                i,
            )
            self.screen.blit(srf, (0, 0))
            pygame.display.update()
            self.input.checkForInput()
        while self.sound.music_channel.get_busy():
            pygame.display.update()
            self.input.checkForInput()
        self.restart_phase = True

    def getPos(self):
        return self.camera.x + self.rect.x, self.rect.y

    def setPos(self, x, y):
        self.rect.x = x
        self.rect.y = y
