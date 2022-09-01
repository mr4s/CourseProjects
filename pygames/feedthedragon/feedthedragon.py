# To Do: 
#      - music
#      - sound effects
#      - show lives and score

import pygame, random

WINDOW_WIDTH  = 600
WINDOW_HEIGHT = 300
WHITE         = (255, 255, 255)
GREEN         = (0, 255, 0)
BLACK         = (0, 0, 0)
RED           = (255, 0, 0)

FPS = 60
clock = pygame.time.Clock()

VELOCITY = 5

to_blit = {}
screen        = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))

def setup():
    pygame.init()

    pygame.display.set_caption("Feed The Dragon")

    font          = pygame.font.Font('assets/AttackGraffiti.ttf', 26)

    title_txt     = font.render("Feed The Dragon!!", True, GREEN, WHITE)
    title_pos     = title_txt.get_rect()
    title_pos.center = (WINDOW_WIDTH//2, 18)

    font          = pygame.font.Font('assets/AttackGraffiti.ttf', 22)

    lives_txt = font.render("Lives: ", True, GREEN)
    lives_pos = lives_txt.get_rect()
    lives_pos.topright = (WINDOW_WIDTH-20, 5)

    score_txt = font.render("Score: ", True, GREEN)
    score_pos = score_txt.get_rect()
    score_pos.topleft = (0, 5)

    to_blit[title_txt] = title_pos
    to_blit[lives_txt] = lives_pos
    to_blit[score_txt] = score_pos

    set_sound()

    display_numbers()
    bliting()

def set_sound():
    pygame.mixer.music.load("assets/ftd_background_music.wav")
    pygame.mixer.music.play(-1)

def display_numbers(lives=5, score=0):
    font          = pygame.font.Font('assets/AttackGraffiti.ttf', 22)

    lives_txt = font.render(f"{lives}", True, GREEN)
    nolives_pos = lives_txt.get_rect()
    nolives_pos.topright = (WINDOW_WIDTH-8, 5)

    score_txt = font.render(f"{score}", True, GREEN)
    noscore_pos = score_txt.get_rect()
    noscore_pos.topleft = (80, 5)

    screen.fill(BLACK)
    screen.blit(lives_txt, nolives_pos)
    screen.blit(score_txt, noscore_pos)
    

def load_img(imgs):
    dragon = pygame.image.load("assets/dragon_right.png")
    coin   = pygame.image.load("assets/coin.png")

    dragon_pos = dragon.get_rect()
    coin_pos   = coin.get_rect()

    dragon_pos.center = (55, (WINDOW_HEIGHT-40)//2)
    coin_pos.topleft  = (WINDOW_WIDTH, random.randint(42, WINDOW_HEIGHT-32))

    to_blit[dragon] = dragon_pos
    to_blit[coin]   = coin_pos

    imgs["dragon"] = dragon_pos
    imgs["coin"] = coin_pos

def bliting():
    for b in to_blit.keys():
        screen.blit(b, to_blit[b])

    pygame.draw.line(screen, WHITE, (0, 40), (WINDOW_WIDTH, 40))

def game_loop(imgs, score, lives):
    run = True

    coin_sound = pygame.mixer.Sound("assets/coin_sound.wav")
    miss_sound = pygame.mixer.Sound("assets/miss_sound.wav")
    miss_sound.set_volume(.1)

    while run:
        
        if(lives > 0):
            keys = pygame.key.get_pressed()

            if keys[pygame.K_UP] and imgs["dragon"].top > 40:
                imgs["dragon"].y -= VELOCITY
            elif keys[pygame.K_DOWN] and imgs["dragon"].bottom < WINDOW_HEIGHT:
                imgs["dragon"].y += VELOCITY
    
            if imgs["dragon"].colliderect(imgs["coin"]):
                score += 1
                imgs["coin"].topleft = (WINDOW_WIDTH, random.randint(42, WINDOW_HEIGHT-32))
                if lives > 0: coin_sound.play()
            # pygame.time.delay(2000)

            elif imgs["coin"].right <= 0:
                lives -= 1
                imgs["coin"].topleft = (WINDOW_WIDTH, random.randint(42, WINDOW_HEIGHT-32))
                if lives > 0: miss_sound.play()
            # pygame.time.delay(2000)

            imgs["coin"].x -= VELOCITY*1.5

        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                run = False
            elif lives <= 0 and event.type == pygame.KEYDOWN:
                lives = 5
                score = 0

        display_numbers(lives, score)
        bliting()

        if lives == 0:
            lose_game()
            lives -= 1
        elif lives > 0:
            pygame.display.update()

        clock.tick(FPS)

    pygame.quit()

def lose_game():
    font = pygame.font.SysFont("calibri", 34, True)
    lose_txt = font.render("You lose! :(", True, RED, WHITE)
    lose_pos = lose_txt.get_rect()
    lose_pos.center = (WINDOW_WIDTH//2, WINDOW_HEIGHT//2)
    screen.blit(lose_txt, lose_pos)
    pygame.display.update()

if __name__ == '__main__':
    imgs = {}
    score = 0
    lives = 5

    setup()
    load_img(imgs)
    game_loop(imgs, score, lives)
