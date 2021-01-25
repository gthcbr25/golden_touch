import sqlite3
import pygame
import random
import os
from os import path
from random import choice

WIDTH = 1920
HEIGHT = 1020
FPS = 30

# Задаем цвета
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
MEBEL = (17, 15, 39)
GREY = (155, 173, 183)
BROWN = (172, 116, 52)
LEFT = True
RIGHT = True
v_bashne = False
WEAPON = []
ARMOR = []
AMULET = []
con = sqlite3.connect('bd/Inventory')
cur = con.cursor()
result = cur.execute(f'SELECT name FROM Weapon').fetchall()
for i in result:
    WEAPON.append(i[0])
result = cur.execute(f'SELECT name FROM Armor').fetchall()
for i in result:
    ARMOR.append(i[0])
result = cur.execute(f'SELECT name FROM Amulet').fetchall()
for i in result:
    AMULET.append(i[0])


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


def death_screen():
    fon = pygame.transform.scale(pygame.image.load('img/fon.png').convert(), (WIDTH, HEIGHT))
    screen.blit(fon, (0, 0))
    button_sprites = pygame.sprite.Group()
    button1 = Button(900, 510, 'img/button2.png')
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
        button_sprites.draw(screen)
        pygame.display.flip()
        clock.tick(FPS)


def win_screen():
    button_sprites = pygame.sprite.Group()
    button1 = Button(900, 510, 'img/button2.png')
    button_sprites.add(button1)
    running = True
    while running:
        screen.fill((0, 0, 0))
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                mx, my = pygame.mouse.get_pos()
                if button1.pressed(mx, my):
                    pygame.quit()
                    quit()
        button_sprites.draw(screen)
        pygame.display.flip()
        clock.tick(FPS)


def draw_text(surf, text, size, x, y):
    font_name = pygame.font.match_font('arial')
    font = pygame.font.Font(font_name, size)
    text_surface = font.render(text, True, BLACK)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    surf.blit(text_surface, text_rect)


class Heart(pygame.sprite.Sprite):
    def __init__(self, x, y):
        self.x = x
        self.y = y
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(pygame.image.load('img/live.png').convert(), (200, 60))
        self.image.set_colorkey((70, 70, 70))
        self.rect = self.image.get_rect()
        self.rect.topleft = self.x, self.y
        self.image.set_colorkey(BLACK)

    def pressed(self, mx, my):
        if mx > self.rect.topleft[0] and my > self.rect.topleft[1]:
            if mx < self.rect.bottomright[0] and my < self.rect.bottomright[1]:
                return True


class Shield(pygame.sprite.Sprite):
    def __init__(self, x, y):
        self.x = x
        self.y = y
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(pygame.image.load('img/shield_iqon.jpg').convert(), (80, 50))
        self.rect = self.image.get_rect()
        self.image.set_colorkey((70, 70, 70))
        self.rect.topleft = self.x, self.y
        self.image.set_colorkey(BLACK)

    def pressed(self, mx, my):
        if mx > self.rect.topleft[0] and my > self.rect.topleft[1]:
            if mx < self.rect.bottomright[0] and my < self.rect.bottomright[1]:
                return True


class Sword(pygame.sprite.Sprite):
    def __init__(self, x, y):
        self.x = x
        self.y = y
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(pygame.image.load('img/atack_iqon.jpg').convert(), (80, 50))
        self.image.set_colorkey((70, 70, 70))
        self.rect = self.image.get_rect()
        self.rect.topleft = self.x, self.y
        self.image.set_colorkey(BLACK)

    def pressed(self, mx, my):
        if mx > self.rect.topleft[0] and my > self.rect.topleft[1]:
            if mx < self.rect.bottomright[0] and my < self.rect.bottomright[1]:
                return True


def shop(a):
    fon = pygame.transform.scale(pygame.image.load('img/shop.png').convert(), (400, 200))
    rect = fon.get_rect()
    screen.blit(fon, (700, 400))
    rect.topleft = (700, 400)
    shops = pygame.sprite.Group()
    if a == 1:
        heart = Heart(850, 480)
        shops.add(heart)
        draw_text(screen, 'вылечиться до 100:', 18, 880, 450)
    elif a == 0:
        weapon = Drop(850, 500, 'weapon', 'gold weapon')
        armor = Drop(950, 560, 'armor', 'gold')
        draw_text(screen, 'gold weapon:', 18, 915, 500)
        draw_text(screen, '200', 20, 900, 520)
        draw_text(screen, 'gold armor:', 18, 1020, 560)
        draw_text(screen, '300', 20, 1010, 580)
        shops.add(weapon)
        shops.add(armor)
    elif a == 2:
        amulet = Drop(850, 500, 'amulet', 'lvl5')
        draw_text(screen, 'amulet_5:', 18, 915, 500)
        draw_text(screen, '150', 20, 910, 520)
        shops.add(amulet)
    run = True
    while run:
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                mx, my = pygame.mouse.get_pos()
                if mx > rect.topleft[0] and my < rect.topleft[1] or mx > rect.bottomleft[0] and my > rect.bottomleft[1]\
                        or mx > rect.topright[0] and my > rect.topright[1] or mx < rect.topleft[0]:
                    return
            if event.type == pygame.MOUSEBUTTONDOWN:
                global live
                global money
                if a == 1:
                    mx, my = pygame.mouse.get_pos()
                    if heart.pressed(mx, my) and money - (100 - live) >= 0:
                        money -= 100 - live
                        live = 100
                if a == 0:
                    mx, my = pygame.mouse.get_pos()
                    if weapon.pressed(mx, my) and money - 200 >= 0:
                        money -= 200
                        weapon1 = Drop(850, 920, 'Weapon', 'gold weapon')
                        land.add(weapon1)
                    elif armor.pressed(mx, my) and money - 300 >= 0:
                        money -= 300
                        armor1 = Drop(950, 920, 'Armor', 'gold')
                        land.add(armor1)
                if a == 2:
                    mx, my = pygame.mouse.get_pos()
                    if amulet.pressed(mx, my) and money - 150 >= 0:
                        money -= 150
                        amulet1 = Drop(850, 920, 'Amulet', 'lvl5')
                        land.add(amulet1)
        shops.draw(screen)
        pygame.display.flip()


def fight(monster, monsterhp, monsterdamage, starthp, damage, chance, dodge):
    fon = pygame.transform.scale(pygame.image.load('img/shop.png').convert(), (400, 200))
    rect = fon.get_rect()
    icons = pygame.sprite.Group()
    atack = Sword(910, 540)
    shield = Shield(810, 540)
    icons.add(atack)
    icons.add(shield)
    rect.topleft = (700, 400)
    run = True
    while run:
        screen.blit(fon, (700, 400))
        draw_text(screen, 'Принц', 22, 1020, 425)
        draw_text(screen, monster, 22, 800, 425)
        draw_text(screen, str(starthp), 22, 1020, 475)
        draw_text(screen, str(monsterhp), 22, 800, 475)
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                mx, my = pygame.mouse.get_pos()
                if atack.pressed(mx, my) or shield.pressed(mx, my):
                    if atack.pressed(mx, my):
                        if random.random() <= chance / 100:
                            monsterhp -= damage
                            if monsterhp <= 0:
                                global live
                                live = starthp
                                return True
                    elif shield.pressed(mx, my):
                        starthp += 5
                    if random.random() >= dodge / 100:
                        starthp -= monsterdamage
                        if starthp <= 0:
                            return False

        icons.draw(screen)
        pygame.display.flip()


class Drop(pygame.sprite.Sprite):
    def __init__(self, x, y, type, name):
        pygame.sprite.Sprite.__init__(self)
        con = sqlite3.connect('bd/Inventory')
        cur = con.cursor()
        result = cur.execute(f'SELECT picture FROM "{type}" WHERE name LIKE "{name}"').fetchall()
        self.name = name
        self.image = pygame.image.load(result[0][0]).convert()
        self.image = pygame.transform.scale(self.image, (60, 60))
        self.type = type
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

    def update(self):
        global weapon, armor, amulet
        keystate = pygame.key.get_pressed()
        if keystate[pygame.K_f] and self.rect.centerx - 35 <= player.rect.centerx <= self.rect.centerx + 35:
            if self.rect.centery == 920:
                if self.type == 'Weapon':
                    weapon.name = self.name
                elif self.type == 'Armor':
                    armor.name = self.name
                elif self.type == 'Amulet':
                    amulet.name = self.name
                    print(amulet.name)
                self.kill()

    def pressed(self, mx, my):
        if mx > self.rect.topleft[0] and my > self.rect.topleft[1]:
            if mx < self.rect.bottomright[0] and my < self.rect.bottomright[1]:
                return True


class Weapon(pygame.sprite.Sprite):
    def __init__(self, name):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((80, 80))
        self.image.fill(BROWN)
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.center = (100, 100)
        self.name = name

    def update(self):
        con = sqlite3.connect('bd/Inventory')
        cur = con.cursor()
        if self.name:
            result = cur.execute(f'SELECT * FROM Weapon WHERE name LIKE "{self.name}"').fetchall()
            self.image = pygame.image.load(f'{result[0][2]}').convert()
            player.damage = result[0][0]
            player.chance = result[0][1]


class Armor(pygame.sprite.Sprite):
    def __init__(self, name=''):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((80, 80))
        self.image.fill(BROWN)
        self.image.set_colorkey(WHITE)
        self.rect = self.image.get_rect()
        self.rect.center = (200, 100)
        self.name = name

    def update(self):
        con = sqlite3.connect('bd/Inventory')
        cur = con.cursor()
        if self.name:
            result = cur.execute(f'SELECT * FROM Armor WHERE name LIKE "{self.name}"').fetchall()
            self.image = pygame.image.load(f'{result[0][1]}').convert()
            self.image = pygame.transform.scale(self.image, (80, 80))
            self.image.set_colorkey(WHITE)
            player.dodge = result[0][0]


class Amulet(pygame.sprite.Sprite):
    def __init__(self, name=''):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((80, 80))
        self.image.fill(BROWN)
        self.image.set_colorkey(MEBEL)
        self.rect = self.image.get_rect()
        self.rect.center = (300, 100)
        self.name = name

    def update(self):
        con = sqlite3.connect('bd/Inventory')
        cur = con.cursor()
        if self.name:
            result = cur.execute(f'SELECT * FROM Amulet WHERE name LIKE "{self.name}"').fetchall()
            self.image = pygame.image.load(f'{result[0][1]}').convert()
            self.image = pygame.transform.scale(self.image, (80, 80))
            player.dop_chance = result[0][0]


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
        self.weapon = 'bronze weapon'
        self.dodge = 0
        self.chance = 30
        self.damage = 30
        self.dop_chance = 0

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
        self.inv = invert

    def update(self):
        global LEFT, RIGHT
        if self.inv:
            if self.rect.centerx - 320 >= player.rect.centerx:
                LEFT = False
                RIGHT = True
        else:
            if self.rect.centerx + 320 <= player.rect.centerx:
                RIGHT = False
                LEFT = True


class Yachik(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        global yachik_imgs
        yachik_img = random.choice(yachik_imgs)
        yachik_img = pygame.transform.scale(yachik_img, (125, 90))
        self.image = yachik_img
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)


class Bochka(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        global bochka_img
        bochka_img = pygame.transform.scale(bochka_img, (75, 70))
        self.image = bochka_img
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)


class Chest(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        global chest_imgs, ARMOR, WEAPON, AMULET
        chest_img = random.choice(chest_imgs)
        yachik_img = pygame.transform.scale(chest_img, (75, 40))
        self.y = y
        self.image = yachik_img
        if chest_img == chest_imgs[0]:
            self.drop = random.choice(WEAPON)
            self.type = 'Weapon'
        elif chest_img == chest_imgs[1]:
            self.drop = random.choice(ARMOR)
            self.type = 'Armor'
        else:
            self.drop = random.choice(AMULET)
            self.type = 'Amulet'
        self.image.set_colorkey(MEBEL)
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

    def update(self):
        keystate = pygame.key.get_pressed()
        if keystate[pygame.K_e] and self.rect.centerx - 35 <= player.rect.centerx <= self.rect.centerx + 35:
            if self.rect.centery == 920:
                drop = Drop(self.rect.centerx, self.rect.centery, self.type, self.drop)
                all_bashnya.add(drop)
                self.kill()


class Door(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        global door_image
        door_image = door_image
        door_image = pygame.transform.scale(door_image, (80, 130))
        self.image = door_image
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.y = y


class Boss(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        global boss_imgs
        self.index = 0
        self.image = pygame.transform.scale(boss_imgs[0], (400, 360))
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.damage = 14
        self.name = 'хранитель башни'
        self.hp = 300

    def update(self):
        self.index += 1
        if self.index >= len(boss_imgs):
            self.index = 0
        self.image = pygame.transform.scale(boss_imgs[self.index], (400, 300))
        self.image.set_colorkey(BLACK)
        if self.rect.centerx - 30 <= player.rect.centerx <= self.rect.centerx + 30:
            if self.rect.centery == 835:
                global live
                if fight(self.name, self.hp, self.damage,
                         live, player.damage, player.chance + player.dop_chance, player.dodge):
                    win_screen()
                else:
                    death_screen()


class Monsters(pygame.sprite.Sprite):
    def __init__(self, sheet, columns, rows, x, y, name):
        pygame.sprite.Sprite.__init__(self)
        self.frames = []
        self.cut_sheet(sheet, columns, rows)
        self.cur_frame = 0
        self.image = pygame.transform.scale(self.frames[self.cur_frame], (400, 400))
        self.rect = self.image.get_rect()
        self.rect.topleft = x, y
        self.image.set_colorkey(BLACK)
        if name == 'Sans':
            self.name = 'Sans'
            self.hp = 200
            self.damage = 10
        elif name == 'Гоблин Рикардо':
            self.name = 'Гоблин Рикардо'
            self.hp = 100
            self.damage = 9
        elif name == 'Одноглаз':
            self.name = 'Одноглаз'
            self.hp = 100
            self.damage = 8
        elif name == 'Грыб':
            self.name = 'Грыб'
            self.hp = 80
            self.damage = 8

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
        self.image = pygame.transform.scale(self.frames[self.cur_frame], (400, 400))
        self.image.set_colorkey(BLACK)
        if self.rect.centerx - 30 <= player.rect.centerx <= self.rect.centerx + 30:
            if self.rect.centery == 870:
                global live, money
                if fight(self.name, self.hp, self.damage,
                         live, player.damage, player.chance + player.dop_chance, player.dodge):
                    money += random.randint(1, 15)
                    self.kill()
                else:
                    death_screen()


class Health(pygame.sprite.Sprite):
    def __init__(self, x, y, img):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(img, (200, 45))
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

    def update(self):
        self.rect.centerx = player.rect.centerx + 870
        self.rect.centery = player.rect.centery - 750
        self.image.set_colorkey(BLACK)


class Coins(pygame.sprite.Sprite):
    def __init__(self, x, y, img):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(img, (70, 60))
        self.image.set_colorkey(WHITE)
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

    def update(self):
        self.rect.centerx = player.rect.centerx + 800
        self.rect.centery = player.rect.centery - 800
        self.image.set_colorkey(WHITE)


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
yachik_imgs = [pygame.image.load('img/yachik2.jpg').convert(), pygame.image.load('img/yachik3.jpg').convert(),
               pygame.image.load('img/yachik4.jpg').convert()]
chest_imgs = [pygame.image.load('img/sword_chest.jpg').convert(),
              pygame.image.load('img/armor_chest.jpg').convert(),
              pygame.image.load('img/amulet_chest.jpg').convert()]
dirt_image = pygame.image.load('img/dirt.png').convert()
words_imgs = [pygame.image.load('img/word.png').convert(),
              pygame.image.load('img/word1.png').convert(), pygame.image.load('img/word2.png').convert()]
boss_imgs = [pygame.image.load('img/boss1.png').convert(), pygame.image.load('img/boss2.png').convert(),
             pygame.image.load('img/boss3.png').convert(), pygame.image.load('img/boss4.png').convert(),
             pygame.image.load('img/boss5.png').convert(), pygame.image.load('img/boss6.png').convert(),
             pygame.image.load('img/boss7.png').convert(), pygame.image.load('img/boss8.png').convert(),
             pygame.image.load('img/boss9.png').convert(), pygame.image.load('img/boss10.png').convert()]
bochka_img = pygame.image.load('img/bochka.jpg').convert()
bash_image = pygame.image.load('img/basn.png').convert()
oven_imgs = [pygame.image.load('img/p2.png').convert(),
             pygame.image.load('img/p3.png').convert(), pygame.image.load('img/p4.png').convert()]
bash_image = pygame.image.load('img/basn.png').convert()
etaj_image = pygame.image.load('img/etaj.jpg').convert()
etaj_image2 = pygame.image.load('img/etaj_pravo.jpg').convert()
door_image = pygame.image.load('img/door.png').convert()
all_sprites = pygame.sprite.Group()
oven_sprites = pygame.sprite.Group()
land = pygame.sprite.Group()
clock = pygame.time.Clock()
inventory_sprites = pygame.sprite.Group()
seller_sprites = pygame.sprite.Group()
seller = Seller(pygame.image.load('img/man2.png').convert(), 4, 1, 1100, 780)
seller1 = Seller(pygame.image.load('img/man1.png').convert(), 4, 1, 1900, 780)
seller2 = Seller(pygame.image.load('img/woman.png').convert(), 4, 1, 900, 780)
seller_sprites.add(seller)
seller_sprites.add(seller1)
seller_sprites.add(seller2)
monsters = pygame.sprite.Group()
oven = Oven(1050, 860)
oven_sprites.add(oven)
all_bashnya = pygame.sprite.Group()
camera = Camera()
bashnya = Bashnya(1500, 450)
for i in range(25):
    dirt = Float(100 * i, 1050)
    land.add(dirt)
for i in range(0, 6):
    monster = Monsters(pygame.image.load('img/Idle.png').convert(), 4, 1, 200 + 500, 270 - 400 * i, 'Грыб')
    monsters.add(monster)
for i in range(6, 12):
    monster = Monsters(pygame.image.load('img/Flight.png').convert(), 8, 1, 200 + 500, 270 - 400 * i, 'Одноглаз')
    monsters.add(monster)
for i in range(12, 18):
    monster = Monsters(pygame.image.load('img/goblin.png').convert(), 4, 1, 200 + 500, 270 - 400 * i, 'Гоблин Рикардо')
    monsters.add(monster)
for i in range(18, 24):
    monster = Monsters(pygame.image.load('img/skelet.png').convert(), 4, 1, 200 + 500, 270 - 400 * i, 'Sans')
    monsters.add(monster)
weapon = Weapon('bronze weapon')
inventory_sprites.add(weapon)
armor = Armor()
inventory_sprites.add(armor)
amulet = Amulet()
inventory_sprites.add(amulet)
boss = Boss(800, -9165)
monsters.add(boss)
player = Player(200, 900)
land.add(bashnya)
start_screen()
for i in range(-9190, 811, 400):
    centr = Etaj(900, i)
    prav_komnata = Room(1650, i)
    x = 1650
    y = i
    all_bashnya.add(prav_komnata)
    if random.choice([False, True, False]):
        chest = Chest(x + 170, y + 110)
        all_bashnya.add(chest)
    if random.choice([False, True]):
        bochka = Bochka(x + 90, y + 96)
        all_bashnya.add(bochka)
    if random.choice([False, True]):
        yachik = Yachik(x, y + 95)
        all_bashnya.add(yachik)
    if random.choice([False, True]):
        yachik2 = Yachik(x - 115, y + 95)
        all_bashnya.add(yachik2)
    lev_komnata = Room(150, i, True)
    all_bashnya.add(lev_komnata)
    x = 150
    if random.choice([False, True, False]):
        chest = Chest(x - 170, y + 110)
        all_bashnya.add(chest)
    if random.choice([False, True]):
        bochka = Bochka(x - 90, y + 96)
        all_bashnya.add(bochka)
    if random.choice([False, True]):
        yachik = Yachik(x, y + 95)
        all_bashnya.add(yachik)
    if random.choice([False, True]):
        yachik2 = Yachik(x + 115, y + 95)
        all_bashnya.add(yachik2)
    door = Door(900, i + 66)
    all_bashnya.add(centr)
    all_bashnya.add(door)
coin = Coins(1000, 0, pygame.image.load('img/money.png').convert())
health = Health(800, 100, pygame.image.load('img/live.png').convert())
all_sprites.add(player)
all_sprites.add(coin)
all_sprites.add(health)
live = 1000000
money = 100

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
                    word = Words(seller.rect.centerx, seller.rect.centery - 60)
                    seller_sprites.add(word)
                    if word.pressed(pygame.mouse.get_pos()):
                        shop(a)
                elif seller1.pressed(pygame.mouse.get_pos()):
                    a = 1
                    word1 = Words(seller1.rect.centerx, seller1.rect.centery - 60)
                    seller_sprites.add(word1)
                    if word1.pressed(pygame.mouse.get_pos()):
                        shop(a)
                elif seller2.pressed(pygame.mouse.get_pos()):
                    a = 2
                    word2 = Words(seller2.rect.centerx, seller2.rect.centery - 60)
                    seller_sprites.add(word2)
                    if word2.pressed(pygame.mouse.get_pos()):
                        shop(a)

        # Обновление
        all_sprites.update()
        land.update()
        inventory_sprites.update()
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
        inventory_sprites.draw(screen)
        draw_text(screen, str(money), 18, 1800, 85)
        draw_text(screen, str(live), 18, 1800, 135)
    else:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                keystate = pygame.key.get_pressed()
                if keystate[pygame.K_UP] and door.rect.centerx - 20 <= player.rect.centerx <= door.rect.centerx + 20:
                    player.rect.centery -= 400
                elif keystate[pygame.K_DOWN]:
                    if door.rect.centerx - 20 <= player.rect.centerx <= door.rect.centerx + 20:
                        if door.rect.centery == 876 and door.y == 876:
                            v_bashne = False
                        else:
                            player.rect.centery += 400
            elif event.type == pygame.USEREVENT + 5:
                monsters.update()
        all_sprites.update()
        all_bashnya.update()
        inventory_sprites.update()
        # Рендеринг
        screen.blit(background, background_rect)
        camera.update(player)
        for sprite in all_sprites:
            camera.apply(sprite)
        for sprite in all_bashnya:
            camera.apply(sprite)
        for sprite in monsters:
            camera.apply(sprite)
        all_bashnya.draw(screen)
        monsters.draw(screen)
        all_sprites.draw(screen)
        inventory_sprites.draw(screen)
        draw_text(screen, str(money), 18, 1800, 85)
        draw_text(screen, str(live), 18, 1800, 135)
    pygame.display.flip()
pygame.quit()
