import pygame, random
from setup import *

Vector = pygame.math.Vector2

class Zombie(pygame.sprite.Sprite):
    def __init__(self, x, y, gender="girl"):
        super().__init__()

        self.sprite = 0
        self.load_images(gender)
        self.rect = self.image.get_rect()

        self.position = Vector(x, y)
        self.velocity = Vector(0, 0)
        self.acceleration = Vector(0, 0)

        self.rect.bottomleft = self.position

        self.HOR_ACC = 0.3
        self.HOR_FRICTION = 0.15

        self.VER_ACC = 0.5

    def load_images(self, gender):
        self.walk_right = []
        self.dead_right = []
        self.walk_left = []
        self.dead_left = []

        for i in range(1, 11):
            self.walk_right.append(pygame.transform.scale(pygame.image.load(f"../assets/images/zombie/{gender}/walk/Walk ({i}).png"), CAR_SIZE))
            self.dead_right.append(pygame.transform.scale(pygame.image.load(f"../assets/images/zombie/{gender}/dead/Dead ({i}).png"), CAR_SIZE))
            self.walk_left.append(pygame.transform.flip(self.walk_right[i-1], True, False))
            self.dead_left.append(pygame.transform.flip(self.dead_right[i-1], True, False))

        self.image = self.walk_right[0]

    def update(self, player_location, portal_location, tile_group):
        self.mask = pygame.mask.from_surface(self.image)

        self.move(player_location, portal_location)
        self.stay_on_platform(tile_group)

    def move(self, player_location, portal_location):
        self.acceleration = Vector(0, self.VER_ACC)

        if self.rect.y <= player_location[1]:
            if self.rect.x < player_location[0]:
                #go right
                self.acceleration.x = self.HOR_ACC
                self.animate(self.walk_right)
            else:
                #go left
                self.acceleration.x = -self.HOR_ACC
                self.animate(self.walk_left)
        else:
            if self.rect.x < portal_location[0]:
                #go right
                self.acceleration.x = self.HOR_ACC
                self.animate(self.walk_right)
            else:
                #go left
                self.acceleration.x = -self.HOR_ACC
                self.animate(self.walk_left)

        self.acceleration.x -= self.velocity.x*self.HOR_FRICTION
        self.velocity += self.acceleration
        self.position += self.velocity+0.5*self.acceleration

        if self.position.x+CAR_SIZE[0]-10 < 0:
            self.position.x = WINDOW_WIDTH
        elif self.position.x > WINDOW_WIDTH:
            self.position.x = -(CAR_SIZE[0]-10)

        self.rect.bottomleft = self.position

    def stay_on_platform(self, tile_group):
        collided_platforms = pygame.sprite.spritecollide(self, tile_group, False, pygame.sprite.collide_mask)

        if collided_platforms and self.velocity.y > 0:
            self.position.y = collided_platforms[0].rect.top+5
            self.velocity.y = 0

    def die(self):
        if self.velocity >= 0:
            self.animate(self.dead_right)
        else:
            self.animate(self.dead_left)

    def animate(self, sprites):
        if self.sprite < len(sprites)-1:
            self.sprite += 0.2
        else:
            self.sprite = 0

        self.image = sprites[int(self.sprite)]
