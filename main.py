import os
import sys

import pygame
import requests


class Mapt(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.color = (255, 255, 255)
        self.bg = (100, 100, 100)
        self.pos = (x, y)
        self.font = pygame.font.Font(None, 30)
        self.text = 'Тип карты'
        self.types = ['sat', 'sat,skl', 'map']
        self.ind = 0
        self.rect_ = pygame.rect.Rect(x, y, 100, 20)

    def change_type(self):
        self.ind = (self.ind + 1) % 3

    def curr_type(self):
        return self.types[self.ind]

    def render(self, screen):
        pygame.draw.rect(screen, self.bg, self.rect_)
        screen.blit(self.font.render(self.text, True, self.color), self.pos)



r = True
r1 = True
mas = float(input())
first = input()
second = input()
map_request = f"http://static-maps.yandex.ru/1.x/?ll={first},{second}&spn={mas},{mas}&l=sat"
response = requests.get(map_request)

if not response:
    print("Ошибка выполнения запроса:")
    print(map_request)
    print("Http статус:", response.status_code, "(", response.reason, ")")
    sys.exit(1)

map_file = "map.png"
with open(map_file, "wb") as file:
    file.write(response.content)


def map_upload(first, second, mas, map):
    map_request = f"http://static-maps.yandex.ru/1.x/?ll={first},{second}&spn={mas},{mas}&l={map}"
    response = requests.get(map_request)

    if not response:
        print("Ошибка выполнения запроса:")
        print(map_request)
        print("Http статус:", response.status_code, "(", response.reason, ")")
        sys.exit(1)

    map_file = "map.png"
    with open(map_file, "wb") as file:
        file.write(response.content)


# Инициализируем pygame
pygame.init()
screen = pygame.display.set_mode((600, 450))
# Рисуем картинку, загружаемую из только что созданного файла.
screen.blit(pygame.image.load(map_file), (0, 0))
map_type_box = Mapt(10, 50)
# Переключаем экран и ждем закрытия окна.
pygame.display.flip()
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN and event.key == pygame.K_PAGEDOWN:
            if r:
                os.remove(map_file)
            if mas <= 20:
                mas += 1
            if 0 < mas < 21:
                r = True
                map_upload(first, second, mas, map_type_box.curr_type())
                screen.blit(pygame.image.load(map_file), (0, 0))
                pygame.display.flip()
            else:
                r = False
        if event.type == pygame.KEYDOWN and event.key == pygame.K_PAGEUP:
            if r:
                os.remove(map_file)
            if mas > 1:
                mas -= 1
            if 21 > mas > 0:
                map_upload(first, second, mas, map_type_box.curr_type())
                r = True
                screen.blit(pygame.image.load(map_file), (0, 0))
                pygame.display.flip()
            else:
                r = False
            pygame.display.flip()
        if event.type == pygame.KEYDOWN and event.key == pygame.K_UP:
            second = str(float(second) + mas)
            if 0 <= abs(float(second)) <= 180:
                if os.path.exists("map.txt"):
                    os.remove(map_file)
                map_upload(first, second, mas, map_type_box.curr_type())
                screen.blit(pygame.image.load(map_file), (0, 0))
                pygame.display.flip()
            else:
                second = str(float(second) - mas)
        if event.type == pygame.KEYDOWN and event.key == pygame.K_DOWN:
            second = str(float(second) - mas)
            if 0 <= abs(float(second)) <= 180:
                if os.path.exists("map.txt"):
                    os.remove(map_file)
                map_upload(first, second, mas, map_type_box.curr_type())
                screen.blit(pygame.image.load(map_file), (0, 0))
                pygame.display.flip()
            else:
               second = str(float(second) + mas)
        if event.type == pygame.KEYDOWN and event.key == pygame.K_RIGHT:
            first = str(float(first) + mas)
            if 0 <= abs(float(first)) <= 180:
                if os.path.exists("map.txt"):
                    os.remove(map_file)
                map_upload(first, second, mas, map_type_box.curr_type())
                screen.blit(pygame.image.load(map_file), (0, 0))
                pygame.display.flip()
            else:
                first = str(float(first) - mas)
        if event.type == pygame.KEYDOWN and event.key == pygame.K_LEFT:
            first = str(float(first) - mas)
            if 0 <= abs(float(first)) <= 180:
                if os.path.exists("map.txt"):
                    os.remove(map_file)
                map_upload(first, second, mas, map_type_box.curr_type())
                screen.blit(pygame.image.load(map_file), (0, 0))
                pygame.display.flip()
            else:
                first = str(float(first) + mas)
        if event.type == pygame.MOUSEBUTTONDOWN:
            pos = pygame.mouse.get_pos()
            if map_type_box.rect_.collidepoint(*pos):
                    map_type_box.change_type()
                    map_upload(first, second, mas, map_type_box.curr_type())
                    screen.blit(pygame.image.load(map_file), (0, 0))
                    pygame.display.flip()
        map_type_box.render(screen)
        pygame.display.flip()
pygame.quit()
if os.path.exists("map.txt"):
    os.remove(map_file)
