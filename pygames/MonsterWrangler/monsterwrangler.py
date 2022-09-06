import pygame, random

#Macros
WINDOW_HEIGHT = 600
WINDOW_WIDTH  = 1200

INNER_TOP = 85
INNER_BOTTOM  = WINDOW_HEIGHT-85

STARTING_LIVES = 5
STARTING_WARPS = 3

YELLOW = (243, 157, 20)
PURPLE = (226, 73, 243)
GREEN = (87, 201, 47)
BLUE = (28, 176, 235)

FPS = 90
clock = pygame.time.Clock()

#Classes
class Game():
    def __init__(self):
        self.frame = 0

        self.score = 0
        self.lives = STARTING_LIVES
        self.cur_round = 1
        self.time = 0
        self.warps = STARTING_WARPS

        self.monster_group = pygame.sprite.Group()

        self.txt = {
                    "middle": Text("Current Catch", WINDOW_WIDTH//2, 5, "c"),
                    "score": Text("Score: 0", 5, 5, "l"),
                    "lives": Text(f"Lives: {STARTING_LIVES}", 5, 30, "l"),
                    "round": Text("Current Round: 1", 5, 55, "l"),
                    "time": Text("Round Time: 0", WINDOW_WIDTH-15, 5, "r"),
                    "warps": Text(f"Warps: {STARTING_WARPS}", WINDOW_WIDTH-15, 30, "r"),
                    "lose": Text("Final Score: 0", WINDOW_WIDTH//2, 150, "c"),
                    "pause": Text("Game paused", WINDOW_WIDTH//2, 150),
                    "continue": Text("Press (r) to reset game or any other key to continue", WINDOW_WIDTH//2, 250),
                    "again": Text("Press any key to play again", WINDOW_WIDTH//2, 250)
                   }

        self.monster_group.add(Monster("blue"))
        self.monster_group.add(Monster("purple"))
        self.monster_group.add(Monster("green"))
        self.monster_group.add(Monster("yellow"))

        self.new_target()

        self.pause = False
        self.lost = False

        # pygame.mixer.music.load("assets/die.wav")
        self.die_sound = pygame.mixer.Sound("assets/die.wav")
        self.catch_sound = pygame.mixer.Sound("assets/catch.wav")
        self.level_sound = pygame.mixer.Sound("assets/next_level.wav")

        self.level_sound.set_volume(0.2)
        self.catch_sound.set_volume(0.2)
        self.die_sound.set_volume(0.2)

    def update(self, knight, screen):
        self.frame += 1
        if self.frame == FPS:
            self.time += 1
            self.frame = 0

        self.check_collisions(knight, screen)
        self.monster_group.update()

        if len(self.monster_group.sprites()) == 0:
            self.new_round(knight)


    def check_collisions(self, knight, screen):
        monster = pygame.sprite.spritecollideany(knight, self.monster_group)
        
        if monster:
            if monster.color == self.target.color:
                monster.remove(self.monster_group)

                self.new_target()
                self.score += 100*self.cur_round
                self.catch_sound.play()

            else:
                self.lives -= 1
                self.die_sound.play()
                knight.reset()

        if self.lives <= 0:
            self.lose(screen)

    def lose(self, screen):
        self.lost = True
        self.txt["lose"].update(screen, f"Final Score: {self.score}")
        self.txt["again"].update(screen)

    def new_round(self, knight):
        self.level_sound.play()

        self.cur_round += 1
        self.time = 0
        self.lives += 1

        number_monsters = self.cur_round*4

        for i in range(number_monsters):
            self.monster_group.add(Monster(random.choice(["blue", "purple", "green", "yellow"])))

        knight.warps = STARTING_WARPS
        knight.reset()

    def new_target(self):
        if len(self.monster_group.sprites()):
            self.target = random.choice(self.monster_group.sprites())

    def pause_game(self, screen):
        self.pause = True
        self.txt["pause"].update(screen)
        self.txt["continue"].update(screen)

        pygame.display.update()

    def unpause_game(self):
        self.pause = False

    def reset_game(self, knight):
        self.lost = False
        self.__init__()
        knight.__init__()

    def draw(self, screen, warps):
        size = 24
        color = self.target.color

        self.txt["middle"].update(screen)
        self.txt["score"].update(screen, f"Score: {self.score}")
        self.txt["lives"].update(screen, f"Lives: {self.lives}")
        self.txt["round"].update(screen, f"Current Round: {self.cur_round}")
        self.txt["time"].update(screen, f"Round Time: {self.time}")
        self.txt["warps"].update(screen, f"Warps: {warps}")

        screen.blit(self.target.image, (self.txt["middle"].rect.centerx-25, (INNER_TOP-self.txt["middle"].rect.bottom)/2-3))

        pygame.draw.line(screen, color, (0, INNER_TOP), (WINDOW_WIDTH, INNER_TOP), 3)
        pygame.draw.line(screen, color, (0, INNER_BOTTOM), (WINDOW_WIDTH, INNER_BOTTOM), 3)
        pygame.draw.line(screen, color, (0, INNER_TOP), (0, INNER_BOTTOM), 3)
        pygame.draw.line(screen, color, (WINDOW_WIDTH, INNER_TOP), (WINDOW_WIDTH, INNER_BOTTOM), 3)

        pygame.draw.line(screen, color, (WINDOW_WIDTH//2-size, self.txt["middle"].rect.bottom), (WINDOW_WIDTH//2+size, self.txt["middle"].rect.bottom), 1)
        pygame.draw.line(screen, color, (WINDOW_WIDTH//2-size, self.txt["round"].rect.bottom), (WINDOW_WIDTH//2+size, self.txt["round"].rect.bottom), 1)
        pygame.draw.line(screen, color, (WINDOW_WIDTH//2-size, self.txt["middle"].rect.bottom), (WINDOW_WIDTH//2-size, self.txt["round"].rect.bottom), 1)
        pygame.draw.line(screen, color, (WINDOW_WIDTH//2+size, self.txt["middle"].rect.bottom), (WINDOW_WIDTH//2+size, self.txt["round"].rect.bottom), 1)

        self.monster_group.draw(screen)

class Monster(pygame.sprite.Sprite):
    def __init__(self, color = "blue"):
        super().__init__()

        self.velocity = random.randint(1, 5)

        self.image = pygame.image.load(f"assets/{color}_monster.png")

        if color == "yellow":
            self.color = YELLOW
        elif color == "purple":
            self.color = PURPLE
        elif color == "green":
            self.color = GREEN
        else:
            self.color = BLUE

        self.rect = self.image.get_rect()
        self.rect.center = (random.randint(20, WINDOW_WIDTH-20), random.randint(INNER_TOP+20, INNER_BOTTOM-20))
        self.image = pygame.transform.scale(self.image, (self.rect.size[0]*0.8, self.rect.size[1]*0.8))

        self.dx = random.choice([-1, 1])
        self.dy = random.choice([-1, 1])

    def update(self):
        if self.dx < 0 and self.rect.left <= 0:
            self.dx *= -1
        if self.dx > 0 and self.rect.right >= WINDOW_WIDTH:
            self.dx *= -1
        if self.dy < 0 and self.rect.top <= INNER_TOP:
            self.dy *= -1
        if self.dy > 0 and self.rect.bottom >= INNER_BOTTOM:
            self.dy *= -1

        self.rect.y += self.dy*self.velocity
        self.rect.x += self.dx*self.velocity

class Knight(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("assets/knight.png")
        self.rect = self.image.get_rect()
        self.rect.centerx = WINDOW_WIDTH//2
        self.rect.bottom  = WINDOW_HEIGHT
        self.image = pygame.transform.scale(self.image, (self.rect.size[0]*0.8, self.rect.size[1]*0.8))

        self.velocity = 4

        self.top = 0
        self.bottom = WINDOW_HEIGHT

        self.warps = STARTING_WARPS

        self.warp_sound = pygame.mixer.Sound("assets/warp.wav")
        self.warp_sound.set_volume(0.2)

    def update(self):
        if self.rect.top < INNER_BOTTOM:
            self.top = INNER_TOP
            self.bottom = INNER_BOTTOM

        key = pygame.key.get_pressed()

        if key[pygame.K_UP] and self.rect.top > self.top:
            self.rect.y -= self.velocity
        elif key[pygame.K_DOWN] and self.rect.bottom < self.bottom+10:
            self.rect.y += self.velocity
        elif key[pygame.K_LEFT] and self.rect.left > 0:
            self.rect.x -= self.velocity
        elif key[pygame.K_RIGHT] and self.rect.right < WINDOW_WIDTH+10:
            self.rect.x += self.velocity

    def reset(self):
        self.rect.centerx = WINDOW_WIDTH//2
        self.rect.bottom = WINDOW_HEIGHT

    def warp(self):
        self.warps -= 1
        self.warp_sound.play()
        self.reset()

class Text():
    def __init__(self, txt, x, y, pos="c"):
        self.font = pygame.font.Font("assets/Abrushow.ttf", 22)
        
        self.txt = self.font.render(txt, True, (255, 255, 255)) 
        self.rect = self.txt.get_rect()
        
        if pos == "l":
            self.rect.topleft = (x, y)
        elif pos == "r":
            self.rect.topright = (x, y)
        else:
            self.rect.top = y
            self.rect.centerx = x

    def update(self, screen, txt=""):
        if txt:
            self.txt = self.font.render(txt, True, (255, 255, 255)) 
        screen.blit(self.txt, self.rect) 


#Main
if __name__ == "__main__":
    pygame.init()

    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))

    game = Game()

    knight = Knight()
    knight_group = pygame.sprite.Group()
    knight_group.add(knight)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                running = False
            elif game.lost and event.type == pygame.KEYDOWN:
                game.reset_game(knight)
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE and knight.warps > 0:
                knight.warp()
            elif event.type == pygame.KEYDOWN and pygame.key.name(event.key) == "p" and game.pause == True:
                game.unpause_game()
            elif event.type == pygame.KEYDOWN and pygame.key.name(event.key) == "p":
                game.pause_game(screen)
            elif event.type == pygame.KEYDOWN and pygame.key.name(event.key) == "r":
                game.reset_game(knight)

        if game.pause == False and game.lost == False:
            screen.fill((0, 0, 0))

            knight_group.update()
            knight_group.draw(screen)

            game.update(knight, screen)
            game.draw(screen, knight.warps)

            pygame.display.update()

        clock.tick(FPS)    

    pygame.quit()
