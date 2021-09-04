import pygame

from gameObjects import *



if __name__ == '__main__':
    pygame.init()
    pygame.display.set_caption("A game")

    # Assigns FPS a value
    FPS = 60
    FramePerSec = pygame.time.Clock()

    # Screen settings
    # flags = pygame.FULLSCREEN |
    info = pygame.display.Info()
    screen_height = info.current_h - 100
    screen_width = info.current_w - 100
    screen = pygame.display.set_mode((screen_width, screen_height))
    screen.fill(BLACK)

    gameField = Field(5, 5, story=2)
    gameField.place_story_cards()
    gameField.generate()

    heroes = [Hero(HERO1)]
    gameField.put_heroes(0, 0, heroes)
    heroes = [Hero(HERO1), Hero(HERO2)]
    gameField.put_heroes(1, 0, heroes)
    heroes = [Hero(HERO1), Hero(HERO2), Hero(HERO3)]
    gameField.put_heroes(2, 0, heroes)
    heroes = [Hero(HERO1), Hero(HERO2), Hero(HERO3), Hero(HERO4)]
    gameField.put_heroes(3, 0, heroes)

    gameField.move((screen_width - gameField.rect.width) / 2,
                    (screen_height - gameField.rect.height) / 2)
    gameField.draw(screen)

    running = True
    while running:
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                click = pygame.mouse.get_pos()
                if gameField.collide(click):
                    cell = gameField.get_collided_cell(click)
                    if cell:
                        print(cell.get_collided_hero(click))
                        # cell.open()
                        # cell.draw(screen)
            elif event.type == pygame.QUIT:
                running = False

        FramePerSec.tick(FPS)
