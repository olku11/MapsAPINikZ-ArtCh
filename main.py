import os
import sys

import pygame
import requests

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


def map_upload(first, second, mas):
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


# Инициализируем pygame
pygame.init()
screen = pygame.display.set_mode((600, 450))
# Рисуем картинку, загружаемую из только что созданного файла.
screen.blit(pygame.image.load(map_file), (0, 0))
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
                map_upload(first, second, mas)
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
                map_upload(first, second, mas)
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
                map_upload(first, second, mas)
                screen.blit(pygame.image.load(map_file), (0, 0))
                pygame.display.flip()
            else:
                second = str(float(second) - mas)
        if event.type == pygame.KEYDOWN and event.key == pygame.K_DOWN:
            second = str(float(second) - mas)
            if 0 <= abs(float(second)) <= 180:
                if os.path.exists("map.txt"):
                    os.remove(map_file)
                map_upload(first, second, mas)
                screen.blit(pygame.image.load(map_file), (0, 0))
                pygame.display.flip()
            else:
               second = str(float(second) + mas)
        if event.type == pygame.KEYDOWN and event.key == pygame.K_RIGHT:
            first = str(float(first) + mas)
            if 0 <= abs(float(first)) <= 180:
                if os.path.exists("map.txt"):
                    os.remove(map_file)
                map_upload(first, second, mas)
                screen.blit(pygame.image.load(map_file), (0, 0))
                pygame.display.flip()
            else:
                first = str(float(first) - mas)
        if event.type == pygame.KEYDOWN and event.key == pygame.K_LEFT:
            first = str(float(first) - mas)
            if 0 <= abs(float(first)) <= 180:
                if os.path.exists("map.txt"):
                    os.remove(map_file)
                map_upload(first, second, mas)
                screen.blit(pygame.image.load(map_file), (0, 0))
                pygame.display.flip()
            else:
                first = str(float(first) + mas)

pygame.quit()
