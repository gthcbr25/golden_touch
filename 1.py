import pygame
import random
import os
import sys
from os import path
WIDTH = 920
HEIGHT = 620
FPS = 30
# Задаем цвета
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)


def start_screen():
    fon = pygame.transform.scale(pygame.image.load('img/fon.png').convert(), (WIDTH, HEIGHT))
    print('3')
    screen.blit(fon, (0, 0))
    button_sprites = pygame.sprite.Group()
    button = Button(350, 100, 'img/button1.png')
    button_sprites.add(button)
    button1 = Button(350, 200, 'img/button2.png')
    button_sprites.add(button1)
    running = True
    while running:
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                mx, my = pygame.mouse.get_pos()
                if button1.pressed(mx, my):
                    pygame.quit()
                    quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                mx, my = pygame.mouse.get_pos()
                if button.pressed(mx, my):
                    return
        button_sprites.draw(screen)
        pygame.display.flip()
        clock.tick(FPS)


class Button(pygame.sprite.Sprite):
    def __init__(self, x, y, img):
        self.x = x
        self.y = y
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(pygame.image.load(f'{img}').convert(), (160, 70))
        self.rect = self.image.get_rect()
        self.rect.topleft = self.x, self.y
        self.image.set_colorkey(BLACK)

    def pressed(self, mx, my):
        if mx > self.rect.topleft[0] and my > self.rect.topleft[1]:
            if mx < self.rect.bottomright[0] and my < self.rect.bottomright[1]:
                return True


class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        global player_imgs
        self.imgs = player_imgs
        self.animcount = 0
        self.invert = False
        player_img = pygame.transform.scale(player_imgs[0], (player_imgs[0].get_size()[0] * 3,
                                                             player_imgs[0].get_size()[1] * 3))
        self.image = player_img
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.speedx = 0

    def update(self):
        keystate = pygame.key.get_pressed()
        self.speedx = 0
        if keystate[pygame.K_LEFT]:
            self.speedx = -8
            self.speedx = -10
            self.animcount += 1
            self.invert = True
        elif keystate[pygame.K_RIGHT]:
            self.invert = False
            self.speedx = 8
            self.speedx = 10
            self.animcount += 1
        else:
            self.animcount = 0
        if self.animcount >= 30.00:
            self.animcount = 0
        a = self.animcount // 6
        player_img = pygame.transform.scale(self.imgs[a], (self.imgs[a].get_size()[0] * 3,
                                                           self.imgs[a].get_size()[1] * 3))
        player_img = pygame.transform.flip(player_img, self.invert, False)
        self.image = player_img
        self.image.set_colorkey(BLACK)
        x, y = self.rect.center
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.rect.x += self.speedx


# Создаем игру и окно
img_dir = path.join(path.dirname(__file__), 'img')
pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
background = pygame.image.load(path.join(img_dir, "fon.png")).convert()
background = pygame.transform.scale(background, (920, 620))
background_rect = background.get_rect()
pygame.display.set_caption("My Game")
player_imgs = [pygame.image.load('img/pb1.png').convert(), pygame.image.load('img/pb2.png').convert(),
               pygame.image.load('img/pb3.png').convert(), pygame.image.load('img/pb4.png').convert(),
               pygame.image.load('img/pb5.png').convert()]
dirt_image = pygame.image.load('img/dirt.png').convert()
fon_image = pygame.image.load('img/fon.png').convert()
clock = pygame.time.Clock()
all_sprites = pygame.sprite.Group()
player = Player(200, 600)
all_sprites.add(player)
start_screen()

# Цикл игры
running = True
left = False
while running:
    # Держим цикл на правильной скорости
    clock.tick(FPS)
    # Ввод процесса (события)
    for event in pygame.event.get():
        all_sprites.update()
        if event.type == pygame.QUIT:
            running = False
    # Обновление
    all_sprites.update()
    # Рендеринг
    screen.fill(BLACK)
    screen.blit(background, background_rect)
    all_sprites.draw(screen)
    pygame.display.flip()

pygame.quit()