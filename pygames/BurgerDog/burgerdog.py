import pygame, random

pygame.init()

WINDOW_WIDTH  = 500
WINDOW_HEIGHT = 300
ORANGE = (246, 170, 54)
WHITE = (255, 255, 255)

display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Burger Dog")

pygame.mixer.music.load("assets/bd_background_music.wav")
bark = pygame.mixer.Sound("assets/bark_sound.wav")
miss = pygame.mixer.Sound("assets/miss_sound.wav")

#Set FPS and clock
FPS   = 60
clock = pygame.time.Clock()

VELOCITY = 5
burger_vel = STARTING_BURGER_VEL = 3
BOOST = 2.5

dog_left = pygame.image.load("assets/dog_left.png")
dog_left_rect = dog_left.get_rect()

dog_right = pygame.image.load("assets/dog_right.png")
dog_right_rect = dog_right.get_rect()

burger = pygame.image.load("assets/burger.png")
burger_img_rect = burger.get_rect()

burger = pygame.transform.scale(burger, (burger_img_rect.size[0]*0.7, burger_img_rect.size[1]*0.7))
dog_left = pygame.transform.scale(dog_left, (dog_left_rect.size[0]*0.6, dog_left_rect.size[1]*0.6))
dog_right = pygame.transform.scale(dog_right, (dog_right_rect.size[0]*0.6, dog_right_rect.size[1]*0.6))

dog = dog_left
dog_rect = dog_left_rect
dog_rect.center = (WINDOW_WIDTH//2, WINDOW_HEIGHT-80)

lives = STARTING_LIVES = 3
score = STARTING_SCORE = 0
burgers_eaten = STARTING_BURGERS = 0
boost = STARTING_BOOST = 100
points = random.randint(100, 1500)

font = pygame.font.Font("assets/WashYourHand.ttf", 20)

#Text
name_txt = font.render("Burger Dog", True, ORANGE)
lives_txt = font.render(f"Lives: {lives}", True, ORANGE)
score_txt = font.render(f"Score: {score}", True, ORANGE)
burgers_txt = font.render(f"Burgers Eaten: {burgers_eaten}", True, ORANGE)
boost_txt = font.render(f"Boost: {boost}", True, ORANGE)
points_txt = font.render(f"Burger Points: {points}", True, ORANGE)
lose_txt = font.render(f"FINAL SCORE: {score}", True, ORANGE)
continue_txt = font.render("Press any key to play again", True, ORANGE)

name_rect = name_txt.get_rect()
lives_rect = lives_txt.get_rect()
score_rect = score_txt.get_rect()
burgers_rect = burgers_txt.get_rect()
boost_rect = boost_txt.get_rect()
points_rect = points_txt.get_rect()
lose_rect = lose_txt.get_rect()
continue_rect = continue_txt.get_rect()

name_rect.center = (WINDOW_WIDTH//2, 10)
lives_rect.topright = (WINDOW_WIDTH - 40, 3)
burgers_rect.center = (WINDOW_WIDTH//2, name_rect.centery+25)
boost_rect.topleft = lives_rect.bottomleft 
points_rect.topleft = (5, 3)
score_rect.topleft = points_rect.bottomleft
burger_img_rect.center = (random.randint(30, WINDOW_WIDTH-30), burgers_rect.bottom+25)
lose_rect.center = (WINDOW_WIDTH//2, WINDOW_HEIGHT//2 - 20)
continue_rect.center = (lose_rect.centerx, lose_rect.centery+60)

running = True
pygame.mixer.music.play(-1)
while running:
    display_surface.fill((0,0,0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
            running = False
            break

        elif lives <= 0 and (event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN):
            lives = STARTING_LIVES
            score = 0
            burgers_eaten = 0
            boost = STARTING_BOOST
            pygame.mixer.music.play(-1, 0.0)

    if lives > 0:
        burger_img_rect.y += burger_vel

        points = random.randint(100, 1500)

        if dog_rect.colliderect(burger_img_rect):
            bark.play()
            score += points
            burger_vel += 0.1
            burger_img_rect.center = (random.randint(30, WINDOW_WIDTH-30), burgers_rect.bottom+25)
            burgers_eaten += 1

            if boost < 100:
                boost += 1

        if burger_img_rect.y >= WINDOW_HEIGHT:
            miss.play()
            lives -= 1
            burger_img_rect.center = (random.randint(30, WINDOW_WIDTH-30), burgers_rect.bottom+25)

        keys = pygame.key.get_pressed()

        if keys[pygame.K_LEFT]:
            dog = dog_left
            if dog_rect.left > 0:
                if keys[pygame.K_SPACE] and boost > 0:
                    boost -= 1
                    dog_rect.centerx -= VELOCITY*BOOST 
                else:
                    dog_rect.centerx -= VELOCITY
        elif keys[pygame.K_RIGHT]:
            dog = dog_right
            if dog_rect.right < WINDOW_WIDTH+20:
                if keys[pygame.K_SPACE] and boost > 0:
                    boost -= 1
                    dog_rect.centerx += VELOCITY*BOOST 
                else:
                    dog_rect.centerx += VELOCITY
        elif keys[pygame.K_UP] and dog_rect.top > burgers_rect.centery+25:
            if keys[pygame.K_SPACE] and boost > 0:
                boost -= 1
                dog_rect.centery -= VELOCITY*BOOST 
            else:
                dog_rect.centery -= VELOCITY
        elif keys[pygame.K_DOWN] and dog_rect.bottom < WINDOW_HEIGHT+20:
            if keys[pygame.K_SPACE] and boost > 0:
                boost -= 1
                dog_rect.centery += VELOCITY*BOOST 
            else:
                dog_rect.centery += VELOCITY
    
        display_surface.blit(burger, burger_img_rect)

    else:
        lose_txt = font.render(f"FINAL SCORE: {score}", True, ORANGE)
        display_surface.blit(lose_txt, lose_rect)
        display_surface.blit(continue_txt, continue_rect)
        pygame.mixer.music.stop()
         
    pygame.draw.line(display_surface, WHITE, (0, burgers_rect.centery+20), (WINDOW_WIDTH, burgers_rect.centery+20))

    lives_txt = font.render(f"Lives: {lives}", True, ORANGE)
    score_txt = font.render(f"Score: {score}", True, ORANGE)
    burgers_txt = font.render(f"Burgers Eaten: {burgers_eaten}", True, ORANGE)
    boost_txt = font.render(f"Boost: {boost}", True, ORANGE)
    points_txt = font.render(f"Burger Points: {points}", True, ORANGE)

    display_surface.blit(name_txt, name_rect)
    display_surface.blit(lives_txt, lives_rect)
    display_surface.blit(score_txt, score_rect)
    display_surface.blit(burgers_txt, burgers_rect)
    display_surface.blit(boost_txt, boost_rect)
    display_surface.blit(points_txt, points_rect)

    display_surface.blit(dog, dog_rect)
    pygame.display.update()

    #Tick the clock
    clock.tick(FPS)


pygame.quit()
