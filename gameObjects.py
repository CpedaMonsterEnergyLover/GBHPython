from random import choice, randint

import pygame.draw

from colors import *

CARD_WIDTH = 2 * 40
CARD_HEIGHT = 3 * 40
PADDING = 5
TOKEN_WIDTH = CARD_WIDTH / 2 - PADDING * 1.2

T_HALF = (TOKEN_WIDTH - PADDING) / 2
TOKEN_POSITIONS = [
    # 1 hero
    [(CARD_WIDTH / 2 - T_HALF, CARD_HEIGHT / 4 * 3 - T_HALF)],
    # 2 heroes
    [(CARD_WIDTH / 4 - T_HALF, CARD_HEIGHT / 4 * 3 - T_HALF),
     (CARD_WIDTH / 4 * 3 - T_HALF, CARD_HEIGHT / 4 * 3 - T_HALF)],
    # 3 heroes
    [(CARD_WIDTH / 4 - T_HALF, CARD_HEIGHT / 6 * 5 - T_HALF),
     (CARD_WIDTH / 4 * 3 - T_HALF, CARD_HEIGHT / 6 * 5 - T_HALF),
     (CARD_WIDTH / 2 - T_HALF, CARD_HEIGHT / 5 * 2.9 - T_HALF)],
    # 4 heroes
    [(CARD_WIDTH / 4 - T_HALF, CARD_HEIGHT / 6 * 5 - T_HALF),
     (CARD_WIDTH / 4 * 3 - T_HALF, CARD_HEIGHT / 6 * 5 - T_HALF),
     (CARD_WIDTH / 4 * 3 - T_HALF, CARD_HEIGHT / 5 * 2.9 - T_HALF),
     (CARD_WIDTH / 4 - T_HALF, CARD_HEIGHT / 5 * 2.9 - T_HALF)]
]

class Hero(pygame.sprite.Sprite):
    color = None
    collider = None

    def __init__(self, color):
        super().__init__()
        self.color = color
        self.surf = pygame.Surface((TOKEN_WIDTH, TOKEN_WIDTH))
        self.rect = self.surf.get_rect()
        self.border()

    def draw(self, surface, slots, i):
        print(slots, i)
        self.move(TOKEN_POSITIONS[slots - 1][i][0], TOKEN_POSITIONS[slots - 1][i][1])
        self.collider = surface.blit(self.surf, self.rect)

    def border(self):
        pygame.draw.circle(self.surf, self.color, (TOKEN_WIDTH / 2, TOKEN_WIDTH / 2), TOKEN_WIDTH / 2)
        pygame.draw.circle(self.surf, RED, (TOKEN_WIDTH / 2, TOKEN_WIDTH / 2), TOKEN_WIDTH / 2, 2)
        self.surf.set_colorkey(BLACK)

    def move(self, x, y):
        self.rect.move_ip(x, y)


class Card(pygame.sprite.Sprite):
    opened = None
    color = None
    is_location = None
    collider = None
    heroes = None

    def __init__(self):
        super().__init__()
        self.surf = pygame.Surface((CARD_WIDTH, CARD_HEIGHT))
        self.rect = self.surf.get_rect()
        self.surf.fill(GREY)
        self.border()
        self.heroes = []

    def draw(self, surface):
        self.collider = surface.blit(self.surf, self.rect)
        slots = len(self.heroes)
        for i in range(slots):
            if self.heroes[i]:
                self.heroes[i].draw(surface, slots, i)

    def border(self):
        pygame.draw.rect(self.surf, BLACK, (0, 0, CARD_WIDTH, CARD_HEIGHT), 2)

    def move(self, x, y):
        self.rect.move_ip(x, y)
        for hero in self.heroes:
            hero.move(x, y)

    def set_color(self, col):
        self.color = col

    def open(self):
        self.opened = True
        self.surf.fill(self.color)
        self.border()

    def get_collided_hero(self, point):
        collided = None
        for hero in self.heroes:
            if hero:
                if hero.rect.collidepoint(point):
                    collided = hero
        return collided


class Field(pygame.sprite.Sprite):
    width = 0
    height = 0
    cells = None
    story_cards = 0
    collider = None

    def __init__(self, width, height, story):
        super().__init__()
        self.surf = pygame.Surface((CARD_WIDTH * width + width, CARD_HEIGHT * height + height))
        self.rect = self.surf.get_rect()
        self.surf.fill(WHITE)
        self.width = width
        self.height = height
        self.cells = [[Card() for y in range(width)] for x in range(height)]
        self.story_cards = story
        for x in range(self.width):
            for y in range(self.height):
                cell = self.get_cell(x, y)
                cell.move(x * CARD_WIDTH + 2, y * CARD_HEIGHT + 2)

    def get_cell(self, x, y):
        return self.cells[x][y] or None

    def print(self):
        print(self.cells)

    def place_story_cards(self):
        for i in range(self.story_cards):
            while True:
                x = randint(0, self.width - 1)
                y = randint(0, self.height - 1)
                cell = self.get_cell(x, y)
                if cell.color is None:
                    cell.set_color(PINK)
                    if i == 0:
                        cell.open()
                    break
                else:
                    continue

    def generate(self):
        for x in range(self.width):
            for y in range(self.height):
                cell = self.get_cell(x, y)
                if cell.color is None:
                    cell.set_color(choose_card())

    def draw(self, surface):
        self.collider = surface.blit(self.surf, self.rect)
        for row in self.cells:
            for cell in row:
                cell.draw(surface)

    def open_all(self):
        for row in self.cells:
            for cell in row:
                cell.open()

    def move(self, x, y):
        self.rect.move_ip(x, y)
        for row in self.cells:
            for cell in row:
                cell.move(x, y)

    def collide(self, point):
        return self.rect.collidepoint(point)

    def get_collided_cell(self, point):
        collided = None
        for row in self.cells:
            for cell in row:
                if cell.rect.collidepoint(point):
                    collided = cell
        return collided

    def put_heroes(self, x, y, heroes):
        for hero in heroes:
            self.put_hero(x, y, hero)

    def put_hero(self, x, y, hero):
        hero.move(x * CARD_WIDTH, y * CARD_HEIGHT)
        self.get_cell(x, y).heroes.append(hero)

    def print_heroes(self):
        for row in self.cells:
            for cell in row:
                if cell.heroes:
                    print(cell.heroes)


def choose_card():
    """ Describes the way of non-story cards distribution """
    colors = [RED, GREEN, BLUE]
    return choice(colors)