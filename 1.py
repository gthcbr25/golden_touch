import pygame
import random
import os
import sqlite3
from os import path

WIDTH = 920
HEIGHT = 620

WIDTH = 1920
HEIGHT = 1020
FPS = 30
# Задаем цвета
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
LEFT = True
RIGHT = True
name1 = ''


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
        global LEFT, RIGHT
        if keystate[pygame.K_LEFT] and LEFT is True:
            self.speedx = -10
            self.animcount += 1
            self.invert = True
            RIGHT = True
        elif keystate[pygame.K_RIGHT] and RIGHT is True:
            self.invert = False
            self.speedx = 10
            self.animcount += 1
            LEFT = True
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


class Float(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = dirt_image
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.x = x

    def update(self):
        global LEFT, RIGHT
        if self.x == 0 and self.rect.centerx >= player.rect.centerx:
            print(0)
            LEFT = False
        elif self.x == 2400 and self.rect.centerx <= player.rect.centerx:
            RIGHT = False


class Camera:
    # зададим начальный сдвиг камеры
    def __init__(self):
        self.dx = 0
        self.dy = 0

    # сдвинуть объект obj на смещение камеры
    def apply(self, obj):
        obj.rect.x += self.dx
        obj.rect.y += self.dy

    # позиционировать камеру на объекте target
    def update(self, target):
        self.dx = -(target.rect.x + target.rect.w // 2 - WIDTH // 2)
        self.dy = -(target.rect.y + target.rect.h - HEIGHT + 80)


class Weapon(pygame.sprite.Sprite):
    def __init__(self, x, y, name):
        global name1
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((50, 50))
        self.image.fill(GREEN)
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        name1 = name


class Youweapon(pygame.sprite.Sprite):
    def __init__(self, x, y):
        global name1
        global youweapon
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(f'{youweapon}').convert()
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

    def podobr(self):
        global youweapon
        con = sqlite3.connect('bd/Inventory')
        cur = con.cursor()
        result = cur.execute(f'SELECT picture FROM Weapon WHERE name LIKE "{name1}"').fetchall()
        for elem in result:
            youweapon = elem[0]
        con.close()

    def update(self):
        self.rect.centerx = player.rect.centerx - 500
        self.rect.centery = player.rect.centery - 500
        self.image = pygame.image.load(f'{youweapon}').convert()
        self.image.set_colorkey(BLACK)


# Создаем игру и окно
img_dir = path.join(path.dirname(__file__), 'img')
pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
background = pygame.image.load(path.join(img_dir, "fon.png")).convert()
background = pygame.transform.scale(background, (1920, 1020))
background_rect = background.get_rect()
pygame.display.set_caption("My Game")
player_imgs = [pygame.image.load('img/pb1.png').convert(), pygame.image.load('img/pb2.png').convert(),
               pygame.image.load('img/pb3.png').convert(), pygame.image.load('img/pb4.png').convert(),
               pygame.image.load('img/pb5.png').convert()]
dirt_image = pygame.image.load('img/dirt.png').convert()
youweapon = 'img/Gold corty.png'
clock = pygame.time.Clock()
all_sprites = pygame.sprite.Group()
camera = Camera()
for i in range(25):
    dirt = Float(100 * i, 1050)
    all_sprites.add(dirt)
player = Player(200, 900)
all_sprites.add(player)

weapon = Weapon(500, 900, 'bronze')
all_sprites.add(weapon)
uweapon = Youweapon(200, 200)
all_sprites.add(uweapon)
check_weapon = False
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
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_e:
                if player.rect.centerx - 100 < weapon.rect.centerx < player.rect.centerx + 100:
                    if player.rect.centery - 20 < weapon.rect.centery < player.rect.centery + 20:
                        check_weapon = True

    # Обновление
    all_sprites.update()
    if check_weapon:
        uweapon.podobr()
        check_weapon = False
    # Рендеринг
    screen.fill(BLACK)
    screen.blit(background, background_rect)
    camera.update(player)
    for sprite in all_sprites:
        camera.apply(sprite)
    all_sprites.draw(screen)
    pygame.display.flip()

pygame.quit()
