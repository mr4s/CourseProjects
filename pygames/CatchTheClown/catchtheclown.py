import pygame, random as rd

pygame.init()

WINDOW_WIDTH  = 945 
WINDOW_HEIGHT = 600

BLACK = (0,0,0)
WHITE = (255, 255, 255)
BLUE = (1, 175, 209)
YELLOW = (248, 231, 28)

display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Catch the Clown!!!")

click_sound = pygame.mixer.Sound("assets/click_sound.wav")
miss_sound  = pygame.mixer.Sound("assets/miss_sound.wav")
pygame.mixer.music.load("assets/ctc_background_music.wav")
pygame.mixer.music.play(-1)

click_sound.set_volume(0.3)
miss_sound.set_volume(0.3)

font = pygame.font.Font("assets/Franxurter.ttf", 23)

score_txt = font.render("SCORE: ", True, YELLOW)
lives_txt = font.render("LIVES: ", True, YELLOW)
name_txt  = font.render("CATCH THE CLOWN", True, BLUE)
gameover_txt = font.render("GAME OVER!", True, BLUE, YELLOW)
continue_txt = font.render("To play again, click anywhere", True, YELLOW, BLUE)

score_rect = score_txt.get_rect()
lives_rect = lives_txt.get_rect()
name_rect  = name_txt.get_rect()
gameover_rect = gameover_txt.get_rect()
continue_rect = continue_txt.get_rect()

name_rect.topleft = (40, 8)
score_rect.topleft = (WINDOW_WIDTH - 140, 8)
lives_rect.topright= (score_rect.right, 33)
gameover_rect.center = (WINDOW_WIDTH//2, 250)
continue_rect.center = (WINDOW_WIDTH//2, 300)

#Set FPS and clock
FPS   = 60
clock = pygame.time.Clock()

STARTING_VELOCITY = 4
VELOCITY = 5
ACCELERATION = .1

lives = STARTING_LIVES = 5
score = STARTING_SCORE = 0

bg_img = pygame.image.load("assets/background.png")
bg_rect = bg_img.get_rect()
bg_rect.center = (WINDOW_WIDTH//2, WINDOW_HEIGHT//2)

clown = pygame.image.load("assets/clown.png") 
clown_rect = clown.get_rect() 
clown_rect.center = (WINDOW_WIDTH//2, WINDOW_HEIGHT//2) 
clown_dx = rd.choice([-1, 1])
clown_dy = rd.choice([-1, 1])

running = True 
while running: 
    for event in pygame.event.get(): 
        if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE): 
            running = False 
            break 
   
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if lives == 0:
                lives = STARTING_LIVES
                score = STARTING_SCORE
                VELOCITY = STARTING_VELOCITY
                pygame.mixer.music.play(-1, 0.0)
            elif clown_rect.collidepoint(event.pos):
                score += 1
                VELOCITY *= (ACCELERATION+1)
                click_sound.play()
                clown_dy = rd.choice([-1, 1])
                clown_dx = rd.choice([-1, 1])
            else:
                lives -= 1
                miss_sound.play()

    score_txt = font.render(f"SCORE: {score}", True, YELLOW)
    lives_txt = font.render(f"LIVES: {lives}", True, YELLOW)

    if lives == 0:
        display_surface.blit(gameover_txt, gameover_rect)
        display_surface.blit(continue_txt, continue_rect)
        pygame.mixer.music.stop()
    else:
        #Move clown
        if not(clown_rect.right < WINDOW_WIDTH and clown_rect.left > 0):
            clown_dx = -clown_dx
        if not(clown_rect.top > 0 and clown_rect.bottom < WINDOW_HEIGHT):
            clown_dy = -clown_dy

        clown_rect.x += clown_dx*VELOCITY
        clown_rect.y += clown_dy*VELOCITY

        display_surface.blit(bg_img, bg_rect)

        display_surface.blit(name_txt, name_rect)
        display_surface.blit(score_txt, score_rect)
        display_surface.blit(lives_txt, lives_rect)
        display_surface.blit(clown, clown_rect)
    
    pygame.display.update()

    #Tick the clock
    clock.tick(FPS)


pygame.quit()
