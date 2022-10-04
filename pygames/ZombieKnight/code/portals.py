import pygame, random
from setup import *

Vector = pygame.math.Vector2

class Portal(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()

        self.sprites = []
        
        self.load_images()
        self.rect = self.image.get_rect()
        self.rect.bottomleft = (x, y)

        self.mask = pygame.mask.from_surface(self.image)

        self.closing = True

    def update(self, player_group, zombie_group):
        self.animate()
        self.go_through_portal(player_group, zombie_group)

    def animate(self):
        if self.sprite <= len(self.sprites)-1 and self.closing:
            self.sprite += 0.1
        elif self.sprite > 0:
            self.sprite -= 0.1
            self.closing = False
        else:
            self.closing = True

        self.image = self.sprites[int(self.sprite)]

    def go_through_portal(self, player_group, zombie_group):
        character = pygame.sprite.spritecollide(self, player_group, False, pygame.sprite.collide_mask) or pygame.sprite.spritecollide(self, zombie_group, False, pygame.sprite.collide_mask)

        if character:
            character = character[0]
            if self.rect.x == -16 and self.rect.y == 0:
                character.position = Vector(1150, 576+96)
                character.rect.topleft = character.position
            elif self.rect.x == 1200 and self.rect.y == 0:
                character.position = Vector(50, 576+96)
                character.rect.topleft = character.position
            elif self.rect.x == -16 and self.rect.y == 576:
                character.position = Vector(1150, 96)
                character.rect.topleft = character.position
            elif self.rect.x == 1200 and self.rect.y == 576:
                character.position = Vector(50, 96)
                character.rect.topleft = character.position

class Green_Portal(Portal):
    def __init__(self, x, y):
        self.sprite = random.randint(0, 21)
        Portal.__init__(self, x, y)

    def load_images(self):
        for i in range(1, 22):
           self.sprites.append(pygame.transform.scale(pygame.image.load(f"../assets/images/portals/green/tile{i:03d}.png"), (96, 96)))

        self.image = self.sprites[0]

class Purple_Portal(Portal):
    def __init__(self, x, y):
        self.sprite = random.randint(0, 21)
        Portal.__init__(self, x, y)

    def load_images(self):
        for i in range(1, 22):
            self.sprites.append(pygame.transform.scale(pygame.image.load(f"../assets/images/portals/purple/tile{i:03d}.png"), (96, 96)))

        self.image = self.sprites[7]
