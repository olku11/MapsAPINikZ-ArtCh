import os
import sys
import pygame
import requests

mas = input()
map_request = f"http://static-maps.yandex.ru/1.x/?ll={input()},{input()}&spn={mas},{mas}&l=sat"
response = requests.get(map_request)

if not response:
    print("Ошибка выполнения запроса:")
    print(map_request)
    print("Http статус:", response.status_code, "(", response.reason, ")")
    sys.exit(1)

map_file = "map.png"
with open(map_file, "wb") as file:
    file.write(response.content)

# Инициализируем pygamepygame.init()
screen = pygame.display.set_mode((600, 450))
# Рисуем картинку, загружаемую из только что созданного файла.screen.blit(pygame.image.load(map_file), (0, 0))
# Переключаем экран и ждем закрытия окна.pygame.display.flip()
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            pass
pygame.quit()
os.remove(map_file)
# Удаляем за собой файл с изображением.os.remove(map_file)