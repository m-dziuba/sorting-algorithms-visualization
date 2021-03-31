import pygame
import sys
from config import *
from sorting_algorithms import *


pygame.init()
WIN = pygame.display.set_mode((VISUALIZER_WIDTH, WINDOW_HEIGHT))
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
        self.draw()

    def draw(self):
        self.mouseover()
        pygame.draw.rect(WIN, self.current_colour, self.rect, BORDER_WIDTH)

        if self.text:
            text_obj = self.font.render(self.text, True, self.current_colour)
            text_rect = text_obj.get_rect()
            text_rect.center = (((self.column + 0.5) * BUTTON_WIDTH), ((self.row + 0.5) * BUTTON_HEIGHT))
            WIN.blit(text_obj, text_rect)

    def mouseover(self):
        pos = pygame.mouse.get_pos()
        if self.rect.collidepoint(*pos):
            self.current_colour = self.secondary_colour

    def mouse_click(self):
        pos = pygame.mouse.get_pos()
        if self.rect.collidepoint(*pos):
            return eval(self.name)

    def menu_mouse_click(self):
        pos = pygame.mouse.get_pos()
        if self.rect.collidepoint(*pos):
            return True


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
                pygame.display.set_caption(f"Sorting visualizer         {algorithm.time_elapsed}")
                algorithm.algorithm()
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                click = True
    return click


def draw_one_bar(i, bar_width, array, mode=None):
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


def update(array, bar_width, start, end, inspected, compared):
    draw_bars(array, bar_width, start, end, inspected, compared)
    pygame.display.update((bar_width * start, MENU_HEIGHT,
                           bar_width * (end - start), VISUALIZER_HEIGHT))


def update_one_bar(bar, array, bar_width, mode=None):
    draw_one_bar(bar, bar_width, array, mode)
    pygame.display.update((bar_width * bar, MENU_HEIGHT, bar_width, VISUALIZER_HEIGHT))


def get_all_algorithms(cls):
    all_algorithms = [(f"{subclass.__name__}()", f"{subclass.__name__[:-4]} Sort")
                      for subclass in cls.__subclasses__()]
    return all_algorithms


def button_menu(algorithm, all_algorithms):
    clock = pygame.time.Clock()
    click = False
    while True:
        pygame.draw.rect(WIN, WHITE, MENU)
        clock.tick(FPS)
        for index, algorithms in enumerate(all_algorithms):
            button = Button(algorithms[0], index, text=algorithms[1])
            if click:
                if button.mouse_click():
                    return button.mouse_click()

        click = False
        click = check_events(algorithm, click)
        pygame.display.update(MENU)


def main():
    clock = pygame.time.Clock()
    all_algorithms = get_all_algorithms(Algorithm)
    algorithm = SelectionSort()
    click = False
    bar_width = VISUALIZER_WIDTH // algorithm.array_length
    while True:
        clock.tick(FPS)
        WIN.fill(WHITE)
        button = Button(algorithm.name, 0, text=f"{algorithm.name[0:-4]} Sort")
        if click:
            if button.menu_mouse_click():
                algorithm = button_menu(algorithm, all_algorithms)

        click = False
        click = check_events(algorithm, click)
        draw_bars(algorithm.array, bar_width, 0, algorithm.array_length)
        pygame.display.update()


if __name__ == '__main__':
    main()
