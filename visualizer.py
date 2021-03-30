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
            return eval(self.name)
        return algorithm


def check_events(algorithm, click):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit(0)
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                pygame.quit()
                sys.exit(0)
            elif event.key == pygame.K_r:
                algorithm.generate_array()
            elif event.key == pygame.K_RETURN:
                algorithm.algorithm()
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                click = True
    return click


def draw_one_bar(i, bar_width, array, mode=None):
    # offset = VISUALIZER_WIDTH // len(array) // 2
    if mode == "inspected":
        colour = INSPECTED_COLOUR
    elif mode == "compared":
        colour = COMPARED_COLOUR
    else:
        colour = BASE_COLOUR

    pygame.draw.line(WIN, WHITE,
                     (bar_width * (i + 0.5), WINDOW_HEIGHT),
                     (bar_width * (i + 0.5), MENU_HEIGHT + 0.5 * BORDER_WIDTH),
                     bar_width + 1)
    pygame.draw.line(WIN, colour,
                     (bar_width * (i + 0.5), WINDOW_HEIGHT),
                     (bar_width * (i + 0.5), WINDOW_HEIGHT - array[i] * VISUALIZER_HEIGHT // VISUALIZER_WIDTH),
                     bar_width + 1)


def draw_bars(array, bar_width, start=0, end=1024, inspected=None, compared=(None, None)):
    for i in range(start, end):
        if i == inspected:
            mode = "inspected"
        elif i in compared:
            mode = "compared"
        else:
            mode = "base"
        draw_one_bar(i, bar_width, array, mode)


def update(array, bar_width, start, end, inspected, compared, elapsed_time=None):
    draw_bars(array, bar_width, start, end, inspected, compared)
    pygame.display.set_caption(f"Sorting visualizer     {elapsed_time}")
    pygame.display.update((bar_width * start, MENU_HEIGHT, bar_width * (end - start), VISUALIZER_HEIGHT))
    # pygame.time.delay(100)


def update_one_bar(bar, array, bar_width, mode=None, elapsed_time=None):
    draw_one_bar(bar, bar_width, array, mode)
    # pygame.display.set_caption(f"Sorting visualizer     {elapsed_time}")
    pygame.display.update((bar_width * bar, MENU_HEIGHT, bar_width, VISUALIZER_HEIGHT))
    pygame.time.delay(25)


def get_all_algorithms(cls):
    all_algorithms = [(f"{subclass.__name__}()", f"{subclass.__name__[:-4]} Sort") for subclass in cls.__subclasses__()]
    return all_algorithms


def main():
    clock = pygame.time.Clock()
    all_algorithms = get_all_algorithms(Algorithm)
    algo = Algorithm("algo")
    click = False
    buttons = []
    bar_width = VISUALIZER_WIDTH // algo.array_length
    while True:
        clock.tick(FPS)
        WIN.fill(WHITE)

        for index, algorithm in enumerate(all_algorithms):
            button = Button(algorithm[0], index, text=algorithm[1])
            button.draw(WIN)
            buttons.append(button)
            if click:
                algo = button.mouse_click(algo)
        click = False
        click = check_events(algo, click)
        draw_bars(algo.array, bar_width, 0, algo.array_length)
        pygame.display.update()


if __name__ == '__main__':
    main()
