import pygame
import random
import os
from os import path

WIDTH = 1920
HEIGHT = 1020
FPS = 60

# Задаем цвета
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)


class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        global player_img
        self.size = player_img.get_size()
        player_img = pygame.transform.scale(player_img, (int(self.size[0] * 3), int(self.size[1] * 3)))
        self.image = player_img
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH / 2, HEIGHT / 2)

    def update(self):
        pass


# Создаем игру и окно
game_folder = os.path.dirname(__file__)
img_dir = path.join(path.dirname(__file__), 'img')
pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
background = pygame.image.load(path.join(img_dir, "fon.jpg")).convert()
background_rect = background.get_rect()
pygame.display.set_caption("My Game")
img_folder = path.join(game_folder, 'img')
player_img = pygame.image.load('img/pb1.png').convert()
clock = pygame.time.Clock()
all_sprites = pygame.sprite.Group()
player = Player()
all_sprites.add(player)

# Цикл игры
running = True
while running:
    # Держим цикл на правильной скорости
    clock.tick(FPS)
    # Ввод процесса (события)
    for event in pygame.event.get():
        # check for closing window
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            keys = pygame.key.get_pressed()
            if keys[pygame.K_w]:
                player.move(0, -1)
            if keys[pygame.K_s]:
                player.move(0, 1)
            if keys[pygame.K_a]:
                player.move(-1, 0)
            if keys[pygame.K_d]:
                player.move(1, 0)

    # Обновление
    all_sprites.update()

    # Рендеринг
    screen.fill(BLACK)
    screen.blit(background, background_rect)
    all_sprites.draw(screen)
    pygame.display.flip()

pygame.quit()