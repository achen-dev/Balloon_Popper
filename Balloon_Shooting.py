# This code will generate a balloon shooting game powered by the external library pygame.
# The balloon will move up and down randomly, and the player will be controlling a cannon to shoot the balloon.
import pygame
import random
import sys
import time
from pygame.locals import *

pygame.init()

FPS = 60
FramePerSec = pygame.time.Clock()

BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
GREY = (192, 192, 192)
WHITE = (255, 255, 255)

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

font_small = pygame.font.SysFont("Verdana", 20)

SCORE = 0

game_window = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
game_window.fill(WHITE)
pygame.display.set_caption("Balloon Shooting")


class Balloon (pygame.sprite.Sprite):
    def __init__(self, speed=None):
        super().__init__()
        if speed is None:
            speed = 5
        self.image = pygame.image.load("balloon.png")
        self.surf = pygame.Surface((50, 50))
        self.rect = self.surf.get_rect(center=(25, 25))
        self.speed = speed

    def update(self):
        if self.rect.bottom > SCREEN_HEIGHT or self.rect.top < 0:
            self.speed *= -1
        elif random.randint(0, 90) == 5:
            self.speed *= -1
        self.rect.y = self.rect.y + self.speed

    def draw(self, surface):
        surface.blit(self.image, self.rect)


class Cannon (pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("cannon.png")
        self.surf = pygame.Surface((100, 50))
        self.rect = self.surf.get_rect(center=(SCREEN_WIDTH, SCREEN_HEIGHT-25))

    def update(self):
        pressed_keys = pygame.key.get_pressed()
        if self.rect.top > 0:
            if pressed_keys[K_UP]:
                self.rect.move_ip(0, -5)
        if self.rect.bottom < SCREEN_HEIGHT:
            if pressed_keys[K_DOWN]:
                self.rect.move_ip(0, 5)

    def cannon_center(self):
        return self.rect.x

    def draw(self, surface):
        surface.blit(self.image, self.rect)


class Bullet (pygame.sprite.Sprite):
    def __init__(self, ):
        super().__init__()
        self.image = pygame.image.load("bullet.png")
        self.surf = pygame.Surface((50, 50))
        self.rect = self.surf.get_rect(center=(SCREEN_WIDTH - 50, -100))

    def move(self, barrel):
        global SCORE
        keypress = pygame.key.get_pressed()
        if keypress[K_SPACE] and self.rect.x < 0:
            self.rect.y = barrel.rect.y + 15
            self.rect.x = SCREEN_WIDTH - 75
            SCORE += 1
        elif self.rect.x > -50:
            self.rect.move_ip(-10, 0)

    def draw(self, surface):
        surface.blit(self.image, self.rect)


CANNON = Cannon()
BALLOON = Balloon()
BULLET = Bullet()
projectiles = [BULLET]
font = pygame.font.SysFont("Verdana", 20)


while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
    game_window.fill(WHITE)
    scores = font_small.render(str(SCORE), True, BLACK)
    game_window.blit(scores, (10, 10))
    CANNON.draw(game_window)
    BALLOON.draw(game_window)
    BULLET.draw(game_window)
    BULLET.move(CANNON)
    BALLOON.update()
    CANNON.update()
    game_over = font.render("Congratulations! it took you %s shots to hit the balloon" % SCORE, True, BLACK)
    if pygame.sprite.spritecollide(BALLOON, projectiles, False):
        game_window.fill(GREEN)
        game_window.blit(game_over, (30, 250))
        pygame.display.update()
        time.sleep(5)
        pygame.quit()
        sys.exit()
    pygame.display.update()
    FramePerSec.tick(FPS)
