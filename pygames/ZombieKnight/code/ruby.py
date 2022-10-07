import pygame, random
from setup import *

class BigRuby:
    def __init__(self, initial_sprite = 0):
        self.sprite = initial_sprite

        self.load_images()

        self.rect = self.image.get_rect()
        self.rect.center = (WINDOW_WIDTH//2, 45)

    def update(self):
        self.animate()
        display_surface.blit(self.image, self.rect)

    def load_images(self):
        self.sprites = []
        for i in range(0, 7):
            self.sprites.append(pygame.transform.scale(pygame.image.load(f"../assets/images/ruby/tile00{i}.png"), (52, 52)))

        self.image = self.sprites[0]

    def animate(self):
        if self.sprite < len(self.sprites)-1:
            self.sprite += 0.2
        else:
            self.sprite = 0

        self.image = self.sprites[int(self.sprite)]

class Ruby(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()

        self.sprite = 0
        self.load_images()
        self.rect = self.image.get_rect()

        self.rect.bottomleft = (x, y)

        self.HOR_VEL = 2
        self.VER_ACC = 0.5
        self.direction = random.choice([-1, 1])
        self.ver_velocity = 0

    def load_images(self):
        self.spin_right = []
        self.spin_left = []

        for i in range(0, 7):
            self.spin_right.append(pygame.transform.scale(pygame.image.load(f"../assets/images/ruby/tile00{i}.png"), (48, 48)))
            self.spin_left.append(pygame.transform.flip(self.spin_right[i], True, False))

        if self.direction > 0:
            self.image = self.spin_right[0]
        else:
            self.image = self.spin_left[0]

    def update(self, tile_group):
        self.mask = pygame.mask.from_surface(self.image)

        self.move()
        self.stay_on_platform(tile_group)

    def move(self):
        self.acceleration = self.VER_ACC

        self.rect.x += self.HOR_VEL*self.direction

        if self.direction > 0:
            self.animate(self.spin_right)
        else:
            self.animate(self.spin_left)

        if self.rect.x+CAR_SIZE[0]-10 < 0 and self.rect.y < 630 and self.rect.y > 100:
            self.rect.x = WINDOW_WIDTH
        elif self.rect.x > WINDOW_WIDTH and self.rect.y < 630 and self.rect.y > 100:
            self.rect.x = -(CAR_SIZE[0]-10)

    def stay_on_platform(self, tile_group):
        collided_platforms = pygame.sprite.spritecollide(self, tile_group, False, pygame.sprite.collide_mask)

        if collided_platforms and self.ver_velocity > 0:
            self.rect.y = collided_platforms[0].rect.top+5
            self.ver_velocity = 0

    def animate(self, sprites):
        if self.sprite < len(sprites)-1:
            self.sprite += 0.2
        else:
            self.sprite = 0

        self.image = sprites[int(self.sprite)]

