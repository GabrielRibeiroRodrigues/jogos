import json
import pygame

from classes.Sprites import Sprites
from classes.Tile import Tile
from entities.Coin import Coin
from entities.CoinBrick import CoinBrick
from entities.Bruno import Bruno
from entities.Mushroom import RedMushroom
from entities.Tiago import Tiago
from entities.CoinBox import CoinBox
from entities.RandomBox import RandomBox
from entities.MovingPlatform import MovingPlatform


class Level:
    def __init__(self, screen, sound, dashboard):
        self.sprites = Sprites()
        self.dashboard = dashboard
        self.sound = sound
        self.screen = screen
        self.level = None
        self.levelLength = 0
        self.entityList = []
        self.background = pygame.image.load("./img/background.png").convert()
        self.bgWidth = self.background.get_width()
        self.hasEndPortal = False
        self.endPortalRect = None

    def loadLevel(self, levelname):
        with open("./levels/{}.json".format(levelname)) as jsonData:
            data = json.load(jsonData)
            self.loadLayers(data)
            self.loadObjects(data)
            self.loadEntities(data)
            self.levelLength = data["length"]

    def loadEntities(self, data):
        try:
            [self.addCoinBox(x, y) for x, y in data["level"]["entities"]["CoinBox"]]
            [self.addGoomba(x, y) for x, y in data["level"]["entities"]["Goomba"]]
            [self.addKoopa(x, y) for x, y in data["level"]["entities"]["Koopa"]]
            [self.addCoin(x, y) for x, y in data["level"]["entities"]["coin"]]
            [self.addCoinBrick(x, y) for x, y in data["level"]["entities"]["coinBrick"]]
            [self.addRandomBox(x, y, item) for x, y, item in data["level"]["entities"]["RandomBox"]]
        except:
            # if no entities in Level
            pass
        if "MovingPlatform" in data.get("level", {}).get("entities", {}):
            for platform in data["level"]["entities"]["MovingPlatform"]:
                # platform = [x, y, direction, amplitude, speed]
                self.entityList.append(MovingPlatform(
                    platform[0], platform[1], self, self.screen,
                    platform[2], platform[3], platform[4]
                ))
        try:
            for x, y in data["level"]["entities"]["EndPortal"]:
                self.endPortalRect = pygame.Rect(x * 32, y * 32, 64, 64)
                self.hasEndPortal = True
        except:
            self.hasEndPortal = False
            self.endPortalRect = None

    def loadLayers(self, data):
        layers = []
        for x in range(*data["level"]["layers"]["sky"]["x"]):
            layers.append(
                (
                        [
                            Tile(self.sprites.spriteCollection.get("sky"), None)
                            for y in range(*data["level"]["layers"]["sky"]["y"])
                        ]
                        + [
                            Tile(
                                self.sprites.spriteCollection.get(
                                    "ground" if y == data["level"]["layers"]["ground"]["y"][0] else "ground_dirt"
                                ),
                                pygame.Rect(x * 32, (y - 1) * 32, 32, 32),
                            )
                            for y in range(*data["level"]["layers"]["ground"]["y"])
                        ]
                )
            )
        self.level = list(map(list, zip(*layers)))

    def loadObjects(self, data):
        for x, y in data["level"]["objects"]["bush"]:
            self.addBushSprite(x, y)
        for x, y in data["level"]["objects"]["cloud"]:
            self.addCloudSprite(x, y)
        for x, y, z in data["level"]["objects"]["pipe"]:
            self.addPipeSprite(x, y, z)
        for x, y in data["level"]["objects"]["sky"]:
            self.level[y][x] = Tile(self.sprites.spriteCollection.get("sky"), None)
        for x, y in data["level"]["objects"]["ground"]:
            self.level[y][x] = Tile(
                self.sprites.spriteCollection.get("ground"),
                pygame.Rect(x * 32, y * 32, 32, 32),
            )

    def updateEntities(self, cam):
        player = cam.entity
        for entity in self.entityList:
            entity.update(cam)
            if entity.alive is None:
                self.entityList.remove(entity)
            # Moving platform player collision: player stands on top
            if isinstance(entity, MovingPlatform) and entity.alive:
                platform = entity
                if player.rect.colliderect(platform.rect):
                    # Check if player is coming from above (player bottom overlaps platform top)
                    player_bottom = player.rect.bottom
                    platform_top = platform.rect.top
                    # Player was above or at platform top and is now overlapping
                    if player.vel.y >= 0 and player_bottom >= platform_top and player_bottom <= platform.rect.bottom:
                        # Snap player to platform top
                        player.rect.bottom = platform_top
                        player.vel.y = 0
                        player.onGround = True
                        # Move player horizontally with platform
                        if platform.direction == "horizontal":
                            player.rect.x += platform.vel
                        else:
                            player.rect.y += platform.vel

    def checkEndPortal(self, yasminRect):
        if not self.hasEndPortal or self.endPortalRect is None:
            return False
        return yasminRect.colliderect(self.endPortalRect)

    def drawBackground(self, camera):
        offset_x = int(camera.pos.x * 32 * 0.3) % self.bgWidth
        self.screen.blit(self.background, (-offset_x, 0))
        self.screen.blit(self.background, (self.bgWidth - offset_x, 0))

    def drawLevel(self, camera):
        sky_sprite = self.sprites.spriteCollection.get("sky")
        try:
            self.drawBackground(camera)
            for y in range(0, 15):
                for x in range(0 - int(camera.pos.x + 1), 20 - int(camera.pos.x - 1)):
                    if self.level[y][x].sprite is None:
                        continue
                    if self.level[y][x].sprite is sky_sprite:
                        continue
                    self.level[y][x].sprite.drawSprite(
                        x + camera.pos.x, y, self.screen
                    )
            self.updateEntities(camera)
            if self.hasEndPortal and self.endPortalRect:
                drawRect = pygame.Rect(
                    self.endPortalRect.x + camera.x,
                    self.endPortalRect.y,
                    self.endPortalRect.width,
                    self.endPortalRect.height
                )
                pygame.draw.rect(self.screen, (0, 255, 100), drawRect, 3)
                inner = drawRect.inflate(-6, -6)
                pygame.draw.rect(self.screen, (0, 180, 70), inner, 2)
        except IndexError:
            return

    def addCloudSprite(self, x, y):
        return

    def addPipeSprite(self, x, y, length=2):
        portal_top = 12  # portal occupies rows 12-13, sitting on ground at row 14
        try:
            # invisible collision above the portal
            for i in range(y, portal_top):
                self.level[i][x] = Tile(None, pygame.Rect(x * 32, i * 32, 32, 32))
                self.level[i][x + 1] = Tile(None, pygame.Rect((x + 1) * 32, i * 32, 32, 32))
            # portal top row
            self.level[portal_top][x] = Tile(
                self.sprites.spriteCollection.get("portal_tl"),
                pygame.Rect(x * 32, portal_top * 32, 32, 32),
            )
            self.level[portal_top][x + 1] = Tile(
                self.sprites.spriteCollection.get("portal_tr"),
                pygame.Rect((x + 1) * 32, portal_top * 32, 32, 32),
            )
            # portal bottom row (row 13, sits on ground at row 14)
            self.level[portal_top + 1][x] = Tile(
                self.sprites.spriteCollection.get("portal_bl"),
                pygame.Rect(x * 32, (portal_top + 1) * 32, 32, 32),
            )
            self.level[portal_top + 1][x + 1] = Tile(
                self.sprites.spriteCollection.get("portal_br"),
                pygame.Rect((x + 1) * 32, (portal_top + 1) * 32, 32, 32),
            )
        except IndexError:
            return

    def addBushSprite(self, x, y):
        try:
            self.level[y][x] = Tile(self.sprites.spriteCollection.get("bush_1"), None)
            self.level[y][x + 1] = Tile(
                self.sprites.spriteCollection.get("bush_2"), None
            )
            self.level[y][x + 2] = Tile(
                self.sprites.spriteCollection.get("bush_3"), None
            )
        except IndexError:
            return

    def addCoinBox(self, x, y):
        self.level[y][x] = Tile(None, pygame.Rect(x * 32, y * 32 - 1, 32, 32))
        self.entityList.append(
            CoinBox(
                self.screen,
                self.sprites.spriteCollection,
                x,
                y,
                self.sound,
                self.dashboard,
            )
        )

    def addRandomBox(self, x, y, item):
        self.level[y][x] = Tile(None, pygame.Rect(x * 32, y * 32 - 1, 32, 32))
        self.entityList.append(
            RandomBox(
                self.screen,
                self.sprites.spriteCollection,
                x,
                y,
                item,
                self.sound,
                self.dashboard,
                self
            )
        )

    def addCoin(self, x, y):
        self.entityList.append(Coin(self.screen, self.sprites.spriteCollection, x, y))

    def addCoinBrick(self, x, y):
        self.level[y][x] = Tile(None, pygame.Rect(x * 32, y * 32 - 1, 32, 32))
        self.entityList.append(
            CoinBrick(
                self.screen,
                self.sprites.spriteCollection,
                x,
                y,
                self.sound,
                self.dashboard
            )
        )

    def addGoomba(self, x, y):
        self.entityList.append(
            Bruno(self.screen, self.sprites.spriteCollection, x, y, self, self.sound)
        )

    def addKoopa(self, x, y):
        self.entityList.append(
            Tiago(self.screen, self.sprites.spriteCollection, x, y, self, self.sound)
        )

    def addRedMushroom(self, x, y):
        self.entityList.append(
            RedMushroom(self.screen, self.sprites.spriteCollection, x, y, self, self.sound)
        )
