import pygame
import random
import os
from os import path
WIDTH = 920
HEIGHT = 620
FPS = 30
# Задаем цвета
import pygame
import random
import os
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
LEFT = True
RIGHT = True
pygame.time.set_timer(pygame.USEREVENT + 1, 900)
pygame.time.set_timer(pygame.USEREVENT + 5, 150)


def start_screen():
    fon = pygame.transform.scale(pygame.image.load('img/fon.png').convert(), (WIDTH, HEIGHT))
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
                if button1.pressed(pygame.mouse.get_pos()):
                    pygame.quit()
                    quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if button.pressed(pygame.mouse.get_pos()):
                    return
            elif event.type == pygame.QUIT:
                pygame.quit()
                quit()
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

    def pressed(self, pos):
        mx, my = pos
        if mx > self.rect.topleft[0] and my > self.rect.topleft[1]:
            if mx < self.rect.bottomright[0] and my < self.rect.bottomright[1]:
                return True


class Seller(pygame.sprite.Sprite):
    def __init__(self, sheet, columns, rows, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.frames = []
        self.cut_sheet(sheet, columns, rows)
        self.cur_frame = 0
        self.image = pygame.transform.scale(self.frames[self.cur_frame], (130, 170))
        self.rect = self.rect.move(x, y)
        self.image.set_colorkey(BLACK)

    def cut_sheet(self, sheet, columns, rows):
        self.rect = pygame.Rect(0, 0, sheet.get_width() // columns,
                                sheet.get_height() // rows)
        for j in range(rows):
            for i in range(columns):
                frame_location = (self.rect.w * i, self.rect.h * j)
                self.frames.append(sheet.subsurface(pygame.Rect(
                    frame_location, self.rect.size)))

    def update(self):
        self.cur_frame = (self.cur_frame + 1) % len(self.frames)
        self.image = pygame.transform.scale(self.frames[self.cur_frame], (130, 170))
        self.image.set_colorkey(BLACK)


class Oven(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        global oven_imgs
        self.index = 0
        self.image = pygame.transform.scale(oven_imgs[0], (100, 180))
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

    def update(self):
        self.index += 1
        if self.index >= len(oven_imgs):
            self.index = 0
        self.image = pygame.transform.scale(oven_imgs[self.index], (100, 180))
        self.image.set_colorkey(BLACK)


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


class Bashnya(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        global bash_image
        bash_image = pygame.transform.scale(bash_image, (750, 500))
        self.image = bash_image
        self.image.set_colorkey(WHITE)
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.x = x


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
bash_image = pygame.image.load('img/basn.png').convert()
oven_imgs = [pygame.image.load('img/p2.png').convert(),
             pygame.image.load('img/p3.png').convert(), pygame.image.load('img/p4.png').convert()]
clock = pygame.time.Clock()
all_sprites = pygame.sprite.Group()
oven_sprites = pygame.sprite.Group()
camera = Camera()
bashnya = Bashnya(700, 350)
for i in range(25):
    dirt = Float(100 * i, 650)
    all_sprites.add(dirt)
player = Player(200, 550)
all_sprites.add(bashnya)
all_sprites.add(player)
seller_sprites = pygame.sprite.Group()
seller = Seller(pygame.image.load('img/man2.png').convert(), 4, 1, 60, 470)
seller1 = Seller(pygame.image.load('img/man1.png').convert(), 4, 1, 300, 470)
seller2 = Seller(pygame.image.load('img/woman.png').convert(), 4, 1, 500, 470)
seller_sprites.add(seller)
seller_sprites.add(seller1)
seller_sprites.add(seller2)
oven = Oven(20, 550)
oven_sprites.add(oven)
start_screen()

# Цикл игры
running = True
left = False
while running:
    # Держим цикл на правильной скорости
    clock.tick(FPS)
    # Ввод процесса (события)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.USEREVENT + 1:
            seller_sprites.update()

        elif event.type == pygame.USEREVENT + 5:
            oven_sprites.update()
    all_sprites.update()
    # Рендеринг
    screen.fill(BLACK)
    screen.blit(background, background_rect)
    camera.update(player)
    for sprite in all_sprites:
        camera.apply(sprite)
    for sprite in seller_sprites:
        camera.apply(sprite)
    for sprite in oven_sprites:
        camera.apply(sprite)
    all_sprites.draw(screen)
    seller_sprites.draw(screen)
    oven_sprites.draw(screen)
    pygame.display.flip()

pygame.quit()