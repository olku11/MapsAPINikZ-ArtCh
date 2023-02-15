import os
import sys

import pygame
import requests

# Это все символы, которые нам нужны для ввода чего-ибудь через клаву
ALP = {'q': 'й', '`': 'ё', 'w': 'ц', 'e': 'у', 'r': 'к', 't': 'е', 'y': 'н', 'u': 'г', 'i': 'ш',
       'o': 'щ', 'p': 'з', '[': 'х', ']': 'ъ', 'a': 'ф', 's': 'ы', 'd': 'в', 'f': 'а', 'g': 'п',
       'h': 'р', 'j': 'о', 'k': 'л', 'l': 'д', ';': 'ж', "'": 'э', 'z': 'я', 'x': 'ч', 'c': 'с',
       'v': 'м', 'b': 'и', 'n': 'т', 'm': 'ь', ',': 'б', '.': 'ю'}
ALP_BIG = {}
for i in ALP:
    ALP_BIG[i.upper()] = ALP[i].upper()


# Кнопка для изменения типа карты
class Mapt(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.color = (255, 255, 255)
        self.bg = (100, 100, 100)  # Бекграунд текста
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


class Textinp(pygame.sprite.Sprite):
    def __init__(self, x, y, color, bg, width, height, size, text=''):
        super().__init__()
        self.color = color
        self.bg = bg
        self.pos = (x, y)
        self.font = pygame.font.Font(None, size)
        self.text = text
        self.rect1 = pygame.rect.Rect(x, y, width, height)

    def render(self, screen):
        screen.blit(self.font.render(self.text, True, self.color, self.bg), self.pos)
        pygame.draw.rect(screen, self.color, self.rect1.inflate(5, 5), 2)


r = True
r1 = True
mas = int(input())
first = input()
second = input()
map_request = f"http://static-maps.yandex.ru/1.x/?ll={first},{second}&z={mas}&l=sat"
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
    global metka
    pts = []
    if metka is not None:
        pts.append(f"{metka[0]},{metka[1]},pm2dgm")
        pts = "pt=" + "~".join(pts)
    if pts:
        map_request = f"http://static-maps.yandex.ru/1.x/?ll={first},{second}&z={mas}&l={map}&{pts}"
    else:
        map_request = f"http://static-maps.yandex.ru/1.x/?ll={first},{second}&z={mas}&l={map}"
    response = requests.get(map_request)

    if not response:
        print("Ошибка выполнения запроса:")
        print(map_request)
        print("Http статус:", response.status_code, "(", response.reason, ")")
        sys.exit(1)

    map_file = "map.png"
    with open(map_file, "wb") as file:
        file.write(response.content)


def get_coors(toponym_name):
    geocoder_api_server = "http://geocode-maps.yandex.ru/1.x/"
    geocoder_params = {
        "apikey": "40d1649f-0493-4b70-98ba-98533de7710b",
        "geocode": toponym_name,
        "format": "json"}
    response = requests.get(geocoder_api_server, params=geocoder_params)

    if not response:
        return [None, None], '', ''

    try:
        json_response = response.json()
        toponym = json_response["response"]["GeoObjectCollection"][
            "featureMember"][0]["GeoObject"]
        adrs = toponym['metaDataProperty']['GeocoderMetaData']['AddressDetails']['Country'][
            'AddressLine']
        index = toponym['metaDataProperty']['GeocoderMetaData']['Address'].get('postal_code', '')
        toponym_coodrinates = toponym["Point"]["pos"]
        toponym_longitude, toponym_lattitude = toponym_coodrinates.split(" ")
    except Exception:
        index = ''
        adrs = ''
        toponym_longitude, toponym_lattitude = [None, None]
    return [toponym_longitude, toponym_lattitude], adrs, index


metka = None
# Инициализируем pygame
pygame.init()
screen = pygame.display.set_mode((600, 450))
# Рисуем картинку, загружаемую из только что созданного файла.
screen.blit(pygame.image.load(map_file), (0, 0))
map_type_box = Mapt(10, 50)
text_box = Textinp(10, 400, (255, 255, 255), (0, 0, 0), 350, 30, 40)
check_box = Textinp(400, 400, (255, 255, 255), (0, 255, 0), 60, 20, 30, text='Поиск')
adres_box = Textinp(10, 10, (255, 255, 255), (0, 50, 100), 540, 20, 20)
check_box2 = Textinp(500, 400, (255, 255, 255), (255, 0, 0), 60, 20, 30, text='Сброc')
# Переключаем экран и ждем закрытия окна.
pygame.display.flip()
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN and event.key == pygame.K_PAGEUP:
            if r:
                os.remove(map_file)
            if mas <= 16:
                mas += 1
            if 2 <= mas <= 17:
                r = True
                map_upload(first, second, mas, map_type_box.curr_type())
                screen.blit(pygame.image.load(map_file), (0, 0))
                pygame.display.flip()
            else:
                r = False
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_PAGEDOWN:
            if r:
                os.remove(map_file)
            if mas >= 3:
                mas -= 1
            if 17 >= mas >= 2:
                map_upload(first, second, mas, map_type_box.curr_type())
                r = True
                screen.blit(pygame.image.load(map_file), (0, 0))
                pygame.display.flip()
            else:
                r = False
            pygame.display.flip()
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_UP:
            a = 450 / (8 * 2 ** (mas - 2.6675))
            second = str(float(second) + a)
            if 0 <= abs(float(second)) <= 180:
                if os.path.exists("map.txt"):
                    os.remove(map_file)
                if float(first) > 180:
                    first = str(-(180 - float(first) % 180))
                if float(first) < -180:
                    first = str(abs(float(first)) % 180)
                if float(second) > 90:
                    second = str(-(90 - float(second) % 90))
                if float(second) < -90:
                    second = str(90 - abs(float(second)) % 90)
                map_upload(first, second, mas, map_type_box.curr_type())
                screen.blit(pygame.image.load(map_file), (0, 0))
                pygame.display.flip()
            else:
                second = str(float(second) - a)
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_DOWN:
            a = 450 / (8 * 2 ** (mas - 2.6675))
            second = str(float(second) - a)
            if 0 <= abs(float(second)) <= 180:
                if os.path.exists("map.txt"):
                    os.remove(map_file)
                if float(first) > 180:
                    first = str(-(180 - float(first) % 180))
                if float(first) < -180:
                    first = str(abs(float(first)) % 180)
                if float(second) > 90:
                    second = str(-(90 - float(second) % 90))
                if float(second) < -90:
                    second = str(90 - abs(float(second)) % 90)
                map_upload(first, second, mas, map_type_box.curr_type())
                screen.blit(pygame.image.load(map_file), (0, 0))
                pygame.display.flip()
            else:
                second = str(float(second) + a)
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_RIGHT:
            a = 600 / (4.56555 * 2 ** (mas - 2.678))
            first = str(float(first) + a)
            if 0 <= abs(float(first)) <= 180:
                if os.path.exists("map.txt"):
                    os.remove(map_file)
                if float(first) > 180:
                    first = str(-(180 - float(first) % 180))
                if float(first) < -180:
                    first = str(abs(float(first)) % 180)
                if float(second) > 90:
                    second = str(-(90 - float(second) % 90))
                if float(second) < -90:
                    second = str(90 - abs(float(second)) % 90)
                map_upload(first, second, mas, map_type_box.curr_type())
                screen.blit(pygame.image.load(map_file), (0, 0))
                pygame.display.flip()
            else:
                first = str(float(first) - a)
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_LEFT:
            a = 600 / (4.56555 * 2 ** (mas - 2.678))
            first = str(float(first) - a)
            if 0 <= abs(float(first)) <= 180:
                if os.path.exists("map.txt"):
                    os.remove(map_file)
                if float(first) > 180:
                    first = str(-(180 - float(first) % 180))
                if float(first) < -180:
                    first = str(abs(float(first)) % 180)
                if float(second) > 90:
                    second = str(-(90 - float(second) % 90))
                if float(second) < -90:
                    second = str(90 - abs(float(second)) % 90)
                map_upload(first, second, mas, map_type_box.curr_type())
                screen.blit(pygame.image.load(map_file), (0, 0))
                pygame.display.flip()
            else:
                first = str(float(first) + a)
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_BACKSPACE:
                text_box.text = text_box.text[:-1]
            else:
                if event.unicode in ALP:
                    text_box.text += ALP[event.unicode]
                elif event.unicode in ALP_BIG:
                    text_box.text += ALP_BIG[event.unicode]
                else:
                    text_box.text += event.unicode
        if event.type == pygame.KEYDOWN:
            map_upload(first, second, mas, map_type_box.curr_type())

        if event.type == pygame.MOUSEBUTTONDOWN:
            pos = pygame.mouse.get_pos()
            if map_type_box.rect_.collidepoint(*pos):
                map_type_box.change_type()
                map_upload(first, second, mas, map_type_box.curr_type())
                screen.blit(pygame.image.load(map_file), (0, 0))
                pygame.display.flip()
            elif check_box.rect1.collidepoint(*pos):
                print(1)
                if text_box.text != '':
                    res = get_coors(text_box.text)
                    print(res)
                    if res[0][0] is None:
                        continue
                    adres_box.text = res[2] + ' ' + res[1]
                    metka = get_coors(adres_box.text)[0]
                    reset = False
                    first, second = res[0]
                    map_upload(first, second, mas, map_type_box.curr_type())
            elif check_box2.rect1.collidepoint(*pos):
                reset = True
                metka = None
                text_box.text = ''
                adres_box.text = ''
                map_upload(first, second, mas, map_type_box.curr_type())
        screen.blit(pygame.image.load("map.png"), (0, 0))
        map_type_box.render(screen)
        text_box.render(screen)
        check_box.render(screen)
        adres_box.render(screen)
        check_box2.render(screen)
        pygame.display.flip()
pygame.quit()
if os.path.exists("map.txt"):
    os.remove(map_file)
