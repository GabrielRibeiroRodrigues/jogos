import pygame


class DashTrait:
    def __init__(self, entity):
        self.entity = entity
        self.isDashing = False
        self.dashFrames = 0
        self.dashDuration = 8
        self.dashSpeed = 10
        self.cooldownTimer = 0
        self.cooldown = 60
        self.trailPositions = []
        self.trailLength = 5
        self.wasShiftPressed = False

    def update(self):
        pressedKeys = pygame.key.get_pressed()
        shiftPressed = pressedKeys[pygame.K_LSHIFT] or pressedKeys[pygame.K_RSHIFT]

        # Decrement cooldown
        if self.cooldownTimer > 0:
            self.cooldownTimer -= 1

        # Detect fresh Shift press (not held) to trigger dash
        if shiftPressed and not self.wasShiftPressed:
            if self.cooldownTimer == 0 and not self.isDashing:
                self.isDashing = True
                self.dashFrames = self.dashDuration
                self.cooldownTimer = self.cooldown
                # Direction from GoTrait heading
                direction = self.entity.traits["goTrait"].heading
                self.entity.vel.x = self.dashSpeed * direction

        self.wasShiftPressed = shiftPressed

        if self.isDashing:
            # Store current position in trail
            pos = self.entity.getPos()
            self.trailPositions.append((pos[0], pos[1], self.entity.rect.width, self.entity.rect.height))
            if len(self.trailPositions) > self.trailLength:
                self.trailPositions.pop(0)

            # Keep applying dash velocity
            direction = self.entity.traits["goTrait"].heading
            self.entity.vel.x = self.dashSpeed * direction

            self.dashFrames -= 1
            if self.dashFrames <= 0:
                self.isDashing = False
        else:
            # Slowly fade out trail
            if self.trailPositions:
                self.trailPositions.pop(0)

    def draw(self, screen, camera):
        if not self.trailPositions:
            return
        trail_surface = pygame.Surface((screen.get_width(), screen.get_height()), pygame.SRCALPHA)
        for i, (x, y, w, h) in enumerate(self.trailPositions):
            alpha = int(80 * (i + 1) / self.trailLength)
            pygame.draw.rect(trail_surface, (50, 100, 255, alpha), (x, y, w, h))
        screen.blit(trail_surface, (0, 0))
