import pygame, random
from setup import *

Vector = pygame.math.Vector2

class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()

        self.sprite = 0

        self.load_images()

        self.rect = self.image.get_rect()
        self.rect.center = (x*32, y*32+5)

        self.position = Vector(x, y)
        self.velocity = Vector(0, 0)
        self.acceleration = Vector(0, 0)

        self.STARTING_POSITION = self.position

        self.HOR_ACC = 1.4
        self.HOR_FRICTION = 0.15

        self.VER_ACC = 0.5
        self.VER_SPEED = 12 #jump

        self.load_images()
        self.slash_group = pygame.sprite.Group()

        self.score = 0
        self.health = STARTING_HEALTH

    def update(self, tile_group, portal_group, zombie_group, attack=False):
        #mask
        self.mask = pygame.mask.from_surface(self.image)

        self.move(tile_group, portal_group)
        self.stay_on_platform(tile_group)

        if attack:
            self.attack()
        self.get_attacked(zombie_group)
        self.slash_group.update()
        self.slash_group.draw(display_surface)

    def load_images(self):
        #idle 
        self.idle_right = []
        for i in range(1, 11):
            self.idle_right.append(pygame.transform.scale(pygame.image.load(f"../assets/images/player/idle/Idle ({i}).png"), CAR_SIZE))

        self.idle_left = []
        for i in range(10):
            self.idle_left.append(pygame.transform.flip(self.idle_right[i], True, False))

        #jump
        self.jump_right = []
        for i in range(1, 11):
            self.jump_right.append(pygame.transform.scale(pygame.image.load(f"../assets/images/player/jump/Jump ({i}).png"), CAR_SIZE))

        self.jump_left = []
        for i in range(10):
            self.jump_left.append(pygame.transform.flip(self.jump_right[i], True, False))

        #run
        self.run_right = []
        for i in range(1, 11):
            self.run_right.append(pygame.transform.scale(pygame.image.load(f"../assets/images/player/run/Run ({i}).png"), CAR_SIZE))

        self.run_left = []
        for i in range(10):
            self.run_left.append(pygame.transform.flip(self.run_right[i], True, False))

        #attack
        self.attack_right = []
        for i in range(1, 11):
            self.attack_right.append(pygame.transform.scale(pygame.image.load(f"../assets/images/player/attack/Attack ({i}).png"), CAR_SIZE))

        self.attack_left = []
        for i in range(10):
            self.attack_left.append(pygame.transform.flip(self.attack_right[i], True, False))

        self.image = self.idle_right[0]

    def move(self, tile_group, portal_group):
        self.acceleration = Vector(0, self.VER_ACC)
        # portal = self.go_through_portal(portal_group)

        key = pygame.key.get_pressed()

        if key[pygame.K_UP]:
            self.jump(tile_group, key)
        elif key[pygame.K_LEFT]:
            self.acceleration.x = -self.HOR_ACC
            self.animate(self.run_left, 0.2)
        elif key[pygame.K_RIGHT]:
            self.acceleration.x = self.HOR_ACC
            self.animate(self.run_right, 0.2)
        else:
            if self.velocity.x >= 0:
                self.animate(self.idle_right, 0.2)
            else:
                self.animate(self.idle_left, 0.2)

        self.acceleration.x -= self.velocity.x*self.HOR_FRICTION
        self.velocity += self.acceleration
        self.position += self.velocity + 0.5*self.acceleration

        if self.position.x+CAR_SIZE[0]-10 < 0 and self.position.y < 630 and self.position.y > 100:
            self.position.x = WINDOW_WIDTH
        elif self.position.x > WINDOW_WIDTH and self.position.y < 630 and self.position.y > 100:
            self.position.x = -(CAR_SIZE[0]-10)

        self.rect.bottomleft = self.position

    def stay_on_platform(self, tile_group):
        collided_platforms = pygame.sprite.spritecollide(self, tile_group, False, pygame.sprite.collide_mask)

        if collided_platforms and self.velocity.y > 0:
            self.position.y = collided_platforms[0].rect.top+5
            self.velocity.y = 0
        elif self.velocity.y:
            if self.velocity.x >= 0:
                self.animate(self.jump_right, 0.2)
            else:
                self.animate(self.jump_left, 0.2)

    def jump(self, tile_group, key):
        if pygame.sprite.spritecollide(self, tile_group, False):
            self.velocity.y  = -self.VER_SPEED
        if key[pygame.K_LEFT]:
            self.acceleration.x = -self.HOR_ACC
        elif key[pygame.K_RIGHT]:
            self.acceleration.x = self.HOR_ACC

    def animate(self, sprites, speed):
        if self.sprite < len(sprites)-1:
            self.sprite += speed
        else:
            self.sprite = 0

        self.image = sprites[int(self.sprite)]

    def attack(self):
        slash = Slash(self.rect.right, self.rect.centery)
        self.slash_group.add(slash)
        if self.velocity.x >= 0:
            slash.throw(self.rect.right, self.rect.centery)
            self.animate(self.attack_right, 0.9)
        else:
            slash.throw(self.rect.left, self.rect.centery, "left")
            self.animate(self.attack_left, 0.9)

    def get_attacked(self, zombie_group):
        if pygame.sprite.spritecollide(self, zombie_group, False, pygame.sprite.collide_mask):
            self.position = Vector(random.randint(70, WINDOW_WIDTH-70), 80)

            if self.health > 0:
                self.health -= 10

    def restart_position(self):
        self.position = self.STARTING_POSITION
        self.rect.center = self.position

    def lose(self):
        pass

class Slash(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()

        self.image = pygame.transform.scale(pygame.image.load("../assets/images/player/slash.png"), (32, 32))
        self.rect  = self.image.get_rect()

        self.mask = pygame.mask.from_surface(self.image)

        self.velocity = 5
        self.direction = 1
        self.shoot = False

    def update(self):
        if self.shoot:
            self.rect.x += self.velocity*self.direction
            if self.rect.left >= WINDOW_WIDTH or self.rect.right <= 0:
                self.shoot = False

    def throw(self, x, y, direction="right"):
        self.shoot = True
        self.rect.bottomleft = (x, y+12)

        if direction == "right":
            self.direction = 1
        else:
            self.image = pygame.transform.flip(self.image, True, False)
            self.direction = -1

