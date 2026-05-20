import pygame


class MeleeTrait:
    def __init__(self, entity):
        self.entity = entity
        self.is_attacking = False
        self.attack_timer = 0
        self.attack_duration = 12
        self.cooldown = 0
        self.cooldown_duration = 20

    def trigger(self):
        if self.cooldown > 0:
            return
        self.is_attacking = True
        self.attack_timer = self.attack_duration
        self.cooldown = self.cooldown_duration

    def update(self):
        if self.cooldown > 0:
            self.cooldown -= 1
        if self.attack_timer > 0:
            self.attack_timer -= 1
            if self.attack_timer == 0:
                self.is_attacking = False

    def get_hitbox(self):
        if not self.is_attacking:
            return None
        r = self.entity.rect
        heading = self.entity.traits["goTrait"].heading
        if heading == 1:
            return pygame.Rect(r.right, r.top + 4, 28, 24)
        else:
            return pygame.Rect(r.left - 28, r.top + 4, 28, 24)
