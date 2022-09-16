import pygame
import random

WINDOW_HEIGHT = 700
WINDOW_WIDTH = 1000

INNER_BOTTOM = WINDOW_HEIGHT-85
INNER_TOP = 35

WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

STARTING_LIVES = 5
STARTING_ALIEN_VELOCITY = 2

FPS = 60
clock = pygame.time.Clock()

screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))


class Game:
    def __init__(self):
        pygame.init()

        pygame.display.set_caption("Space Invaders")

        self.pause = False
        self.lost  = False

        self.round = 1
        self.score = 0
        self.time  = 0

        self.player = Player()

        aliens = [Alien(60*i, 60*j+30, i, j) for i in range(1, 12) for j in range(1, 6)]

        self.aliens = pygame.sprite.Group()
        for alien in aliens:
            self.aliens.add(alien)

        self.alien_shots = pygame.sprite.Group()

        self.txt = {
            "this_round": Text(f"Round : {self.round}", 80, 20),
            "new_round": Text(f"Space Invaders Round {self.round}", WINDOW_WIDTH//2, WINDOW_HEIGHT//2-55),
            "begin": Text("Press 'ENTER' to Begin", WINDOW_WIDTH//2, WINDOW_HEIGHT//2+50),
            "score": Text(f"Score: {self.score}", WINDOW_WIDTH//2, 20),
            "lives": Text(f"Lives: {self.player.lives}", WINDOW_WIDTH-60, 20),
            "hit": Text("You've been hit!", WINDOW_WIDTH//2, WINDOW_HEIGHT//2-55),
            "continue": Text("Press 'ENTER' to Continue", WINDOW_WIDTH//2, WINDOW_HEIGHT//2),
            "lose": Text(f"Final Score: {self.score}", WINDOW_WIDTH//2, WINDOW_HEIGHT//2-55),
            "again": Text("Press 'ENTER' To Play Again", WINDOW_WIDTH//2, WINDOW_HEIGHT//2)
        }

        self.new_round_sound = pygame.mixer.Sound("assets/new_round.wav")
        self.alien_fire_sound = pygame.mixer.Sound("assets/alien_fire.wav")
        self.alien_hit_sound = pygame.mixer.Sound("assets/alien_hit.wav")
        self.player_hit_sound = pygame.mixer.Sound("assets/player_hit.wav")

        self.player_hit_sound.set_volume(.1)
        self.new_round_sound.set_volume(.1)
        self.alien_hit_sound.set_volume(.1)
        self.alien_fire_sound.set_volume(.1)

    def update(self):
        if not self.pause:
            screen.fill((0, 0, 0))

            self.time += 1
            self.player.update()
            self.aliens.update(self.round)

            alien = pygame.sprite.spritecollideany(self.player.shot, self.aliens)

            if alien:
                self.alien_hit_sound.play()
                self.aliens.remove(alien)
                self.player.shot.hit()
                self.score += 1

            if len(self.aliens.sprites()) < 1:
                self.new_round()

            alien = random.choice(self.aliens.sprites())
            if self.time == 2*FPS//self.round:
                self.alien_fire_sound.play()
                alien.shoot()
                self.time = 0

                self.alien_shots.add(alien.shot)

            player_hit = pygame.sprite.spritecollide(self.player, self.alien_shots, True)
            if len(player_hit) > 0:
                self.player_hit()

            for s in self.alien_shots:
                s.update()

            for alien in self.aliens:
                if alien.rect.bottom >= WINDOW_HEIGHT-85:
                    self.lose()

            if self.player.lives <= 0:
                self.lose()

            pygame.draw.line(screen, WHITE, (0, WINDOW_HEIGHT-85), (WINDOW_WIDTH, WINDOW_HEIGHT-85), 2)
            pygame.draw.line(screen, WHITE, (0, 35), (WINDOW_WIDTH, 35), 2)

            self.txt["this_round"].update(f"Round:{self.round}")
            self.txt["score"].update(f"Score:{self.score}")
            self.txt["lives"].update(f"Lives:{self.player.lives}")

    def new_round(self):
        self.new_round_sound.play()

        screen.fill((0, 0, 0))

        self.round += 1

        for alien in self.aliens:
            alien.reset(self.round)

        self.txt["new_round"].update(f"Space Invaders Round {self.round}")
        self.txt["continue"].update()

        aliens = [Alien(60*i, 60*j+30, i, j) for i in range(1, 12) for j in range(1, 6)]

        self.aliens = []

        self.aliens = pygame.sprite.Group()
        for alien in aliens:
            self.aliens.add(alien)

        self.alien_shots = pygame.sprite.Group()

        self.pause = True

    def lose(self):
        screen.fill((0, 0, 0))

        self.txt["lose"].update(f"Final Score: {self.score}")
        self.txt["again"].update()

        self.pause = True
        self.lost  = True


    def player_hit(self):
        self.player_hit_sound.play()

        screen.fill((0, 0, 0))

        self.player.get_hit()
        self.pause = True

        self.txt["hit"].update()
        self.txt["continue"].update()


class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()

        self.image = pygame.image.load("assets/player_ship.png")
        self.rect = self.image.get_rect()
        self.rect.centerx = WINDOW_WIDTH//2
        self.rect.bottom = WINDOW_HEIGHT-5

        self.lives = STARTING_LIVES

        self.velocity = 4

        self.shot = Player_Shot()

        self.player_fire_sound = pygame.mixer.Sound("assets/player_fire.wav")
        self.player_fire_sound.set_volume(0.1)

        screen.blit(self.image, self.rect)

    def update(self):
        key = pygame.key.get_pressed()

        if key[pygame.K_LEFT] and self.rect.left > 0:
            self.rect.x -= self.velocity
        elif key[pygame.K_RIGHT] and self.rect.right < WINDOW_WIDTH:
            self.rect.x += self.velocity
        elif key[pygame.K_SPACE] and self.shot.trigger == False:
            self.player_fire_sound.play()
            self.shoot()

        self.shot.update()

        screen.blit(self.image, self.rect)

    def shoot(self):
        self.shot.shoot(self.rect.top, self.rect.centerx)

    def get_hit(self):
        self.lives -= 1

class Player_Shot(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()

        self.image = pygame.image.load("assets/green_laser.png")
        self.rect   = self.image.get_rect()

        self.velocity = 5

        self.trigger = False

    def update(self): 
        if self.rect.y <= 35:
            self.trigger = False

        if self.trigger:
            self.rect.y -= self.velocity

            screen.blit(self.image, self.rect)

        else:
            self.rect.y = WINDOW_HEIGHT

    def shoot(self, bottom, centerx):
        self.rect.bottom = bottom
        self.rect.centerx = centerx

        self.trigger = True

    def hit(self):
        self.trigger = False

class Alien(pygame.sprite.Sprite):
    right = WINDOW_WIDTH
    bottom = WINDOW_HEIGHT

    def __init__(self, x, y, column, line):
        super().__init__()

        self.image = pygame.image.load("assets/alien.png")
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.starting_pos = (x, y)
        self.column = column
        self.line = line

        self.velocity = STARTING_ALIEN_VELOCITY

        self.shot = Alien_Shot()

        self.dx = 1

    def update(self, cur_round):
        if self.rect.centerx <= WINDOW_WIDTH-60*(12-self.column) and self.rect.centerx >= 60*(self.column):
            self.rect.x += self.velocity*self.dx
        else:
            self.rect.y += 10
            self.dx *= -1

            self.rect.x += self.velocity*self.dx

        screen.blit(self.image, self.rect)

    def reset(self, cur_round):
        self.rect.center = self.starting_pos

        self.velocity = STARTING_ALIEN_VELOCITY+cur_round

        self.shot = Alien_Shot()

        self.dx = 1

    def shoot(self):
        self.shot.shoot(self.rect.bottom, self.rect.centerx)

class Alien_Shot(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()

        self.image = pygame.image.load("assets/red_laser.png")
        self.rect   = self.image.get_rect()

        self.velocity = 5

        self.trigger = False

    def update(self): 
        if self.trigger:
            self.rect.y += self.velocity

            screen.blit(self.image, self.rect)

        else:
            self.rect.y = 0

    def shoot(self, top, centerx):
        self.rect.top = top
        self.rect.centerx = centerx

        self.trigger = True

    def hit(self):
        self.trigger = False

class Text:
    def __init__(self, txt, x, y):
        self.font = pygame.font.Font("assets/Facon.ttf", 24)

        self.txt = self.font.render(txt, True, WHITE)
        self.rect = self.txt.get_rect()
        self.rect.center = (x, y)

        screen.blit(self.txt, self.rect)

    def update(self, txt=""):
        if txt:
            self.txt = self.font.render(txt, True, WHITE)

        screen.blit(self.txt, self.rect)


if __name__ == "__main__":
    game = Game()

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                running = False
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN and game.lost:
                game.__init__()
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN and game.pause:
                game.pause = False

        game.update()
        pygame.display.update()

        clock.tick(FPS)

    pygame.quit()
