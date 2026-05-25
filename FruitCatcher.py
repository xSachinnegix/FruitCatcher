import pygame
import sys
import random
import time
from pygame.locals import *

#verison 2 of fruit catcher

pygame.init()
#audio settings
pygame.mixer.pre_init(44100, -16, 2, 2048)
pygame.mixer.init()
#screen size settings
screen_width = 800
screen_hight = 600
pygame.display.set_caption("Fruit Catcher")
screen = pygame.display.set_mode((screen_width, screen_hight))
screen_w, screen_h = pygame.display.get_surface().get_size()

#font/tick
clock = pygame.time.Clock()
font = pygame.font.SysFont("arial bold", 35)
big_font = pygame.font.SysFont("arial", 50)
small_font = pygame.font.SysFont("arial", 20)

#colours in use
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (220, 50, 50)
YELLOW = (255, 220, 0)
ORANGE = (255, 140, 0)
GREEN = (0, 180, 0)
BLUE = (100, 180, 255)
BROWN = (139, 90, 43)

# loading in the fruit images from the assets folder
apple_img = pygame.image.load("Assets/ApplePNG.png").convert_alpha()
apple_img = pygame.transform.scale(apple_img, (36, 36))

banana_img = pygame.image.load("Assets/BananaPNG.png").convert_alpha()
banana_img = pygame.transform.scale(banana_img, (36, 36))

broccoli_img = pygame.image.load("Assets/BroccoliPNG.png").convert_alpha()
broccoli_img = pygame.transform.scale(broccoli_img, (36, 36))

bomb_img = pygame.image.load("Assets/BombPNG.png").convert_alpha()
bomb_img = pygame.transform.scale(bomb_img, (36, 36))

# loading the background image from the assets folder
sky_img = pygame.image.load("Assets/SkyPNG.png").convert()
sky_img = pygame.transform.scale(sky_img, (screen_w, screen_h))

# loading the basket image from the assets folder
basket_img = pygame.image.load("Assets/BasketPNG.png").convert_alpha()
basket_img = pygame.transform.scale(basket_img, (90, 30))

# loading audio files
pygame.mixer.music.load("Assets/Crazy-Candy-Highway-2.ogg")
pygame.mixer.music.play(-1)  # -1 means loop forever
fruit_catch = pygame.mixer.Sound("Assets/mixkit-fairy-arcade-sparkle-866.wav")

#list that holds everything falling on screen
falling_fruits = []

#this is the base class all of the fruits inherit from this
class FallingFruit:
    def __init__(self):
        self.x = random.randint(30, screen_w - 30)
        self.y = -30
        self.width = 36
        self.height = 36
        self.speed = 3
        self.points = 0
    def move(self):
        # this moves the obj down every frame
        self.y = self.y + self.speed
    def off_screen(self):
        #if the obj went past the bottom then return true
        return self.y > screen_h + 30
    def draw(self):
        pygame.draw.rect(screen, WHITE, (int(self.x), int(self.y), self.width, self.height))
    def get_rect(self):
        #this is needed for collision detection
        return pygame.Rect(int(self.x), int(self.y), self.width, self.height)

#apple gives 1 point
class Apple(FallingFruit):
    def __init__(self,falling_speed):
        super().__init__()
        self.speed = falling_speed
        self.points = 1
    def draw(self):
            screen.blit(apple_img, (int(self.x), int(self.y)))


#banana gives 2 point, falls slightly faster
class Banana(FallingFruit):
    def __init__(self, falling_speed):
        super().__init__()
        self.points = 2
        self.speed = falling_speed + 1.3
    def draw(self):
        screen.blit(banana_img, (int(self.x), int(self.y)))

#broccoli takes away 3 points
class Broccoli(FallingFruit):
    def __init__(self, falling_speed):
        super().__init__()
        self.points = -3
        self.speed = falling_speed -1
    def draw(self):
        screen.blit(broccoli_img, (int(self.x), int(self.y)))


#bomb loses a lfie
class Bomb(FallingFruit):
    def __init__(self, falling_speed):
        super().__init__()
        self.points = 0
        self.speed = falling_speed
    def draw(self):
        screen.blit(bomb_img, (int(self.x), int(self.y)))
#player controlled basket
class Basket:
    def __init__(self):
        self.x = screen_w / 2
        self.y = screen_h - 40
        self.width = 90
        self.height = 30
        self.speed = 7
#added basket movement
    def move(self):
        if pressed_key[K_RIGHT]:
            self.x = self.x + self.speed
        if pressed_key[K_LEFT]:
            self.x = self.x - self.speed
            #stops the basket from going off the edge
        if self.x < 0:
            self.x = 0
        if self.x > screen_w - self.width:
            self.x = screen_w - self.width

    def draw(self):
        screen.blit(basket_img, (int(self.x), int(self.y)))

    def get_rect(self):
        return pygame.Rect(int(self.x), int(self.y), self.width, self.height)

#this is the main class which handles the scores, lives, waves and spawning
class Game:
    def __init__(self):
        self.score = 0
        self.lives = 3
        self.apple_counts = 0
        self.banana_counts = 0
        self.wave = 1
        self.wave_start_time = time.time()
        self.last_spawn = time.time()
        self.spawn_rate = 0.8
        self.falling_speed = 3
        self.game_running = True
        self.win_screen = False
        self.wave_message = False
        self.message_time = 0

    def wave_refresh(self):
        if time.time() - self.wave_start_time > 15:
            self.wave = self.wave + 1
            self.falling_speed = self.falling_speed + 0.5
            self.spawn_rate = max(0.4, self.spawn_rate - 0.1)
            self.wave_start_time = time.time()
            self.wave_message = True
            self.message_time = time.time()

    def spawn_fruit(self):
        if time.time() - self.last_spawn > self.spawn_rate:
            if self.wave == 1:
                choice = random.randint(1, 6)
            elif self.wave == 2:
                choice = random.randint(1, 7)
            else:
                choice = random.randint(1, 8)
            if choice == 1 or choice == 2:
                falling_fruits.append(Apple(self.falling_speed))
            elif choice == 3 or choice == 4:
                falling_fruits.append(Banana(self.falling_speed))
            elif choice == 5:
                falling_fruits.append(Broccoli(self.falling_speed))
            elif choice == 6 or choice == 7 or choice == 8:
                falling_fruits.append(Bomb(self.falling_speed))
            self.last_spawn = time.time()

#checks if basket got any fruits
    def collision_check(self, basket):
        for obj in falling_fruits[:]:
            if obj.get_rect().colliderect(basket.get_rect()):
                if isinstance(obj, Apple):
                    self.apple_counts = self.apple_counts + 1
                    self.score = self.score + obj.points
                    fruit_catch.play()
                elif isinstance(obj, Banana):
                    self.banana_counts = self.banana_counts + 1
                    self.score = self.score + obj.points
                    fruit_catch.play()
                elif isinstance(obj, Bomb):
                    self.lives = self.lives - 1
                elif isinstance(obj, Broccoli):
                    self.score = max(0, self.score + obj.points)
                falling_fruits.remove(obj)
                if self.lives <= 0:
                    self.game_running = False
                if self.apple_counts >= 10 and self.banana_counts >= 10:
                    self.game_running = False
                    self.win_screen = True
        for obj in falling_fruits[:]:
            if obj.off_screen():
                falling_fruits.remove(obj)

    def hud(self):
        score_text = font.render("Score: " + str(self.score), True, WHITE)
        lives_text = font.render("Lives: " + str(self.lives), True, WHITE)
        wave_text = font.render("Wave: " + str(self.wave), True, WHITE)
        apples_text = small_font.render("Apples: " + str(self.apple_counts) + "/10", True, RED)
        bananas_text = small_font.render("Bananas: " + str(self.banana_counts) + "/10", True, YELLOW)
        screen.blit(score_text, (10, 10))
        screen.blit(lives_text, (10, 40))
        screen.blit(wave_text, (screen_w - 120, 10))
        screen.blit(apples_text, (screen_w // 2 - 100, 10))
        screen.blit(bananas_text, (screen_w // 2 - 100, 35))

        if self.wave_message:
            if time.time() - self.message_time < 2:
                wave_msg = big_font.render("Wave " + str(self.wave) + "!", True, ORANGE)
                screen.blit(wave_msg, (screen_w // 2 - 80, screen_h // 2 - 30))
            else:
                self.wave_message = False

    def end_screen(self, won):
            screen.fill(BLACK)
            if won:
                title = big_font.render("congratulations you won !", True, GREEN)
            else:
                title = big_font.render("GAME OVER GOOD LUCK NEXT TIME", True, RED)
            score_text = font.render("Final Score: " + str(self.score), True, WHITE)
            apples_text = font.render("Apples caught: " + str(self.apple_counts) + "/10", True, RED)
            bananas_text = font.render("Bananas caught: " + str(self.banana_counts) + "/10", True, YELLOW)
            restart_text = font.render("Press R to restart or Q to quit", True, WHITE)

            #centering the end and win screen fonts
            title_rect = title.get_rect(center=(screen_w // 2, screen_h // 2 - 120))
            screen.blit(title, title_rect)
            score_rect = score_text.get_rect(center=(screen_w // 2, screen_h // 2 - 60))
            screen.blit(score_text, score_rect)
            apples_rect = apples_text.get_rect(center=(screen_w // 2, screen_h // 2 - 20))
            screen.blit(apples_text, apples_rect)
            bananas_rect = bananas_text.get_rect(center=(screen_w // 2, screen_h // 2 + 20))
            screen.blit(bananas_text, bananas_rect)
            restart_rect = restart_text.get_rect(center=(screen_w // 2, screen_h // 2 + 70))
            screen.blit(restart_text, restart_rect)
            pygame.display.flip()
            waiting = True
            while waiting:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_r:
                            falling_fruits.clear()
                            self.score = 0
                            self.lives = 3
                            self.apple_counts = 0
                            self.banana_counts = 0
                            self.wave = 1
                            self.falling_speed = 3
                            self.spawn_rate = 0.8
                            self.wave_start_time = time.time()
                            self.last_spawn = time.time()
                            self.game_running = True
                            self.win_screen = False
                            waiting = False
                        if event.key == pygame.K_q:
                            pygame.quit()
                            sys.exit()


basket = Basket()
game = Game()
#main game looks which keeps on running until the game ends#

while True:
    clock.tick(60)
    pressed_key = pygame.key.get_pressed()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
    if game.game_running:
        game.wave_refresh()
        game.spawn_fruit()
        basket.move()
        for obj in falling_fruits:
            obj.move()
        game.collision_check(basket)
        screen.blit(sky_img, (0, 0))
        basket.draw()
        for obj in falling_fruits:
            obj.draw()
        game.hud()
        pygame.display.flip()
    else:
        game.end_screen(game.win_screen)
