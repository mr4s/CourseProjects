import pygame
import game
from setup import *

if __name__ == "__main__":
    pygame.init()

    pygame.display.set_caption("Zombie Knight")

    bg_img = pygame.image.load("../assets/images/background.png")
    bg_img = pygame.transform.scale(bg_img, (1280, 736))

    game = game.Game()

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                running = False
                break
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN and game.begin == False:
                    game.start()
                elif event.key == pygame.K_RETURN and game.start_night == False:
                    game.new_night(True)
                if event.key == pygame.K_SPACE:
                    game.update(True)
                
        if game.begin and game.start_night:
            display_surface.blit(bg_img, (0, 0))
        else:
            display_surface.fill((0, 0, 0))

        game.update()
        pygame.display.update()

        #Tick the clock
        clock.tick(FPS)


    pygame.quit()
