import pygame
import sys
from sorting_algorithms import *


pygame.init()

# VISUALIZER WINDOW DIMENSIONS
VISUALIZER_WIDTH = 1024
VISUALIZER_HEIGHT = 800


# COLOURS
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)

# BARS
INSPECTED_COLOUR = BLUE
COMPARED_COLOUR = RED
BASE_COLOUR = GREEN


# BUTTONS
BUTTON_WIDTH = VISUALIZER_WIDTH // 3
BUTTON_HEIGHT = 100
BUTTON_SPACING = 0
BUTTONS_FONT_SIZE = 24
BUTTONS_FONT = pygame.font.Font("assets\\Ticketing.ttf", BUTTONS_FONT_SIZE)
BUTTONS_FONTS = "assets\\Ticketing.ttf"
BORDER_WIDTH = BUTTON_WIDTH // BUTTON_HEIGHT
# MENU
MENU_HEIGHT = BUTTON_HEIGHT * 2


# WINDOW
WINDOW_HEIGHT = VISUALIZER_HEIGHT + MENU_HEIGHT
WIN = pygame.display.set_mode((VISUALIZER_WIDTH, WINDOW_HEIGHT))
FPS = 200
VISUALIZER_RECT = pygame.Rect(0, MENU_HEIGHT, VISUALIZER_WIDTH, VISUALIZER_HEIGHT)
pygame.display.set_caption("Sorting visualizer")


class Button:

    def __init__(self, name, button_number, colour=BLACK, secondary_colour=GREEN, text=None,
                 font=BUTTONS_FONTS, font_size=BUTTONS_FONT_SIZE, button_total=3):
        self.name = name
        self.colour = colour
        self.current_colour = colour
        self.secondary_colour = secondary_colour
        self.button_number = button_number
        self.text = text
        self.font = pygame.font.Font(font, font_size)
        self.button_total = button_total
        self.column = button_number % button_total
        self.row = button_number // button_total
        self.placement_and_size = (self.column * BUTTON_WIDTH, self.row * BUTTON_HEIGHT,
                                   BUTTON_WIDTH, BUTTON_HEIGHT)
        self.rect = pygame.Rect(self.placement_and_size)

    def draw(self, surface):
        self.mouseover()
        pygame.draw.rect(surface, self.current_colour, self.rect, BORDER_WIDTH)

        if self.text:
            text_obj = self.font.render(self.text, True, self.current_colour)
            text_rect = text_obj.get_rect()
            text_rect.center = (((self.column + 0.5) * BUTTON_WIDTH), ((self.row + 0.5) * BUTTON_HEIGHT))
            surface.blit(text_obj, text_rect)

    def mouseover(self):
        pos = pygame.mouse.get_pos()
        if self.rect.collidepoint(*pos):
            self.current_colour = self.secondary_colour

    def mouse_click(self, algorithm):
        pos = pygame.mouse.get_pos()
        if self.rect.collidepoint(*pos):
            # print(self.name)
            return eval(self.name)
        return algorithm


def check_events(array, algorithm, click):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit(0)
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                pygame.quit()
                sys.exit(0)
            elif event.key == pygame.K_r:
                array = algorithm.generate_array()
            elif event.key == pygame.K_RETURN:
                algorithm.algorithm()
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                click = True
    return array, click


def draw_bars(array, inspected=None, compared_1=None, compared_2=None):
    pygame.draw.rect(WIN, WHITE, VISUALIZER_RECT)
    pos_x = VISUALIZER_WIDTH // len(array)
    for i in range(len(array)):
        if array[i] == inspected:
            pygame.draw.line(WIN, INSPECTED_COLOUR,
                             (pos_x * i, WINDOW_HEIGHT),
                             (pos_x * i, WINDOW_HEIGHT - array[i] * VISUALIZER_HEIGHT // max(array)),
                             VISUALIZER_WIDTH // len(array))
            inspected = None
        elif array[i] == compared_1:
            pygame.draw.line(WIN, COMPARED_COLOUR,
                             (pos_x * i, WINDOW_HEIGHT),
                             (pos_x * i, WINDOW_HEIGHT - array[i] * VISUALIZER_HEIGHT // max(array)),
                             VISUALIZER_WIDTH // len(array))
            compared_1 = None
        elif array[i] == compared_2:
            pygame.draw.line(WIN, COMPARED_COLOUR,
                             (pos_x * i, WINDOW_HEIGHT),
                             (pos_x * i, WINDOW_HEIGHT - array[i] * VISUALIZER_HEIGHT // max(array)),
                             VISUALIZER_WIDTH // len(array))
            compared_1 = None
        else:
            pygame.draw.line(WIN, BASE_COLOUR,
                             (pos_x * i, WINDOW_HEIGHT),
                             (pos_x * i, WINDOW_HEIGHT - array[i] * VISUALIZER_HEIGHT // max(array)),
                             VISUALIZER_WIDTH // len(array))


def update(array, inspected=None, compared_1=None, compared_2=None, elapsed_time=None):
    # pygame.time.wait(1)
    draw_bars(array, inspected, compared_1, compared_2)
    pygame.display.set_caption(f"Sorting visualizer     {elapsed_time}")
    pygame.display.update()


def get_all_algorithms(cls):
    all_algorithms = [(f"{subclass.__name__}()", f"{subclass.__name__[:-4]} Sort") for subclass in cls.__subclasses__()]
    return all_algorithms


def main():
    run = True
    clock = pygame.time.Clock()
    all_algorithms = get_all_algorithms(Algorithm)
    algo = Algorithm("algo")
    click = False
    buttons = []
    while run:
        clock.tick(FPS)
        WIN.fill(WHITE)

        for index, algorithm in enumerate(all_algorithms):
            button = Button(algorithm[0], index, text=algorithm[1])
            button.draw(WIN)
            buttons.append(button)
            if click:
                algo = button.mouse_click(algo)

        click = False
        algo.array, click = check_events(algo.array, algo, click)
        draw_bars(algo.array)

        pygame.display.update()


if __name__ == '__main__':
    main()
