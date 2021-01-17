import pygame
import random
import os
from os import path

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
v_bashne = False


def start_screen():
    fon = pygame.transform.scale(pygame.image.load('img/fon.png').convert(), (WIDTH, HEIGHT))
    screen.blit(fon, (0, 0))
    button_sprites = pygame.sprite.Group()
    button = Button(900, 410, 'img/button1.png')
    button_sprites.add(button)
    button1 = Button(900, 510, 'img/button2.png')
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
        self.rect = self.image.get_rect()
        self.rect.topleft = x, y
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

    def pressed(self, pos):
        mx, my = pos
        if mx > self.rect.topleft[0] and my > self.rect.topleft[1]:
            if mx < self.rect.bottomright[0] and my < self.rect.bottomright[1]:
                return True


class Words(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        global words_imgs
        if a == 0:
            self.image = pygame.transform.scale(words_imgs[0], (650, 500))
            self.image.set_colorkey(WHITE)
            self.rect = self.image.get_rect()
            self.rect.topleft = x, y
        if a == 1:
            self.image = pygame.transform.scale(words_imgs[1], (650, 500))
            self.image.set_colorkey(WHITE)
            self.rect = self.image.get_rect()
            self.rect.topleft = x, y
        if a == 2:
            self.image = pygame.transform.scale(words_imgs[2], (650, 500))
            self.image.set_colorkey(WHITE)
            self.rect = self.image.get_rect()
            self.rect.topleft = x, y

    def pressed(self, pos):
        mx, my = pos
        if mx > self.rect.topleft[0] and my > self.rect.topleft[1]:
            if mx < self.rect.bottomright[0] and my < self.rect.bottomright[1]:
                return True


class Oven(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        global oven_imgs
        self.index = 0
        self.image = pygame.transform.scale(oven_imgs[0], (200, 360))
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

    def update(self):
        self.index += 1
        if self.index >= len(oven_imgs):
            self.index = 0
        self.image = pygame.transform.scale(oven_imgs[self.index], (150, 300))
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
        self.speedy = 0
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
        elif keystate[pygame.K_UP] and RIGHT is True:
            pass
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
        self.rect.y += self.speedy


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
            LEFT = False
        elif self.x == 2400 and self.rect.centerx <= player.rect.centerx:
            RIGHT = False


class Bashnya(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        global bash_image
        bash_image = pygame.transform.scale(bash_image, (750, 1000))
        self.image = bash_image
        self.image.set_colorkey(WHITE)
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.x = x


class Etaj(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        global etaj_image, etaj_image2
        etaj_image = pygame.transform.scale(etaj_image, (750, 400))
        self.image = etaj_image
        self.image.set_colorkey(WHITE)
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)


class Room(pygame.sprite.Sprite):
    def __init__(self, x, y, invert=False):
        pygame.sprite.Sprite.__init__(self)
        global etaj_image2
        etaj_image3 = etaj_image2
        etaj_image3 = pygame.transform.scale(etaj_image3, (750, 400))
        if invert:
            etaj_image3 = pygame.transform.flip(etaj_image3, invert, False)
        self.image = etaj_image3
        self.image.set_colorkey(WHITE)
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)


class Door(pygame.sprite.Sprite):
    def __init__(self, x, y, invert=False):
        pygame.sprite.Sprite.__init__(self)
        global door_image
        door_image = door_image
        door_image = pygame.transform.scale(door_image, (80, 130))
        self.image = door_image
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.y = y


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
pygame.time.set_timer(pygame.USEREVENT + 1, 1500)
pygame.time.set_timer(pygame.USEREVENT + 5, 150)
screen = pygame.display.set_mode((WIDTH, HEIGHT))
background = pygame.image.load(path.join(img_dir, "fon.png")).convert()
background = pygame.transform.scale(background, (1920, 1020))
background_rect = background.get_rect()
pygame.display.set_caption("My Game")
player_imgs = [pygame.image.load('img/pb1.png').convert(), pygame.image.load('img/pb2.png').convert(),
               pygame.image.load('img/pb3.png').convert(), pygame.image.load('img/pb4.png').convert(),
               pygame.image.load('img/pb5.png').convert()]
dirt_image = pygame.image.load('img/dirt.png').convert()
bash_image = pygame.image.load('img/basn.png').convert()
oven_imgs = [pygame.image.load('img/p2.png').convert(),
             pygame.image.load('img/p3.png').convert(), pygame.image.load('img/p4.png').convert()]
bash_image = pygame.image.load('img/basn.png').convert()
etaj_image = pygame.image.load('img/etaj.jpg').convert()
etaj_image2 = pygame.image.load('img/etaj_pravo.jpg').convert()
door_image = pygame.image.load('img/door.png').convert()
words_imgs = [pygame.image.load('img/word.png').convert(),
             pygame.image.load('img/word1.png').convert(), pygame.image.load('img/word2.png').convert()]
all_sprites = pygame.sprite.Group()
oven_sprites = pygame.sprite.Group()
land = pygame.sprite.Group()
clock = pygame.time.Clock()
seller_sprites = pygame.sprite.Group()
seller = Seller(pygame.image.load('img/man2.png').convert(), 4, 1, 1100, 780)
seller1 = Seller(pygame.image.load('img/man1.png').convert(), 4, 1, 1900, 780)
seller2 = Seller(pygame.image.load('img/woman.png').convert(), 4, 1, 900, 780)
seller_sprites.add(seller)
seller_sprites.add(seller1)
seller_sprites.add(seller2)
oven = Oven(1050, 860)
oven_sprites.add(oven)
all_bashnya = pygame.sprite.Group()
camera = Camera()
bashnya = Bashnya(1500, 450)
for i in range(25):
    dirt = Float(100 * i, 1050)
    land.add(dirt)
player = Player(200, 900)
land.add(bashnya)
all_sprites.add(player)
start_screen()
for i in range(-9190, 811, 400):
    centr = Etaj(900, i)
    prav_komnata = Room(1650, i)
    lev_komnata = Room(150, i, True)
    door = Door(900, i + 66)
    all_bashnya.add(lev_komnata)
    all_bashnya.add(prav_komnata)
    all_bashnya.add(centr)
    all_bashnya.add(door)

# Цикл игры
running = True
left = False
while running:
    # Держим цикл на правильной скорости
    clock.tick(FPS)
    # Ввод процесса (события)
    if v_bashne is False:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.USEREVENT + 1:
                seller_sprites.update()

            elif event.type == pygame.USEREVENT + 5:
                oven_sprites.update()
            elif event.type == pygame.KEYDOWN:
                keystate = pygame.key.get_pressed()
                if keystate[pygame.K_UP]:
                    if bashnya.rect.centerx - 200 <= player.rect.centerx <= bashnya.rect.centerx + 200:
                        v_bashne = True
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if seller.pressed(pygame.mouse.get_pos()):
                    a = 0
                    word = Words(seller.rect.topleft[0] - 50, seller.rect.topleft[1] - 100)
                    seller_sprites.add(word)
                elif seller1.pressed(pygame.mouse.get_pos()):
                    a = 1
                    word1 = Words(seller1.rect.topleft[0] - 50, seller.rect.topleft[1] - 100)
                    seller_sprites.add(word1)
                elif seller2.pressed(pygame.mouse.get_pos()):
                    a = 2
                    word2 = Words(seller2.rect.topleft[0] - 50, seller.rect.topleft[1] - 100)
                    seller_sprites.add(word2)


        # Обновление
        all_sprites.update()
        land.update()
        # Рендеринг
        screen.blit(background, background_rect)
        camera.update(player)
        for sprite in all_sprites:
            camera.apply(sprite)
        for sprite in seller_sprites:
            camera.apply(sprite)
        for sprite in oven_sprites:
            camera.apply(sprite)
        for sprite in land:
            camera.apply(sprite)
        oven_sprites.draw(screen)
        land.draw(screen)
        seller_sprites.draw(screen)
        all_sprites.draw(screen)
    else:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                keystate = pygame.key.get_pressed()
                if keystate[pygame.K_UP]:
                    player.rect.centery -= 400
                elif keystate[pygame.K_DOWN]:
                    if door.y == 876 and door.rect.centerx - 20 <= player.rect.centerx <= door.rect.centerx + 20:
                        v_bashne = False
                    elif door.rect.centerx - 20 <= player.rect.centerx <= door.rect.centerx + 20:
                        player.rect.centery += 400
        all_sprites.update()
        all_bashnya.update()
        # Рендеринг
        screen.blit(background, background_rect)
        camera.update(player)
        for sprite in all_sprites:
            camera.apply(sprite)
        for sprite in all_bashnya:
            camera.apply(sprite)
        all_bashnya.draw(screen)
        all_sprites.draw(screen)

    pygame.display.flip()

pygame.quit()