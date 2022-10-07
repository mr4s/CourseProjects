import pygame, random
from player import Player
from zombies import Zombie
from portals import Green_Portal, Purple_Portal
from ruby import BigRuby#, Ruby
from setup import *

class Game():
    def __init__(self):
        pygame.font.init()

        self.poultrygeist_font = pygame.font.Font("../assets/fonts/Poultrygeist.ttf", 40)
        self.pixel_font = pygame.font.Font("../assets/fonts/Pixel.ttf", 21)
        self.game_name_txt = self.poultrygeist_font.render("Zombie Knight", True, GREEN)
        self.game_name_rect = self.game_name_txt.get_rect()
        self.game_name_rect.center = (WINDOW_WIDTH//2, WINDOW_HEIGHT//2-50)
        self.begin_txt = self.poultrygeist_font.render("Press 'Enter' to Begin", True, WHITE)
        self.begin_rect = self.begin_txt.get_rect()
        self.begin_rect.center = (WINDOW_WIDTH//2, WINDOW_HEIGHT//2+30)

        self.begin = False

        self.night = 1
        self.tts = STARTING_TIME
        self.zombie_interval = 5

        self.initialize()

    def update(self, attack=False):
        if self.begin == False:
            display_surface.blit(self.game_name_txt, self.game_name_rect)
            display_surface.blit(self.begin_txt, self.begin_rect)
        else:
            for t in self.tile_group:
                t.update()

            self.kill_zombies()

            self.center_ruby.update()
            self.portal_group.update(self.player_group, self.zombie_group)
            self.player_group.update(self.tile_group, self.portal_group, self.zombie_group, attack)
            self.zombie_group.update(self.player_group.sprites()[0].rect.center, self.portal_group, self.tile_group)

            self.blit_text()
            self.portal_group.draw(display_surface)
            self.player_group.draw(display_surface)
            self.zombie_group.draw(display_surface)

    def blit_text(self):
        score_txt = self.pixel_font.render(f"Score: {self.player_group.sprites()[0].score}", True, WHITE)
        health_txt = self.pixel_font.render(f"Health: {self.player_group.sprites()[0].health}", True, WHITE)
        night_txt = self.pixel_font.render(f"Night: {self.night}", True, WHITE)
        sunrise_txt = self.pixel_font.render(f"Sunrise In: {self.tts}", True, WHITE)

        score_rect = score_txt.get_rect()
        health_rect = health_txt.get_rect()
        night_rect = night_txt.get_rect() 
        sunrise_rect = sunrise_txt.get_rect()
        game_name_rect = self.game_name_txt.get_rect()

        health_rect.bottomleft = (5, WINDOW_HEIGHT-5)
        score_rect.bottomleft = (health_rect.topleft[0], health_rect.topleft[1]+3)
        sunrise_rect.bottomright = (WINDOW_WIDTH-5, WINDOW_HEIGHT-5)
        night_rect.bottomright = (sunrise_rect.topright[0], sunrise_rect.topright[1]+3)
        game_name_rect.center = (WINDOW_WIDTH//2, score_rect.bottom-3)
        
        display_surface.blit(health_txt, health_rect)
        display_surface.blit(score_txt, score_rect)
        display_surface.blit(sunrise_txt, sunrise_rect)
        display_surface.blit(night_txt, night_rect)
        display_surface.blit(self.game_name_txt, game_name_rect)

    def initialize(self):
        tile_map = [
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [7, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 8, 0],
            [4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 5, 0, 0, 0, 0, 6, 0, 0, 0, 0, 0, 3, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 5, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [4, 4, 4, 4, 4, 5, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3, 4, 4, 4, 4, 4],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 5, 0, 0, 0, 0, 0, 0, 0, 0, 3, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 9, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3, 4, 4, 5, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [8, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 7, 0],
            [2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2],
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
        ]

        self.initialize_tiles(tile_map)
        self.initialize_center_ruby()
        self.initialize_player(tile_map)
        self.initialize_portals(tile_map)
        self.initialize_zombies()
        # self.initialize_rubies()

    def initialize_rubies(self):
        self.ruby_group = pygame.sprite.Group()

        x = random.randint(32, WINDOW_WIDTH-32)
        ruby = Ruby(x, 0)
        self.ruby_group.add(ruby)

    def initialize_center_ruby(self):
        self.center_ruby = BigRuby()

    def initialize_portals(self, tile_map):
        self.portal_group = pygame.sprite.Group()
        for line in range(len(tile_map)):
            for row in range(len(tile_map[0])):
                if tile_map[line][row] == 7:
                    self.portal_group.add(Green_Portal(row*32-16, line*32+32))
                elif tile_map[line][row] == 8:
                    self.portal_group.add(Purple_Portal(row*32-16, line*32+32))

    def initialize_player(self, tile_map):
        self.player_group = pygame.sprite.Group()
        for line in range(len(tile_map)):
            for row in range(len(tile_map[0])):
                if tile_map[line][row] == 9:
                    player = Player(row*32, line*32)
                    self.player_group.add(player)

    def initialize_zombies(self):
        self.zombie_group = pygame.sprite.Group()

        x = random.randint(0, WINDOW_WIDTH-32)
        zombie = Zombie(x, 0, self.portal_group, random.choice(["boy", "girl"]))
        self.zombie_group.add(zombie)

    def initialize_tiles(self, tile_map):
        self.tile_group = pygame.sprite.Group()
        for line in range(len(tile_map)):
            for row in range(len(tile_map[0])):
                if tile_map[line][row] and tile_map[line][row] <= 5:
                    tile = Tiles(tile_map[line][row], row*32, line*32)
                    self.tile_group.add(tile)

    def start(self):
        self.begin = True

    def kill_zombies(self):
        if pygame.sprite.groupcollide(self.player_group.sprites()[0].slash_group, self.zombie_group, True, True):
            self.player_group.sprites()[0].score += 10

class Tiles(pygame.sprite.Sprite):
    def __init__(self, tile_type, x, y):
        super().__init__()

        self.image = pygame.image.load(f"../assets/images/tiles/Tile ({tile_type}).png")
        self.image = pygame.transform.scale(self.image, (32, 32))
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)

        #mask
        self.mask = pygame.mask.from_surface(self.image)
        
    def update(self):
        display_surface.blit(self.image, self.rect)

